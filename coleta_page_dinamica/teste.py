from bs4 import BeautifulSoup
import httpx

def acessar_pagina(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    print(link)
    pagina = httpx.get(link, headers = headers)
    print('acessado')
    bs1 = BeautifulSoup(pagina.text,'html.parser')
    return bs1

acessar_pagina('https://www.sica.int/noticias/sg-sica-realiza-encuentro-nacional-sobre-justicia-juvenil-restaurativa-en-honduras_1_134705.html')