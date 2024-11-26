import httpx
from bs4 import BeautifulSoup
from clicar_botao_01 import percorrer_paginas
from inserir_bd import inserir_db
from clicar_botao_01 import acessar_pagina_dinamica, webscrapping_bs



def main():
    link = 'https://www.sica.int/consulta/noticias_401_3_1.html'
    #'//button[text()=""]'
    xpath = '/html/body/div[2]/div/div[1]/div/article/section/div[2]/div/div/section/div[1]/div/a[3]/span'
    bs = percorrer_paginas(link = link, xpath= xpath, navegador = 'chrome', tempo_espera=25)
    # extrair = extrair_infos(bs)


if __name__=="__main__":
    main()