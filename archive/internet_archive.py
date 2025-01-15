#consultar arquivo json 
#salvar informações no internet archive
#atualizar json com o link do internet archive

from waybackpy import WaybackMachineSaveAPI
from dotenv import load_dotenv
from tinydb import TinyDB, Query, where
import os
from pathlib import Path

def archive_consultar_json(lista_arq_json):
    for arq_json in lista_arq_json:
        db = TinyDB(arq_json, indent=4, ensure_ascii=False)
        for consulta in db:
            link = consulta['link']
            salvar_internet_archive(link)


def salvar_internet_archive(link):
    user_agente = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    save_API = WaybackMachineSaveAPI(link, user_agente)
    link_archive = save_API.save()
    data_horario_archive_datatime = save_API.timestamp()
    print(data_horario_archive_datatime)
    

def main():
    var_env = 'DIR_BD'
    env_dir = load_dotenv('../.env_dir')
    dir_env = os.getenv(var_env)
    lista_arquivos = os.listdir(dir_env)
    lista_caminhos = []
    lista_caminhos = [os.path.join(dir_env, arquivo) for arquivo in lista_arquivos]
    # for arquivo in lista_arquivos:
    #     caminho_completo = os.path.join(dir_env, arquivo)
    #     lista_caminhos.append(caminho_completo)
    #TODO: transformar as linhas de 33 a 36 em uma compreensão de lista
    lista_caminhos = 'https://jornal.unesp.br/2024/12/02/fama-de-periodico-nao-garante-qualidade-da-ciencia/'
    # archive_consultar_json(lista_caminhos)
    salvar_internet_archive(lista_caminhos)


  

if __name__=="__main__":
    main()