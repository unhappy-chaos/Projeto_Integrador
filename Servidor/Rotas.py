from fastapi import FastAPI
import os
from Servidor.Config.Database.conexao import conectar_banco # Caminho absoluto para evitar problemas ao rodar uvicorn
app = FastAPI()

@app.get("/")
def status():
    conexao = conectar_banco()
    
    if conexao is None:
        return("Erro! Não foi possível conectar ao banco; FASTAPI ROTA GET")
    else:
        conexao.close()
        return("Servidor Rodando perfeitamente! Conexão ao banco já realizada.")


@app.get("/tabelas")
def listar_tabelas():
    conexao = conectar_banco()

    if conexao is None:
        return("Erro! Não foi possível conectar ao banco; FASTAPI ROTA GET CLIENTES")

    try:
        comando = conexao.cursor()

        comando.execute("SHOW TABLES;")

        resultados = comando.fetchall() # Pega todos resultados de qual lá tenha sido o último comando no banco

        tabelas = []

        for tabela in resultados: # Resultados é uma lista, com tuplas como items
            tabelas.append(tabela[0]) # Para cada item da lista, vamos pegar o que está dentro das tuplas com [0]

        return(tabelas)

    finally:
        conexao.close() # Independente se a consulta for bem sucedida pela rota ou não, a conexão é fechada no fim   

import os
import signal

@app.get("/kill")
def fecha_server():
    os.kill(os.getppid(), signal.SIGKILL) # Fecha para o Linux
    os._exit(0) # Fecha para o Windows
    
@app.get("/verificar")
def teste(algo):
    return("teste")