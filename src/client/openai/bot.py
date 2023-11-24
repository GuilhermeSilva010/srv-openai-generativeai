import os

import dotenv
import openai
from openai import OpenAI
from tenacity import retry_if_exception_type, wait_exponential, stop_after_attempt, retry

from configuration.logger_config import logger


@retry(reraise=True,
       retry=retry_if_exception_type((openai.APIError, openai.APITimeoutError)),
       wait=wait_exponential(multiplier=1, min=1, max=2),
       stop=stop_after_attempt(1))
def bot_openai(dados_ecommerce, historico, prompt):
    dotenv.load_dotenv()

    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        model = 'gpt-4'
        prompt_do_sistema = f"""
        Você é um chatbot de atendimento a clientes de um e-commerce.
        Você não deve responder perguntas que não sejam dados do ecommerce informado!
        ## Dados do ecommerce:
        {dados_ecommerce}
        ## Historico:
        {historico}
        """
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": prompt_do_sistema
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=True,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            model=model)
        return response
    except openai.AuthenticationError as e:
        logger.error(f"Erro de autenticação, verifique as credenciais enviadas ao OpenAI: {e}")
    except openai.APITimeoutError as e:
        logger.error(f"Timeout na chamada da API: {e}")
        raise
    except openai.APIError as e:
        logger.error(f"Ocorreu um erro com essa chamada, verifique mais tarde o problema: {e}")
        logger.error("Pulando para o proximo item")
