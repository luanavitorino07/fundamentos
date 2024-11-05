import httpx
from bs4 import BeautifulSoup

def montar_urls(url,pag_inicial,pag_final):
    lista_url_paginacao = []
    contador = pag_final
    while contador > pag_inicial:
        url_paginacao = url + str(contador)
        lista_url_paginacao.append(url_paginacao)
        contador = contador - 30
    print(lista_url_paginacao)
    return(lista_url_paginacao)

def acessar_pagina(link):
    pagina = httpx.get(link)
    bs = BeautifulSoup(pagina.text,'html.parser')
    http_code = pagina.status_code
   
    return(bs, http_code)

def extrair_infos(link):
    pagina = acessar_pagina(link)#(elemento_1,elemento_2)
    bs = pagina[0]
    http_code = pagina [1]    
    lista_noticias = bs.find('div',attrs={'id':'content-core'}).find_all('article')
    for noticia in lista_noticias:
        titulo = noticia.find('h2').text.strip()
        link = noticia.a['href']
        lista_tag_span = noticia.find('span',attrs={'class':'documentByLine'}).find_all('span',attrs={'class':'summary-view-icon'})
        #print(lista_tag_span)
        data = lista_tag_span[0].text.strip()
        #for span in lista_tag_span:
         #   data = span
           # horario = span[1].text.strip()
           # tag = span[2].text.strip()
        print(titulo)
        print(link)
        print(data)
        #TODO
            #Numero da nota, horario, tag, paragrafos
        #print(horario)
        #print(tag)
        print('#'*5)

def main():
    url = "https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa/notas-a-imprensa?b_start:int="
    links = montar_urls(url,pag_inicial = 0,pag_final = 120)
    for link in links:
        extrair_infos(link)


if __name__=="__main__":
    main()
