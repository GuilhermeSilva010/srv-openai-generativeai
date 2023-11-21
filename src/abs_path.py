import os
from dotenv import load_dotenv

def abs_path_resource():
    # Obtém o caminho do diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Carrega as variáveis de ambiente
    load_dotenv()

    # Obtém o caminho do recurso a partir do diretório 'src'
    resource = os.getenv("PATH_RESOURCES")
    path = os.path.abspath(os.path.join(script_dir, resource))

    return path