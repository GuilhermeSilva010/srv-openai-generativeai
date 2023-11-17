import os

import dotenv
import openai
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from abs_path import abs_path_resource
from configuration.logger_config import logger


# Tratamento de Exceções e Retentativa de Chamadas da API OpenIA
@retry(reraise=True,
       retry=retry_if_exception_type((openai.RateLimitError, openai.UnprocessableEntityError, openai.APITimeoutError,
                                      openai.InternalServerError)),
       wait=wait_exponential(multiplier=1, min=5, max=10),
       stop=stop_after_attempt(3))
def analise_sentimento(nome_do_produto):

    prompt_sistema = """
    Você é um analisador de sentimentos de avaliações de produtos.
    Escreva um parágrafo com até 50 palavras resumindo as avaliações e depois atribua qual o sentimento geral para o produto.
    Identifique também 3 pontos fortes e 3 pontos fracos identificados a partir das avaliações.

    #### Formato de saída

    Nome do produto: 
    Resumo das avaliações:
    Sentimento geral: [aqui deve ser POSITIVO, NEUTRO ou NEGATIVO]
    Pontos fortes: [3 bullet points]
    Pontos fracos: [3 bullet points]
    """

    path_resources = abs_path_resource()

    path = os.path.join(path_resources, "data")

    prompt_usuario = carrega(f"{path}/avaliacoes-{nome_do_produto}.txt")
    logger.info(f"Iniciando a análise do produto: {nome_do_produto}")

    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        result = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": prompt_usuario
                }
            ],
            temperature=1,
            max_tokens=2048,
            presence_penalty=0,
            frequency_penalty=0,
            top_p=1
        )

        salva(f"{path}/analise-{nome_do_produto}", result.choices[0].message.content)
        logger.info("Análise concluída com sucesso!")
        return
    except openai.AuthenticationError as e:
        logger.error(f"Erro de autenticação, verifique as credenciais enviadas ao OpenAI: {e}")
    except openai.APITimeoutError as e:
        logger.error(f"Timeout na chamada da API: {e}")
        raise
    except openai.APIConnectionError as e:
        logger.error(f"Falha ao conectar com OpenAI: {e}")
    except openai.RateLimitError as e:
        logger.error(f"OpenAI API requisição excedeu o limite: {e}")
        raise
    except openai.UnprocessableEntityError as e:
        logger.error(f"Entidade não processada: {e}")
        raise
    except openai.InternalServerError as e:
        logger.error(f"Erro no retorno da chamada da API: {e}")
        raise
    except openai.APIError as e:
        logger.error(f"Ocorreu um erro com essa chamada, verifique mais tarde o problema: {e}")
        logger.error("Pulando para o proximo item")


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        logger.error(f"Erro no carregamento de arquivo: {e}")


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        logger.error(f"Erro ao salvar arquivo: {e}")


dotenv.load_dotenv()

lista_de_produtos = ["DVD player automotivo", "Esteira elétrica para fitness", "Grill elétrico para churrasco",
                     "Mixer de sucos e vitaminas", "Tapete de yoga", "Miniatura de carro colecionável",
                     "Balança de cozinha digital", "Jogo de copos e taças de cristal", "Tabuleiro de xadrez de madeira",
                     "Boia inflável para piscina"]
for nome_do_produto in lista_de_produtos:
    analise_sentimento(nome_do_produto)

