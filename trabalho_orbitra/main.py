import customtkinter as ctk

from telas.inicio import TelaInicio
from telas.motorista import TelaMotorista
from telas.veiculo import TelaVeiculo
from telas.cidade import TelaCidade
from telas.rota import TelaRota
from telas.viagem import TelaViagem
from telas.abastecimento import TelaAbastecimento

from componentes.temas import Temas
from componentes.botoes import BotaoMenu


class Orbitra(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("ORBITRA - Gestão de Frota")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        self.temas = Temas()
        self.temas.aplicar("dark")

        self.configure(fg_color=self.temas.cor("fundo"))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_menu()
        self.criar_area_principal()

        self.abrir_tela("Início")

    # MENU LATERAL

    def criar_menu(self):

        self.menu = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color=self.temas.cor("menu")
        )

        self.menu.grid(row=0, column=0, sticky="nsew")
        self.menu.grid_propagate(False)

        ctk.CTkLabel(
            self.menu,
            text="ORBITRA",
            font=("Arial", 28, "bold"),
            text_color=self.temas.cor("destaque")
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self.menu,
            text="Gestão de Frota",
            font=("Arial", 13),
            text_color=self.temas.cor("texto_secundario")
        ).pack(pady=(0, 30))

        opcoes = [
            "Início",
            "Motoristas",
            "Veículos",
            "Cidades",
            "Rotas",
            "Viagens",
            "Abastecimentos"
        ]

        self.botoes_menu = []

        for nome in opcoes:

            botao = BotaoMenu(
                self.menu,
                texto=nome,
                comando=lambda n=nome: self.abrir_tela(n),
                temas=self.temas
            )

            botao.pack(fill="x", padx=15, pady=5)

            self.botoes_menu.append(botao)

        ctk.CTkFrame(
            self.menu,
            fg_color="transparent"
        ).pack(expand=True)

        BotaoMenu(
            self.menu,
            texto="Sair",
            comando=self.destroy,
            temas=self.temas
        ).pack(fill="x", padx=15, pady=20)

    # ÁREA PRINCIPAL

    def criar_area_principal(self):

        self.area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=self.temas.cor("fundo")
        )

        self.area.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.area.grid_columnconfigure(0, weight=1)
        self.area.grid_rowconfigure(0, weight=1)

    # NAVEGAÇÃO

    def abrir_tela(self, nome):

        for widget in self.area.winfo_children():
            widget.destroy()

        telas = {
            "Início": TelaInicio,
            "Motoristas": TelaMotorista,
            "Veículos": TelaVeiculo,
            "Cidades": TelaCidade,
            "Rotas": TelaRota,
            "Viagens": TelaViagem,
            "Abastecimentos": TelaAbastecimento
        }

        tela = telas[nome](
            self.area,
            self.temas
        )

        tela.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # ALTERAÇÃO DE TEMA

    def alternar_tema(self):

        novo_tema = (
            "light"
            if self.temas.tema_atual == "dark"
            else "dark"
        )

        self.temas.aplicar(novo_tema)

        self.destroy()

        nova_janela = Orbitra()
        nova_janela.mainloop()


if __name__ == "__main__":

    app = Orbitra()
    app.mainloop()