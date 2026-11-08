import customtkinter as ctk


class TelaInicio(ctk.CTkFrame):

    def __init__(self, master, temas):

        super().__init__(
            master,
            fg_color=temas.cor("fundo")
        )

        self.temas = temas

        self.criar_interface()

    def criar_interface(self):

        ctk.CTkLabel(
            self,
            text="Bem-vindo ao ORBITRA",
            font=("Arial", 28, "bold"),
            text_color=self.temas.cor("texto")
        ).pack(anchor="w", padx=30, pady=(35, 5))

        ctk.CTkLabel(
            self,
            text="Sistema de Gestão de Frota",
            font=("Arial", 14),
            text_color=self.temas.cor("texto_secundario")
        ).pack(anchor="w", padx=30, pady=(0, 30))

        resumo = ctk.CTkFrame(
            self,
            fg_color=self.temas.cor("card"),
            corner_radius=12
        )

        resumo.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(
            resumo,
            text="Painel de controle",
            font=("Arial", 20, "bold"),
            text_color=self.temas.cor("texto")
        ).pack(anchor="w", padx=20, pady=20)

        ctk.CTkLabel(
            resumo,
            text="Acompanhe e gerencie as informações da sua frota.",
            font=("Arial", 14),
            text_color=self.temas.cor("texto_secundario")
        ).pack(anchor="w", padx=20, pady=(0, 20))

        indicadores = [
            "Motoristas",
            "Veículos",
            "Cidades",
            "Rotas",
            "Viagens"
        ]

        area_cards = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        area_cards.pack(fill="x", padx=20, pady=20)

        for nome in indicadores:

            card = ctk.CTkFrame(
                area_cards,
                fg_color=self.temas.cor("card"),
                corner_radius=12
            )

            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=7,
                pady=5
            )

            ctk.CTkLabel(
                card,
                text=nome,
                font=("Arial", 13),
                text_color=self.temas.cor("texto_secundario")
            ).pack(pady=(20, 5))

            ctk.CTkLabel(
                card,
                text="0",
                font=("Arial", 30, "bold"),
                text_color=self.temas.cor("destaque")
            ).pack(pady=(0, 20))