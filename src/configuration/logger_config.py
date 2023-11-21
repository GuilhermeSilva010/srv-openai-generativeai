import datetime
import logging
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


def setup_logger():
    # Configurar o logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Nível de logging (ajustável conforme necessário)

    # Formato para as mensagens de log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Obter informações do ambiente
    application_name = os.getenv("APPLICATION_NAME")
    path_logs = os.getenv("PATH_RESOURCES")

    # Obtém o caminho do diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    path = os.path.abspath(os.path.join(script_dir, "..", path_logs))

    # Diretório de logs
    log_directory = os.path.join(path, "logs")

    # Verificar se o diretório de logs existe; criar se não existir
    os.makedirs(log_directory, exist_ok=True)

    # Nome do arquivo de log com a data
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file_name = f"openai_{application_name}_{current_date}.log"
    log_file_path = os.path.join(log_directory, log_file_name)

    # Configurar o manipulador do arquivo de log
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)  # Registrar mensagens de INFO e superiores
    file_handler.setFormatter(formatter)

    # Adicionar o manipulador do arquivo ao logger
    logger.addHandler(file_handler)

    # Adicionar um manipulador para exibir logs no terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)  # Pode ajustar conforme necessário
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


# Configurar o logger
logger = setup_logger()
