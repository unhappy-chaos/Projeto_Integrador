import customtkinter as ctk


class BotaoMenu(ctk.CTkButton):

    def __init__(
        self,
        master,
        texto,
        comando,
        temas
    ):

        super().__init__(
            master,

            text=texto,

            command=comando,

            height=42,

            corner_radius=8,

            anchor="w",

            font=("Arial", 14),

            fg_color="transparent",

            hover_color=temas.cor("campo"),

            text_color=temas.cor("texto")
        )


class BotaoAcao(ctk.CTkButton):

    def __init__(
        self,
        master,
        texto,
        comando,
        temas,
        tipo="normal"
    ):

        cores = {
            "normal": temas.cor("botao"),
            "excluir": temas.cor("excluir"),
            "secundario": temas.cor("campo")
        }

        cor = cores.get(tipo, temas.cor("botao"))

        super().__init__(
            master,

            text=texto,

            command=comando,

            width=110,

            height=36,

            corner_radius=8,

            font=("Arial", 13, "bold"),

            fg_color=cor,

            hover_color=temas.cor("botao_hover"),

            text_color=temas.cor("texto")
        )