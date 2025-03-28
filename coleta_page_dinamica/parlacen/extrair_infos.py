from bs4 import BeautifulSoup
import httpx
from inserir_bd import inserir_db

#importações para abrir outra página dinâmica e clicar nela
from selenium import webdriver 
from selenium.webdriver.common.action_chains import ActionChains 
from time import sleep 

#importações para ajustar o formato da data
from datetime import datetime 
import locale 



def extrair_infos(bs): #cria uma lista com as notícias, abre cada uma invidualmente e pega suas informções pelo html
    noticias = bs.find_all('div', attrs={'class':'col-xl-4 col-md-6 col-sm-12 mt-4'})
    for noticia in noticias:
        titulo = noticia.find('h5').text.strip()
        link = f'https://parlacen.int{noticia.find('button').a['href']}'


        pagina = webdriver.Chrome() #inicia o navegador do chrome
        pagina.get(link) 
        clicar_na_pagina(pagina, 10, 10) #clica na pagina
        html_pagina = pagina.page_source
        bsPagina = BeautifulSoup(html_pagina, "html.parser")
        pagina.quit() #fecha o navegador



        autor = bsPagina.find('span', attrs={'class':'text-muted'}).text[16::].strip()

        lista_paragrafos = bsPagina.find_all('span')
        paragrafos = [paragrafo.text.strip() for paragrafo in lista_paragrafos]
        paragrafos = paragrafos[2::]   
 
        tagSmall = bsPagina.find_all('small', attrs={'class':'text-muted'})
        data = tagSmall[0].text.strip()[0:9]
        data_nova = data_extenso(data, '%Y-%m-%d', 'es_ES.utf8')

        print(f'titulo: {titulo}')
        print(f'link: {link}')
        print(f'data: {data_nova}\n')
        print(f'autor: {autor}\n')
        print(f'paragrafos {paragrafos}\n')

        print("#########")

        var_ambiente = 'DIR_BD'
        nome_json = 'parlacen.json'
        inserir_db(titulo = titulo, data = data_nova, autor = autor, paragrafos = paragrafos, link=link, var_ambiente = var_ambiente, nome_json = nome_json )


def clicar_na_pagina(driver, x, y): 
    """clica em um ponto da página, para que as informações fiquem disponíveis"""
    actions = ActionChains(driver)
    actions.move_by_offset(x, y).click().perform()
    sleep(2)  

        

def data_extenso (data, formato, lingua):
    """
    formata a data no padrão para inserir no banco de dados
    Parâmetros:
    ----------
    data : str (tabela com os formatos de data e horário https://archive.is/wip/IeQ7I)
        A data em formato de string que será convertida(exemplo: october 21, 2024)
    formato : str
        O formato no qual a data está representada. Exemplo: '%B %d, %Y'.
    lingua : str (tabela com os formatos das linguas : https://archive.is/wip/CL0oe) 
        O código do idioma que será utilizado para formatar a data por extenso.
        Exemplo: 'pt_BR.utf8' para português do Brasil.
    Retorno:
    ----------
    str : retorna uma string no seguinte formato "%d/%m/%Y"
    Exemplo de uso:
    ----------
    data_extenso('october 21, 2024', '%B %m, %Y', 'us_US.utf8')
    '21/10/2024'
    """

    
    locale.setlocale(locale.LC_ALL, lingua)

    # Parsear la fecha
    fecha = datetime.strptime(data, formato)

    # Formatear la fecha
    fecha_formateada = fecha.strftime('%d/%m/%Y')
    #print(fecha_formateada)
    return fecha_formateada
