from templates import acessar_pagina
from bs4 import BeautifulSoup
import httpx
from inserir_bd import inserir_db


# def acessar_pagina(link):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Connection': 'keep-alive',
#     }
#     print(link)
#     pagina = httpx.get(link, headers = headers)
#     print('acessado')
#     bs1 = BeautifulSoup(pagina.text,'html.parser')
#     return bs1

def extrair_infos(bs):
    #TODO: tratar data e autoria
    #TODO: transformar paragrafos em lista 
    #TODO: converter a data para dd/mm/yyyy https://gitlab.com/unesp-labri/projeto/templates/-/blob/main/locale.py?ref_type=heads
    noticias = bs.find_all('tr', attrs={'class':'k-master-row'})
    for noticia in noticias:
        titulo = noticia.find('h4').text.strip()
        link = f'https://www.sica.int{noticia.a['href']}'
        data = noticia.find('h5').text.strip()
        
        pagina = acessar_pagina(link)
        #paragrafos = pagina.find('p').text.strip()
        


        print(f'titulo: {titulo}\n')
        print(f'link: {link}\n')
        print(f'data: {data}\n')
        print(f'paragrafos {paragrafos}\n')


        print("#########")
    # return titulo, link
        
