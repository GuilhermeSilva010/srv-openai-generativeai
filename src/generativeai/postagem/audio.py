import openai
from dotenv import load_dotenv
import os

from openai import OpenAI

from abs_path import abs_path_resource
from configuration.logger_config import logger


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def openai_assistant(audio_file):
    load_dotenv()
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("iniciando Transcrição de Aúdio")
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        logger.info("Finalizando Transcrição de Aúdio")
        conteudo = transcript.choices[0].message.content
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


def transcription():
    caminho_audio = "SnapInsta.io - Tchau Obrigado 2 - MC Ryan SP, Kadu, IG, MC GP, Kanhoto, Paulin Da Capital, MC GH Do 7 (DJ Victor) (128 kbps).mp3"


    nome_arquivo = "Tchau Obrigado 2 - MC Ryan SP, Kadu, IG, MC GP, Kanhoto, Paulin Da Capital, MC GH Do 7 (DJ Victor)"
    url_podcast = "https://www.youtube.com/watch?v=8dfSth3DrO4"

    path_resources = abs_path_resource()

    path = os.path.join(path_resources, "data", "audio")

    audio_file = open(caminho_audio, "rb")
    logger.info("Leitura do arquivo efetuada com sucesso")
    transcricao = openai_assistant(audio_file)

    salva(f"{path}/trascricao-{nome_arquivo}", transcricao)

transcription()
