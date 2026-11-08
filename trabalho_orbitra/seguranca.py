import re
import logging

from datetime import datetime
from tkinter import messagebox


logging.basicConfig(
    filename="orbitra.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# CAMPOS OBRIGATÓRIOS

def validar_campos(registro):

    for campo, valor in registro.items():

        if not str(valor).strip():

            messagebox.showwarning(
                "Atenção",
                f"O campo {campo} é obrigatório."
            )

            return False

    return True


# CPF

def validar_cpf(cpf):

    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    for tamanho in (9, 10):

        soma = sum(
            int(cpf[i]) * (tamanho + 1 - i)
            for i in range(tamanho)
        )

        digito = (soma * 10 % 11) % 10

        if digito != int(cpf[tamanho]):
            return False

    return True


# E-MAIL

def validar_email(email):

    padrao = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

    return bool(re.match(padrao, email))


# DATA

def validar_data(data):

    try:

        datetime.strptime(data, "%d/%m/%Y")

        return True

    except ValueError:

        return False


# REGISTROS DUPLICADOS

def verificar_duplicado(registros, campo, valor, ignorar=None):

    for indice, registro in enumerate(registros):

        if indice == ignorar:
            continue

        if str(registro.get(campo, "")).strip().casefold() == str(valor).strip().casefold():
            return True

    return False


# CONFIRMAR EXCLUSÃO

def confirmar_exclusao():

    return messagebox.askyesno(
        "Confirmar exclusão",
        "Deseja realmente excluir este registro?"
    )


# LOGS

def registrar_log(mensagem):

    logging.info(mensagem)


# TRATAMENTO DE ERROS

def registrar_erro():

    logging.exception("Ocorreu um erro na aplicação.")

    messagebox.showerror(
        "Erro",
        "Não foi possível realizar a operação."
    )