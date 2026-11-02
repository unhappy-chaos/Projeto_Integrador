import uvicorn

if __name__ == "__main__": # inicia o uvicorn somente se você chamar esse arquivo diretamente
    uvicorn.run(
        "Servidor.Rotas:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )