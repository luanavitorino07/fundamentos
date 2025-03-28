import os
from dotenv import load_dotenv


def variaveis_de_ambiente(var_env):
    env_dir = load_dotenv('../.env_dir')
    dir_env = os.getenv(var_env)
    print(f'dir_env: {dir_env}')
    return dir_env

def main():
    var_env = 'DIR_BD'
    variaveis_de_ambiente(var_env)


if __name__=="__main__":
    main()
