from bs4 import BeautifulSoup
from clicar_botao_01 import clicar_botao_01

def extrair_infos(bs):
    noticias = bs.find_all('li', attrs={'class':'cat-post-item'})
    for noticia in noticias:
        link = noticia.a['href']
        print(link)


def main():
    link = 'https://www.aladi.org/sitioaladi/language/pt/atividadeseeventos/'
    #'//button[text()=""]'
    xpath = '//*[@id="category-posts-4"]/div/button'
    bs = clicar_botao_01(link = link, xpath= xpath, navegador = 'chrome', tempo_espera=3)
    extrair = extrair_infos(bs)

if __name__=="__main__":
    main()
