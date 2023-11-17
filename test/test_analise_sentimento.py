import os
import unittest
from unittest.mock import patch, MagicMock
from src.analise_sentimento import analise_sentimento  # ou importe a função que deseja testar


class TestAnaliseSentimento(unittest.TestCase):
    @patch("openai.OpenAI")
    @patch("src.configuration.logger_config")
    def test_analise_sentimento(self, mock_logger, mock_openai):
        # Configurar mocks e dados simulados
        nome_do_produto = "DVD player automotivo"
        prompt_usuario = "Avaliação simulada."

        # Configurar retorno simulado para a chamada da API OpenAI
        mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = "Resultado simulado."

        # Chamar a função
        analise_sentimento(nome_do_produto)

        # Verificar se os métodos esperados foram chamados
        mock_logger.info.assert_called_with(f"Iniciando a análise do produto: {nome_do_produto}")
        api_key = os.getenv("OPENAI_API_KEY")
        mock_openai.assert_called_with(api_key=api_key)  # Substitua pelo valor correto
        mock_openai.return_value.chat.completions.create.assert_called_with(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Seu prompt de sistema"},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=1,
            max_tokens=2048,
            presence_penalty=0,
            frequency_penalty=0,
            top_p=1
        )
        mock_logger.info.assert_called_with("Análise concluída com sucesso!")


if __name__ == "__main__":
    unittest.main()
