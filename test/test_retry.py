import unittest
from unittest.mock import patch
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import OpenAIError

# Seu código aqui
def funcao_que_pode_falhar():
    # Simular um RateLimitError após 2 tentativas
    if funcao_que_pode_falhar.contador <= 2:
        raise OpenAIError("Simulando OpenAIError")
    else:
        return "Operação bem-sucedida"

@retry(reraise=True,
       retry=retry_if_exception_type((OpenAIError)),
       wait=wait_exponential(multiplier=1, min=5, max=10),
       stop=stop_after_attempt(3))
def chamada_com_retry():
    return funcao_que_pode_falhar()

# Classe de teste
class TestRetry(unittest.TestCase):

    def test_retry_exemplo(self):
        with patch('test_retry.funcao_que_pode_falhar') as mock_funcao:
            # Simulando uma exceção nas duas primeiras chamadas
            mock_funcao.side_effect = [OpenAIError("Erro 1"), OpenAIError("Erro 2"), "Operação bem-sucedida"]

            # Teste da função com retry
            resultado = chamada_com_retry()

            # Verificar se o resultado é o esperado
            self.assertEqual(resultado, "Operação bem-sucedida")

if __name__ == '__main__':
    unittest.main()
