import httpx  # Importa a biblioteca httpx para realizar requisições web
from httpx import RequestError, TimeoutException  # Importa exceções específicas do httpx
from time import sleep  # Importa a biblioteca time para usar a função sleep
from bs4 import BeautifulSoup  # Importa BeautifulSoup para analisar o HTML

def acessar_pagina(link, retry_attempts=6, timeout=10, backoff_factor=2):
    """
    Acessa uma página da web, com suporte a retries e tratamento de erros, incluindo falha de verificação SSL.

    Args:
        link (str): A URL da página a ser acessada.
        retry_attempts (int, optional): Número máximo de tentativas de acesso. Defaults to 6.
        timeout (int, optional): Tempo limite de espera da resposta em segundos. Defaults to 10.
        backoff_factor (int, optional): Fator de espera exponencial entre tentativas. Defaults to 2.

    Returns:
        tuple: Um objeto BeautifulSoup em caso de sucesso, ou None em caso de falha, junto com o código HTTP da resposta.

    Notes:
        - Utiliza a biblioteca 'httpx' para realizar as requisições HTTP, que é mais moderna e rápida que a 'requests'.
        - Implementa um algoritmo de retries com espera exponencial para lidar com erros de rede, aumentando a robustez da função ao acessar páginas web.
        - Em caso de sucesso, retorna um objeto BeautifulSoup para facilitar a extração de dados da página.
        - Os headers da requisição são definidos para simular um navegador web, evitando bloqueios por parte de alguns sites.
    """
    # Define headers para a requisição, simulando um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    # Loop de tentativas de acesso à página
    """
    Problema que essa parte do código resolveu:
        requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='oglobo.globo.com', port=443): Max retries exceeded with url: /politica/noticia/2024/04/09/moro-julgado-no-tre-pr-dois-unicos-votos-pela-cassacao-foram-de-indicados-por-lula.ghtml (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x7a20bbf12330>, 'Connection to oglobo.globo.com timed out. (connect timeout=None)'))
    """
    http_code = None
    for attempt in range(retry_attempts):
        try:
            pagina = httpx.get(link, headers=headers, timeout=timeout)  # Faz a requisição GET
            http_code = pagina.status_code  # Obtém o código de status HTTP
            pagina.raise_for_status()  # Lança uma exceção se houver um erro HTTP (códigos 4xx ou 5xx)
            bs = BeautifulSoup(pagina.text, "html.parser")  # Analisa o HTML com BeautifulSoup
            return bs, http_code  # Retorna o BeautifulSoup e o código de status se a requisição for bem-sucedida

        except httpx.ConnectError as e:
            if 'certificate verify failed' in str(e):
                print(f"SSL verification failed on attempt {attempt + 1}. Retrying without SSL verification...")
                try:
                    pagina = httpx.get(link, headers=headers, timeout=timeout, verify=False)
                    http_code = pagina.status_code
                    pagina.raise_for_status()
                    bs = BeautifulSoup(pagina.text, "html.parser")
                    return bs, http_code
                except Exception as e_ssl:
                    print(f"Retry without SSL verification failed: {e_ssl}")
        
        except httpx.TimeoutException:
            print(f"Timeout error on attempt {attempt + 1}")

        except httpx.RequestError as exc:
            print(f"An error occurred: {exc}")
        
        except Exception as exc:
            print(f"An unexpected error occurred: {exc}")
        
        if attempt < retry_attempts - 1:
            sleep_time = backoff_factor ** attempt
            print(f"Retrying in {sleep_time} seconds...")
            sleep(sleep_time)
    
    return None, http_code  # Retorna None se todas as tentativas falharem