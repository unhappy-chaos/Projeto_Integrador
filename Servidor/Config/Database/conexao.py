
import platform
import pyodbc
import os
from pathlib import Path

CONFIG = Path(__file__).resolve().parent.parent # Busca a pasta Config e salva em uma váriavel de ambiente

def conectar_banco():

    sistema = platform.system() #Aponta qual sistema está sendo utilizado

    if sistema == "Linux": # Se for linux ele vai usar a váriavel de ambiente para apontar a pasta e arquivo de configuração que o unixODBC quer usar

        linux = CONFIG / "Linux" # Da pasta Config vamos para a pasta Linux

        os.environ["ODBCSYSINI"] = str(linux) # Aponta qual driver ODBC vai ser utilizado pelo unixODBC
        os.environ["ODBCINI"] = str(linux / "odbc.ini") # Aponta os parâmetros da conexão o unixODBC vai usar

        string_conexao = (
            "DSN=ORBITRA;"
            "UID=root;"
            "PWD=RafinhaGames27072312@;"
        )

    elif sistema == "Windows":

        string_conexao = (
            "DRIVER={MySQL ODBC 9.1 Unicode Driver};"
            "SERVER=localhost;"
            "PORT=3306;"
            "DATABASE=ORBITRA;"
            "UID=root;"
            "PWD=RafinhaGames27072312@;"
        )

    else:
        raise OSError(f"Sistema operacional {sistema} não suportado.")

    try:
        conexao = pyodbc.connect(string_conexao)
        print(f"{sistema} conectado com sucesso ao banco!")
        return conexao

    except pyodbc.Error as erro_conexao:
        print(f"Erro ao conectar no {sistema}: {erro_conexao}")
        return None



# Bloco de teste
if __file__ == "__conexao__": # Esse código só vai rodar se você ativar ele aqui no arquivo
    conn = conectar_banco() # Rodando a função e pegando o resultado dela, nessa de rodar a função ele se conecta ao banco

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();") # Roda isso aqui dentro do banco aparentemente
        print("Versão do banco:", cursor.fetchone()[0]) # pq tem uma função com [0]?
        conn.close() # Fecha a conexão após utilizar ela para algo, bem importante
