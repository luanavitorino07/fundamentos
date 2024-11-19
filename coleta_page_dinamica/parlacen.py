import httpx
from bs4 import BeautifulSoup
from clicar_botao_01 import percorrer_paginas
from inserir_bd import inserir_db
from clicar_botao_01 import acessar_pagina_dinamica, webscrapping_bs



def main():
    link = 'https://parlacen.int/noticias'
    #'//button[text()=""]'
    xpath = '/html/body/app-root/app-noticias/div/div/div/div/div[3]/app-cards-display/div/ngb-pagination/ul/li[last()]/a/span'
    bs = percorrer_paginas(link = link, xpath= xpath, navegador = 'chrome', tempo_espera=25)
    # extrair = extrair_infos(bs)


if __name__=="__main__":
    main()