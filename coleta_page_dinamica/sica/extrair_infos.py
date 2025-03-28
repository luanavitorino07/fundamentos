from inserir_bd import inserir_db

#imports para abrir a página de cada notícia e extrair as informações
import httpx  
from httpx import RequestError, TimeoutException  
from time import sleep 
from bs4 import BeautifulSoup  



#imports para formatar a data
from datetime import datetime
import locale



def extrair_infos(bs):
    noticias = bs.find_all('tr', attrs={'class':'k-master-row'})

    for noticia in noticias:
        titulo = noticia.find('h4').text.strip()
        link = f'https://www.sica.int{noticia.a['href']}'
        data = noticia.find('h5').text.strip().split()[2:7]
        data = f'{data[0]}/{data[2]}/{data[4]}'
        data_nova = data_extenso(data, '%d/%B/%Y', 'es_ES.utf8')
        autor = noticia.find('h5').text.strip().split()[-1]
        
        pagina = acessar_pagina(link)
        paragrafos = []
        paragrafos = pagina[0].find('p', attrs={'style':'text-align:justify;'}).text.strip().split('\n')


        print(f'titulo: {titulo}\n')
        print(f'link: {link}\n')
        print(f'data: {data}\n')
        print(f'autor: {autor}\n')
        print(f'paragrafos {paragrafos}\n')


        print("#########")

        var_ambiente = 'DIR_BD'
        nome_json = 'sica.json'
        inserir_db(titulo = titulo, data = data_nova, autor = autor, paragrafos = paragrafos, link=link, var_ambiente = var_ambiente, nome_json = nome_json )

        

def acessar_pagina(link, retry_attempts=6, timeout=10, backoff_factor=2):
    """
    Acessa uma página da web, com suporte a retries e tratamento de erros, incluindo falha de verificação SSL.
    """
    # Define headers para a requisição, simulando um navegador
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

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


def data_extenso (data, formato, lingua):
    """
    formata a data no padrão para inserir no banco de dados
    Parâmetros:
    ----------
    data : str (tabela com os formatos de data e horário https://archive.is/wip/IeQ7I)
        A data em formato de string que será convertida(exemplo: october 21, 2024)
    formato : str
        O formato no qual a data está representada. Exemplo: '%B %d, %Y'.
    lingua : str (tabela com os formatos das linguas : https://archive.is/wip/CL0oe) 
        O código do idioma que será utilizado para formatar a data por extenso.
        Exemplo: 'pt_BR.utf8' para português do Brasil.
    Retorno:
    ----------
    str : retorna uma string no seguinte formato "%d/%m/%Y"
    Exemplo de uso:
    ----------
    data_extenso('october 21, 2024', '%B %m, %Y', 'us_US.utf8')
    '21/10/2024'
    """

    
    locale.setlocale(locale.LC_ALL, lingua)

    # Parsear la fecha
    fecha = datetime.strptime(data, formato)

    # Formatear la fecha
    fecha_formateada = fecha.strftime('%d/%m/%Y')
    #print(fecha_formateada)
    return fecha_formateada
