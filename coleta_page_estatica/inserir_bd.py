from tinydb import TinyDB, Query
from var_ambiente import variaveis_de_ambiente
from rich.console import Console

console = Console()


def inserir_db(titulo = 'NA', numero_da_nota = 'NA', data = 'NA', horario = 'NA', tag = 'NA', paragrafos ='NA', link='NA', var_ambiente = 'NA', nome_json= 'NA'):
    dir_json = variaveis_de_ambiente(var_ambiente)
    db = TinyDB(f'{dir_json}{nome_json}', indent=4, ensure_ascii=False)
    buscar = Query()
    verificar_bd = db.contains(buscar.link==link)

    if not verificar_bd:
        db.insert({
            "titulo":titulo, 
            "numero_da_nota":numero_da_nota,
            "data":data,
            "horario":horario,
            "tag":tag,
            "paragrafos":paragrafos,
            "link":link
        })
    else:
        console.print("ja esta na base", style='#00FF6D')



def main():
    titulo = 'NA'
    numero_da_nota = 'NA'
    data = 'NA'
    horario = 'NA'
    tag = 'NA'
    paragrafos ='NA'
    link='NA'
    var_ambiente = 'DIR_BD'
    nome_json= 'NA'

    inserir_db(
        titulo = titulo, 
        numero_da_nota = numero_da_nota, 
        data = data, horario = horario, 
        tag = tag, paragrafos = paragrafos, 
        link=link, var_ambiente = var_ambiente, 
        nome_json = nome_json)



if __name__=="__main__":
    main()
