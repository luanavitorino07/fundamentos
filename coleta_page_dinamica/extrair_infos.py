from bs4 import BeautifulSoup
import httpx
from inserir_bd import inserir_db

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager # webdriver_manager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from clicar_botao_01 import acessar_pagina_dinamica, webscrapping_bs

def webscrapping_bs(pagina):
    html_pagina = pagina.page_source
    bs = BeautifulSoup(html_pagina, "html.parser")
    return bs


def acessar_pagina_dinamica(link, navegador = 'chrome', tempo_espera = 3):
    if navegador == "chrome":
        pagina = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif navegador == "edge":
        pagina = webdriver.Edge(EdgeChromiumDriverManager().install())


    pagina.get(link)
    sleep(tempo_espera)
    return pagina

def acessar_pagina(link):
    print(link)
    pagina = httpx.get(link)
    bs1 = BeautifulSoup(pagina.text,'html.parser')
   
    return bs1

def extrair_infos(bs):
    noticias = bs.find_all('div', attrs={'class':'col-xl-4 col-md-6 col-sm-12 mt-4'})
    for noticia in noticias:
        titulo = noticia.find('h5').text.strip()
        link = f'https://parlacen.int{noticia.a['href']}'
        
        acessar = acessar_pagina_dinamica(link)
        acessar_link = webscrapping_bs(acessar)
        print("acessado") 
        print(acessar_link)


        data = acessar_link.find('app-noticia').find('small', attrs={'class': 'text-muted'})
        # paragrafos = acessar_link.find('p', attrs={'class':'card-text info-text pt-5 mt-2 px-2-responsive'}).text.strip()
        # print("acessado")  
        
        #data = "NA"
        paragrafos = "NA"

        print(titulo)
        print(link)
        print(data)
        #print(paragrafos)
        var_ambiente = 'DIR_BD'
        nome_json = 'parlacen.json'
        inserir_db(titulo = titulo, data = data,  paragrafos = paragrafos, link=link, var_ambiente = var_ambiente, nome_json = nome_json )
        print()
    print("#########")
    # return titulo, link
        
