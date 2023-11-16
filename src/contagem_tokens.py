import tiktoken

codificador  = tiktoken.encoding_for_model("gpt-4")
lista_de_tokens = codificador.encode("Você é um categorizador de produtos")

print(lista_de_tokens)
print(f"Quantidade de Tokens: {len(lista_de_tokens)}")
custo_entrada = (len(lista_de_tokens)/1000) * 0.0015
print(custo_entrada)