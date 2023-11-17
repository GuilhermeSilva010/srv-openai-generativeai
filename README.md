# Sistema de Recomendação Utilizando OpenAI

## Visão Geral

Este sistema, atualmente em forma de script, proporciona funcionalidades de recomendação de produtos baseadas nos interesses do cliente. Utilizando a API da OpenAI, Python e outras ferramentas, o sistema cria e envia e-mails personalizados.

## Pré-requisitos

Antes de utilizar o sistema, assegure-se de possuir:

- Uma conta no OpenAI para obter uma chave de API.
- Ferramentas: Python 3.1.+, OpenAI, Tiktoken, Smtplib, Tenacity, Git, unittest.
- Variáveis de ambiente configuradas (consulte a seção abaixo).

## Configuração de Variáveis de Ambiente

O sistema depende de várias variáveis de ambiente. Certifique-se de configurar as seguintes variáveis:

- `OPENAI_API_KEY`: Chave de API do OpenAI, gerada no site do OpenAI.
- `email_destinatario`: Endereço de e-mail do destinatário.
- `email_remetente`: Endereço de e-mail do remetente.
- `key_google_app`: Chave de aplicativo Google, gerada conforme [este link](https://support.google.com/accounts/answer/185833?visit_id=638357805751377685-173321712&p=InvalidSecondFactor&rd=1).

## Como Utilizar

### 1. Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/GuilhermeSilva010/srv-openai-generativeai.git
cd srv-openai-generativeai
pip install -r requirements.txt
```
### 2. Configuração

Configure as variáveis de ambiente conforme mencionado acima.

### 3. Execução

Execute o script desejado, como o recomendador.py, que realiza a leitura de dados, integração com o OpenAI para análise de interesses do cliente, criação de e-mail de recomendação e envio.

```bash
python3 recomendador.py
```

### 4. Atenção aos Tokens
Observe cuidadosamente o consumo de tokens por requisição. Defina limites adequados para tokens por requisição, bem como limites diários/mensais para controlar os custos ao utilizar a API do OpenAI.

### Testes
O sistema inclui várias classes de teste. A classe mais completa até o momento é recomendador.py, que realiza todo o processo de recomendação e envio de e-mail.

### Suporte
Para obter suporte adicional, consulte a documentação do OpenAI e fique atento às melhores práticas para o uso da API, garantindo um uso eficiente e econômico. Duvidas sobre os desenvolvimento e ferramentas utilizadas consulte os links abaixo das documentações.

- Documentação OpenAI - [link](https://platform.openai.com/docs/overview). 
- Documentação Tenacity - [link](https://tenacity.readthedocs.io/en/latest/).
- GitFlow - [link](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow#:~:text=Gitflow%20is%20an%20alternative%20Git,lived%20branches%20and%20larger%20commits.).
- Git Semantics para Commits - [link](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716).
- Google Key App - [link](https://support.google.com/accounts/answer/185833?visit_id=638357805751377685-173321712&p=InvalidSecondFactor&rd=1).

### Créditos

- Alura - [link](https://cursos.alura.com.br/loginForm)
- Jeferson Rodrigues da Silva
- Guilherme Carvalho - Linkedin - [link](https://www.linkedin.com/in/guilherme-carvalho010/)
- 