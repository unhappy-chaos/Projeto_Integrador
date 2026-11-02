# Pela verificação é onde criaremos o código que vai verificar o Login, se o login der certo iniciamos o uvicorn escutando a nossas rotas
import uvicorn
def verificar(login):
    pass
    if login == "deu certo":
        uvicorn.run("Servidor.Rotas:app", host = "127.0.0.1", port = 8000, reload = True)
        return("Algo aqui pera")