import os
import openai
import dotenv
from openai import OpenAI
import tiktoken

from abs_path import abs_path_resource


def carrega(nome_do_arquivo):
    try:
        with open(nome_do_arquivo, "r") as arquivo:
            dados = arquivo.read()
            return dados
    except IOError as e:
        print(f"Erro: {e}")


dotenv.load_dotenv()
codificador = tiktoken.encoding_for_model("gpt-4")

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

path_resources = abs_path_resource()

prompt_usuario = carrega(f"{path_resources}/data/lista_de_compras_100_clientes.csv")

lista_de_tokens = codificador.encode(prompt_sistema + prompt_usuario)

numero_tokens = len(lista_de_tokens)
print(f"Número de Tokens: {numero_tokens}")

# Validando Gastos de Tokens que Influencia no Custo $$
modelo = "gpt-4"
tamanho_saida_esperado = 2048

if numero_tokens >= 4096 - tamanho_saida_esperado:
    modelo = "gpt-3.5-turbo-16k"

print(f"Modelo escolhido: {modelo}")

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
    max_tokens=tamanho_saida_esperado,
    presence_penalty=0,
    frequency_penalty=0,
    top_p=1
)

print(result.choices[0].message.content)
