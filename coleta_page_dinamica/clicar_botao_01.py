from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # webdriver_manager
from webdriver_manager.chrome import ChromeDriverManager # webdriver_manager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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


def clicar_botao_01(link, xpath, navegador, tempo_espera):
    pagina = acessar_pagina_dinamica(link, navegador='chrome', tempo_espera = 3)
    botao = encontrar_botao(pagina, xpath)
    bs = webscrapping_bs(pagina)
    pagina.quit()
    return bs


def main():
    link = 'https://www.aladi.org/sitioaladi/language/pt/atividadeseeventos/'
    #'//button[text()=""]'
    xpath = '//*[@id="category-posts-4"]/div/button'
    pagina = acessar_pagina_dinamica(link, navegador='chrome', tempo_espera = 3)
    botao = encontrar_botao(pagina, xpath)
    bs = webscrapping_bs(pagina)
    pagina.quit()



if __name__=="__main__":
    main()
