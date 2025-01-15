from templates import acessar_pagina, data_extenso
from bs4 import BeautifulSoup
import httpx
from inserir_bd import inserir_db



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

        

