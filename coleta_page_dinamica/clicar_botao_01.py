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


def encontrar_botao_02(pagina, xpath):
    while True:
        try:
            # bs = webscrapping_bs(pagina)
            # infos = extrair_infos(bs)
            sleep(10)
            titulos = pagina.find_elements(By.TAG_NAME, "h5")
            botoes = pagina.find_elements(By.XPATH, "//button[@type='button']")

            tags_a = pagina.find_elements(By.CLASS_NAME, "nav-link")
            
            for tag_h5, botao in zip(titulos, botoes):
                titulo = tag_h5.text
                tag_a = botao.find_element(By.TAG_NAME, "a")
                link = tag_a.get_attribute("href")
                
                print(titulo)
                print(link)
            print("###")
            # div_noticias = pagina.find_element(By.CLASS_NAME, "row text_center")
            # noticias = div_noticias.find_elements(By.CLASS_NAME, "col-xl-4 col-md-6 col-sm-12 mt-4")

            # print(noticias)
            # for div in noticias:
            #     titulo = div.find_element(By.TAG_NAME, "h5").text
            #     tag_a = div.find_element(By.TAG_NAME, "a")
            #     link = tag_a.get_attribute("href")
            #     print(link, titulo)
            
            botao = WebDriverWait(pagina, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            botao.click()
            sleep(3)
        except:
            print("botão não encontrado")
            break
    #return infos


def webscrapping_bs(pagina):
    html_pagina = pagina.page_source
    bs = BeautifulSoup(html_pagina, "html.parser")
    return bs


def carregar_mais(link, xpath, navegador, tempo_espera):
    """funçao responsável por clicar no botão "carregar mais" ou equivalente e coletar todos os links de uma só vez"""
    pagina = acessar_pagina_dinamica(link, navegador='chrome', tempo_espera = 3)
    botao = encontrar_botao(pagina, xpath)
    bs = webscrapping_bs(pagina)
    pagina.quit()
    return bs

def percorrer_paginas(link, xpath, navegador, tempo_espera):
    """responsável por clicar no botão da próxima página, passar a página carregada para o bs e ir para a próxima página"""
    #carregar pagina
    pagina = acessar_pagina_dinamica(link, navegador='chrome', tempo_espera = 3)
    #passar pagina carregada para o bs
    botao = encontrar_botao_02(pagina, xpath)
    pagina.quit()
    


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
