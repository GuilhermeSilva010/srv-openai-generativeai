import json
import os

import openai
import tiktoken
from openai import OpenAI
import dotenv

from configuration.logger_config import logger
from envia_email import envia_email


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro no carregamento de arquivo: {e}")


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def modelo_gpt(prompt_sistema, prompt_usuario):
    codificador = tiktoken.encoding_for_model("gpt-4")
    lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)

    numero_tokens = len(lista_de_tokens)
    logger.info(f"Número de Tokens: {numero_tokens}")

    # Validando Gastos de Tokens que Influencia no Custo $$
    modelo = "gpt-4"
    tamanho_saida_esperado = 2048

    if numero_tokens >= 4096 - tamanho_saida_esperado:
        modelo = "gpt-3.5-turbo-16k"

    logger.info(f"Modelo escolhido: {modelo}")
    return modelo


def openai_assistant(prompt_sistema, prompt_usuario, modelo):
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        result = client.chat.completions.create(
            model=modelo,
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

        conteudo = result.choices[0].message.content
        return conteudo
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


dotenv.load_dotenv()

path_resources = os.getenv("PATH_RESOURCES")

path = os.path.join(os.path.abspath(path_resources), "data")

lista_de_compras_por_cliente = carrega(f"{path}/lista_de_compras_10_clientes.csv")

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser em json:

{
    "clientes": [
        {
            "nome": "nome cliente",
            "perfil": "descreva o perfil do cliente em 3 palavras"
        }
    ]
}
  """

modelo = modelo_gpt(prompt_sistema, lista_de_compras_por_cliente)
conteudo = openai_assistant(prompt_sistema, lista_de_compras_por_cliente, modelo)

perfis = json.loads(conteudo)

prompt_sistema = """
A partir do perfil do cliente, crie recomendações de produtos.
ignore a palavra cliente seguida de número é apenas um identificador interno.
Retorne o texto de apenas um cliente por vez, respeite a ordem.

O formato de saída deve ser:

Prezado/a Cliente (Não pode inserir o número do cliente 0,1... etc),

Espero que este e-mail o encontre bem. Em busca de tornar sua experiência de compra mais personalizada, temos o prazer de apresentar algumas recomendações de produtos alinhados aos seus interesses únicos.

[Expressão de Reconhecimento dos Interesses do Cliente]

Sabemos que você valoriza [Lista de Interesses], e é por isso que selecionamos cuidadosamente produtos que acreditamos serem perfeitos para você:

1. [Produto Recomendado 1] - [Breve Descrição e Benefícios]
2. [Produto Recomendado 2] - [Breve Descrição e Benefícios]
3. [Produto Recomendado 3] - [Breve Descrição e Benefícios]

[Chamada para Ação]

Sinta-se à vontade para explorar essas sugestões e, caso tenha alguma dúvida ou precise de mais informações, nossa equipe de atendimento está pronta para ajudar.

Agradecemos pela confiança em nossa marca e esperamos que essas recomendações tornem sua experiência de compra ainda mais especial.

Atenciosamente,
GenerativeAI
  """

modelo = modelo_gpt(prompt_sistema, conteudo)
for perfil in perfis["clientes"]:
    logger.info(f"Descrição de perfil cliente: {perfil['nome']}")
    recomendacao_email = openai_assistant(prompt_sistema, perfil["perfil"], modelo)
    envia_email(recomendacao_email)
