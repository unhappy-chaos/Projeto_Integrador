
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
        print(f"Conectado com sucesso no {sistema}!")
        return conexao

    except pyodbc.Error as e:
        print(f"Erro ao conectar no {sistema}: {e}")
        return None


if __name__ == "__main__":
    conn = conectar_banco()

    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION();")
        print("Versão do banco:", cursor.fetchone()[0])
        conn.close()
