import dotenv
import os
from openai import OpenAI


def categorizar_produto(nome_produto, categorias_validas):
    dotenv.load_dotenv()

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    # Exemplo de Engenharia de Prompt Consistente - prompt system
    # Você é um assistente de programação
    ####### Contexto
    # Você está atuando com vulnerabilidades e melhorias de código.
    # Você precisa enviar a melhor solução possível para o problema apresentado.
    ### Exemplo
    # var1 = var1 
    # variavel = var1

    prompt_sistema = f"""
    Você é um categorizador de produtos.
    Você deve escolher uma categoria da lista abaixo.
    Caso as categorias informadas, não sejam válidas, responda da seguinte forma: "Não Posso Ajudar, Tente Novamente com Categorias Válidas"
    ##### Categorias Validas
    {categorias_validas}
    #### Exemplo
    Bola de Futebol
    Esportes
    """
    result = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt_sistema
            },
            {
                "role": "user",
                "content": nome_produto
            }
        ],
        temperature=1,
        max_tokens=256,
        presence_penalty=0,
        frequency_penalty=0,
        top_p=1
    )

    print("A Categoria Mais Adequada Para Este Produto")
    print(result.choices[0].message.content)


print("Digite as Categorias Válidas")
print("Exemplo: 'Esportes, Beleza, Moda, Pet, Outros'")

categorias_validas = input()

while True:
    print("Digite o Nome do Produto")

    nome_produto = input()

    categorizar_produto(nome_produto, categorias_validas)
