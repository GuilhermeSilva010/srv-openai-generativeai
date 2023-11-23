import openai
import requests
from PIL import Image
from dotenv import load_dotenv
import os
from instabot import Bot
import shutil

from openai import OpenAI

from abs_path import abs_path_resource
from configuration.logger_config import logger


def salva(nome_do_arquivo, conteudo):
    try:
        with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write(conteudo)
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")


def openai_assistant_chat_resume_imagem(resumo):
    print("Resumindo com o gpt para um post do instagram ...")

    prompt_sistema = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.

    """
    prompt_usuario = ". \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"

    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        result = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
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


def openai_assistant_hashtags(resumo_instagram):
    print("Gerando as hashtags com a open ai ... ")

    prompt_sistema = """
        Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

        Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

        - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
        - Você deve utilizar o gênero neutro na construção do seu texto
        - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
        - O texto deve ser escrito em português do Brasil.
        - A saída deve conter 5 hashtags.

        """

    prompt_usuario = f'Aqui está um resumo de um texto "{resumo_instagram}". Por favor, gere 5 hashtags que sejam relevantes para este texto e que possam ser publicadas no Instagram.  Por favor, faça isso em português do Brasil '

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
            temperature=0.6,
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


def openai_assistant_chat_resume(transcricao):
    print("Resumindo com o gpt para um post do instagram ...")

    prompt_sistema = """
    Assuma que você é um digital influencer digital e que está construíndo conteúdos das áreas de tecnologia em uma plataforma de áudio (podcast).

    Os textos produzidos devem levar em consideração uma peresona que consumirá os conteúdos gerados. Leve em consideração:

    - Seus seguidores são pessoas super conectadas da área de tecnologia, que amam consumir conteúdos relacionados aos principais temas da área de computação.
    - Você deve utilizar o gênero neutro na construção do seu texto
    - Os textos serão utilizados para convidar pessoas do instagram para consumirem seu conteúdo de áudio
    - O texto deve ser escrito em português do Brasil.

    """
    prompt_usuario = ". \nReescreva a transcrição acima para que possa ser postado como uma legenda do Instagram. Ela deve resumir o texto para chamada na rede social. Inclua hashtags"

    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        result = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": prompt_sistema
                },
                {
                    "role": "user",
                    "content": transcricao + prompt_usuario
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


def openai_assistant_whisper(audio_file):
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
        conteudo = transcript.text
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


def openai_assistant_dall_e(texto_imagem):
    load_dotenv()
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        logger.info("Criando Imagem utilizando a API do DALL-E")

        image = client.images.generate(
            model="dall-e-3",
            quality='hd',
            prompt=f"Uma pintura ultra futurista, textless, 3d que retrate {texto_imagem}",
            n=1,
            size="1024x1024"
        )
        logger.info("Finalizando Geração de Imagens")

        return image.data
    except openai.APIError as e:
        logger.error(f"Ocorreu um erro com essa chamada, verifique mais tarde o problema: {e}")
        logger.error("Pulando para o proximo item")


def postar_instagram(caminho_imagem, texto, user, password):
    if os.path.exists("config"):
        shutil.rmtree("config")
    bot = Bot()

    bot.login(username=user, password=password)

    resposta = bot.upload_photo(caminho_imagem, caption=texto)

def ferramenta_download_imagem(imagem_gerada):
    lista_nome_imagens = []
    try:
        ## alterar por quantidade de imagens invés de 4 - criar variavel
        for contador_imagens in range(0, 1):
            caminho = imagem_gerada[contador_imagens].url
            imagem = requests.get(caminho)

            with open(f"alura_{contador_imagens}.png", "wb") as arquivo_imagem:
                arquivo_imagem.write(imagem.content)

            lista_nome_imagens.append(f"alura_{contador_imagens}.png")
        return lista_nome_imagens
    except:
        print("Ocorreu um erro!")
        return None


# código omitido

def ferramenta_converter_png_para_jpg(caminho_imagem_escolhida):
    img_png = Image.open(caminho_imagem_escolhida)
    img_png.save(caminho_imagem_escolhida.split(".")[0] + ".jpg")

    return caminho_imagem_escolhida.split(".")[0] + ".jpg"


def confirmacao_postagem(caminho_imagem_convertida, Legenda_postagem):
    print("f\nCaminho Imagem: (caminho_imagem_convertida}")
    print(f"\Legenda: {Legenda_postagem}")

    print("\n\nDeseja postar os dados acima no seu instagram? Digite 's' para sim e 'n' para não.")
    return input()

def ferramenta_conversao_binario_para_string(texto):
    if isinstance(texto, bytes):
        return str(texto.decode())
    return texto

def transcription():
    caminho_audio = "teste.mp3"

    nome_arquivo = "Tchau Obrigado 2 - MC Ryan SP, Kadu, IG, MC GP, Kanhoto, Paulin Da Capital, MC GH Do 7 (DJ Victor)"
    url_podcast = "https://www.youtube.com/watch?v=8dfSth3DrO4"

    path_resources = abs_path_resource()

    path = os.path.join(path_resources, "data", "audio")
    path_audio = f"{path}/{caminho_audio}"

    audio_file = open(path_audio, "rb")  # mudar para o metodo carrega, separando eles em um arquivo files.
    logger.info("Leitura do arquivo efetuada com sucesso")
    transcricao = openai_assistant_whisper(audio_file)

    resumo_transcricao = openai_assistant_chat_resume(transcricao)
    logger.info("Resumo Feito com sucesso")
    logger.info("Iniciando geração de hashtags")
    hashtags = openai_assistant_hashtags(resumo_transcricao)
    logger.info("Finalizando geração de hashtags")

    resumo_transcricao.join(f"\n{hashtags}")

    logger.info("iniciando geração de texto para criação de imagem")
    texto_imagem = openai_assistant_chat_resume_imagem(resumo_transcricao)

    # imagens_data = openai_assistant_dall_e(texto_imagem)
    #
    # ferramenta_download_imagem(imagens_data)

    legenda_imagem = f"Link do Podcast: {ferramenta_conversao_binario_para_string(url_podcast)} \n {ferramenta_conversao_binario_para_string(resumo_transcricao)} \n {ferramenta_conversao_binario_para_string(hashtags)}"

    logger.info(legenda_imagem)
    logger.info(f'HASHTASG: {hashtags}')

    image_jpg = ferramenta_converter_png_para_jpg('alura_escolhida.png')

    if confirmacao_postagem(image_jpg, legenda_imagem).lower() == "s":
        user = os.getenv("USER_INSTAGRAM")
        password =  os.getenv("PASSWORD_INSTAGRAM")
        postar_instagram('alura_0.jpg', legenda_imagem, user, password)

    # salva(f"{path}/resumo-insta-{nome_arquivo}", resumo_transcricao)


transcription()
