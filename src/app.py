from flask import Flask

from abs_path import abs_path_resource
from client.openai.bot import bot_openai

import os
from generativeai.utils.helpers import carrega

# Obtém o diretório do script atual
app_directory = os.getcwd()

# Navega para o diretório pai
template_folder = os.path.dirname(app_directory)
static_folder = os.path.join(template_folder, 'web', 'static')

# Navega para o diretório  de templates
template_folder = os.path.join(template_folder, "web", 'templates')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
app.secret_key = 'alura'

path_resources = abs_path_resource()

path = os.path.join(path_resources, "ecommerce", "dados_ecommerce.txt")

dados_ecommerce = carrega(path)

from web.views import *


def bot(prompt, historico):
    while True:
        bot_openai(dados_ecommerce, historico, prompt)


if __name__ == "__main__":
    app.run(debug=True)
