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


def percorrer_paginas(link, xpath, navegador, tempo_espera):
    """responsável por clicar no botão da próxima página, passar a página carregada para o bs e ir para a próxima página"""
    #carregar pagina
    pagina = acessar_pagina_dinamica(link, navegador='chrome', tempo_espera = 3)
    #passar pagina carregada para o bs
    botao = encontrar_botao(pagina, xpath)
    pagina.quit()


def acessar_pagina_dinamica(link, navegador = 'chrome', tempo_espera = 3): #função que apre o navegador com o link
    if navegador == "chrome":
        pagina = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    elif navegador == "edge":
        pagina = webdriver.Edge(EdgeChromiumDriverManager().install())

    pagina.get(link)
    sleep(tempo_espera)
    return pagina


def encontrar_botao(pagina, xpath):#função que extrai o html da página, extrai as informações desejadas, encontra o botão da próxima página e clica nele
    while True:    
        try:
            bs = webscrapping_bs(pagina)
            infos = extrair_infos(bs)
            sleep(3)
            botao = WebDriverWait(pagina, 15).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            botao.click()
            sleep(10)
        except:
            print("botão não encontrado")
            break
            

def webscrapping_bs(pagina):
    html_pagina = pagina.page_source
    bs = BeautifulSoup(html_pagina, "html.parser")
    return bs


def main():
    link = 'https://www.sica.int/consulta/noticias_401_3_1.html'
    xpath = '/html/body/div[2]/div/div[1]/div/article/section/div[2]/div/div/section/div[1]/div/a[3]/span'
    bs = percorrer_paginas(link = link, xpath= xpath, navegador = 'chrome', tempo_espera=25)



if __name__=="__main__":
    main()
