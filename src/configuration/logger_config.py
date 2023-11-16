import datetime
import logging
import os
from dotenv import load_dotenv


load_dotenv()

def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Nível de logging (pode ser ajustado conforme necessário)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Obter a data atual
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # Obter o caminho absoluto do diretório de logs
    log_directory = os.path.abspath('logs')

    # Verificar se o diretório de logs existe, se não, criar o diretório
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Configurar o manipulador do arquivo de log com a data no nome do arquivo
    application_name = os.getenv("APPLICATION_NAME")
    path_logs = os.getenv("PATH_LOGS")

    log_file_name = os.path.join(path_logs, f"arq_ia_fortify_{application_name}_{current_date}.log")

    file_handler = logging.FileHandler(log_file_name)

    file_handler.setLevel(logging.INFO)  # Apenas registra mensagens de erro e superiores
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
