from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager # webdriver_manager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from extrair_infos import extrair_infos


def carregar_mais(link, xpath, navegador, tempo_espera):
    """funçao responsável por clicar no botão "carregar mais" ou equivalente e coletar todos os links de uma só vez"""
    pagina = acessar_pagina_dinamica(link, navegador='chrome', tempo_espera = 3)
    botao = encontrar_botao(pagina, xpath)
    bs = webscrapping_bs(pagina)
    pagina.quit()
    return bs


def acessar_pagina_dinamica(link, navegador = 'chrome', tempo_espera = 3):
    if navegador == "chrome":
        pagina = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif navegador == "edge":
        pagina = webdriver.Edge(EdgeChromiumDriverManager().install())


    pagina.get(link)
    sleep(tempo_espera)
    return pagina

def encontrar_botao(pagina, xpath):
    while True:
        try:
            botao = WebDriverWait(pagina, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            botao.click()
            sleep(3)
        except:
            print("botão não encontrado")
            break


def webscrapping_bs(pagina):
    html_pagina = pagina.page_source
    bs = BeautifulSoup(html_pagina, "html.parser")
    return bs
 


def main():
    link = 'https://www.aladi.org/sitioaladi/language/pt/atividadeseeventos/'
    xpath = '/html/body/div[2]/div[4]/div/div/div/main/article/div/aside/div/button'
    bs = carregar_mais(link = link, xpath= xpath, navegador = 'chrome', tempo_espera=3)
    extrair_infos(bs)



if __name__=="__main__":
    main()
