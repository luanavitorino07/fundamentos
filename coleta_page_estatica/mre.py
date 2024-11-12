import httpx
from bs4 import BeautifulSoup
from inserir_bd import inserir_db

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

        numero_da_nota = int(noticia.find('span').text.strip().split()[-1])
        data = lista_tag_span[0].text.strip()
        horario = lista_tag_span[1].text.strip()
        tag = lista_tag_span[2].text.strip()

        pegar_paragrafos = acessar_pagina(link)
        bs = pegar_paragrafos[0]
        http_code = pegar_paragrafos[1]  
        lista_paragrafos = bs.find('div',attrs={'id':'content-core'}).find_all('p')
        # paragrafos = []
        # for paragrafo in lista_paragrafos:              
        #     tagp = paragrafos.append(paragrafo.text.strip())
        #compreensao de lista
        paragrafos = [paragrafo.text.strip() for paragrafo in lista_paragrafos]
        paragrafos.append("")
        #utilizacao do filter para tirar strings vazias da lista
        paragrafos = list(filter(None, paragrafos))
            


        print(titulo)
        print(numero_da_nota)
        print(link)
        print(data)
        print(horario)
        print(tag)
        print(paragrafos)


        var_ambiente = 'DIR_BD'
        nome_json = 'teste2.json'
        inserir_db(titulo = titulo, numero_da_nota = numero_da_nota, data = data, horario = horario, tag = tag, paragrafos = paragrafos, link=link, var_ambiente = var_ambiente, nome_json = nome_json )

 
        print('#'*5)

def main():
    url = "https://www.gov.br/mre/pt-br/canais_atendimento/imprensa/notas-a-imprensa/notas-a-imprensa?b_start:int="
    links = montar_urls(url,pag_inicial = 0,pag_final = 120)
    for link in links:
        extrair_infos(link)


if __name__=="__main__":
    main()
