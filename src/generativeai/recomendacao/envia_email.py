import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from configuration.logger_config import logger


def envia_email(conteudo):
    remetente = os.getenv("EMAIL_REMETENTE")
    destinatario = os.getenv("EMAIL_DESTINATARIO")
    key_google_app = os.getenv("KEY_GOOGLE_APP")

    # Configurações do remetente e do destinatário
    remetente_email = remetente
    remetente_senha = key_google_app
    destinatario_email = destinatario

    # Configuração do servidor SMTP do Gmail
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Criar uma mensagem
    assunto = 'Recomendações de Produtos - IA'
    corpo = conteudo
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente_email
    mensagem['To'] = destinatario_email
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(corpo, 'plain'))

    # Configurar o servidor SMTP e enviar o e-mail
    try:
        servidor_smtp = smtplib.SMTP(smtp_server, smtp_port)
        servidor_smtp.starttls()  # Ativar a criptografia TLS
        servidor_smtp.login(remetente_email, remetente_senha)
        servidor_smtp.sendmail(remetente_email, destinatario_email, mensagem.as_string())
        servidor_smtp.quit()
        logger.info('E-mail enviado com sucesso!')
    except Exception as e:
        logger.error(f'Erro ao enviar e-mail: {e}')
