import customtkinter as ctk


class Temas:

    def __init__(self):

        self.tema_atual = "dark"

        self.cores = {

            "dark": {
                "fundo": "#101722",
                "menu": "#172334",
                "card": "#192638",
                "campo": "#263449",
                "borda": "#34465D",
                "texto": "#FFFFFF",
                "texto_secundario": "#AAB8C8",
                "destaque": "#55A7FF",
                "botao": "#1769AA",
                "botao_hover": "#2785CE",
                "excluir": "#923D4A"
            },

            "light": {
                "fundo": "#F1F4F8",
                "menu": "#FFFFFF",
                "card": "#FFFFFF",
                "campo": "#E8EDF3",
                "borda": "#D3DCE7",
                "texto": "#202B3A",
                "texto_secundario": "#68788C",
                "destaque": "#1769AA",
                "botao": "#1769AA",
                "botao_hover": "#2785CE",
                "excluir": "#C44755"
            }
        }

    def aplicar(self, tema):

        if tema not in self.cores:
            raise ValueError("Tema não encontrado.")

        self.tema_atual = tema

        if tema == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def cor(self, nome):

        return self.cores[self.tema_atual][nome]


    def configurar_tabela(self, tabela):

        from tkinter import ttk

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "Treeview",
            background=self.cor("card"),
            foreground=self.cor("texto"),
            fieldbackground=self.cor("card"),
            rowheight=35,
            borderwidth=0,
            font=("Arial", 10)
        )

        estilo.configure(
            "Treeview.Heading",
            background=self.cor("menu"),
            foreground=self.cor("texto"),
            font=("Arial", 10, "bold"),
            relief="flat"
        )

        estilo.map(
            "Treeview",
            background=[
                ("selected", self.cor("destaque"))
            ],
            foreground=[
                ("selected", "#FFFFFF")
            ]
        )

        estilo.map(
            "Treeview.Heading",
            background=[
                ("active", self.cor("destaque"))
            ],
            foreground=[
                ("active", "#FFFFFF")
            ]
        )
