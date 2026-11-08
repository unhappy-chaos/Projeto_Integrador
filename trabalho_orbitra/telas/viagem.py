import customtkinter as ctk
from tkinter import ttk, messagebox

from seguranca import (
    validar_campos, validar_data,
    confirmar_exclusao, registrar_log
)
from componentes.botoes import BotaoAcao


class TelaViagem(ctk.CTkFrame):

    def __init__(self, master, temas):

        super().__init__(master, fg_color=temas.cor("fundo"))

        self.temas = temas
        self.registros = []
        self.selecionado = None

        self.criar_interface()

    def criar_interface(self):

        ctk.CTkLabel(
            self, text="Viagens",
            font=("Arial", 27, "bold"),
            text_color=self.temas.cor("texto")
        ).pack(anchor="w", padx=30, pady=25)

        form = ctk.CTkFrame(
            self, fg_color=self.temas.cor("card"),
            corner_radius=12
        )
        form.pack(fill="x", padx=30)

        nomes = [
            "Motorista",
            "Veículo",
            "Rota",
            "Data da Viagem"
        ]

        self.campos = {}

        for i, nome in enumerate(nomes):

            box = ctk.CTkFrame(form, fg_color="transparent")
            box.grid(row=0, column=i, padx=10, pady=15, sticky="ew")
            form.grid_columnconfigure(i, weight=1)

            ctk.CTkLabel(
                box, text=nome,
                text_color=self.temas.cor("texto_secundario")
            ).pack(anchor="w")

            if nome != "Data da Viagem":

                campo = ctk.CTkComboBox(
                    box,
                    values=[],
                    fg_color=self.temas.cor("campo")
                )

            else:

                campo = ctk.CTkEntry(
                    box,
                    placeholder_text="DD/MM/AAAA",
                    fg_color=self.temas.cor("campo")
                )

            campo.pack(fill="x", pady=5)
            self.campos[nome] = campo

        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(anchor="w", padx=30, pady=15)

        BotaoAcao(botoes, "Cadastrar", self.cadastrar, self.temas).pack(side="left", padx=5)
        BotaoAcao(botoes, "Editar", self.editar, self.temas, "secundario").pack(side="left", padx=5)
        BotaoAcao(botoes, "Excluir", self.excluir, self.temas, "excluir").pack(side="left", padx=5)
        BotaoAcao(botoes, "Limpar", self.limpar, self.temas, "secundario").pack(side="left", padx=5)

        self.tabela = ttk.Treeview(
            self, columns=nomes, show="headings"
        )
        self.temas.configurar_tabela(self.tabela)
        for nome in nomes:
            self.tabela.heading(nome, text=nome)
            self.tabela.column(nome, width=180)

        self.tabela.pack(fill="both", expand=True, padx=30, pady=15)
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar)

    def ler_campos(self):

        return {
            nome: campo.get().strip()
            for nome, campo in self.campos.items()
        }

    def atualizar_tabela(self):

        self.tabela.delete(*self.tabela.get_children())

        for i, registro in enumerate(self.registros):
            self.tabela.insert(
                "", "end", iid=str(i),
                values=list(registro.values())
            )

    def validar(self, registro):

        if not validar_campos(registro):
            return False

        if not validar_data(registro["Data da Viagem"]):

            messagebox.showwarning(
                "Data inválida",
                "Utilize o formato DD/MM/AAAA."
            )

            return False

        return True

    def cadastrar(self):

        registro = self.ler_campos()

        if not self.validar(registro):
            return

        self.registros.append(registro)
        registrar_log("Viagem cadastrada.")
        self.atualizar_tabela()
        self.limpar()

    def selecionar(self, evento=None):

        selecionados = self.tabela.selection()

        if not selecionados:
            return

        self.selecionado = int(selecionados[0])
        registro = self.registros[self.selecionado]

        for nome, campo in self.campos.items():
            campo.set(registro[nome])

    def editar(self):

        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Selecione uma viagem.")
            return

        registro = self.ler_campos()

        if not self.validar(registro):
            return

        self.registros[self.selecionado] = registro
        registrar_log("Viagem editada.")
        self.atualizar_tabela()
        self.limpar()

    def excluir(self):

        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Selecione uma viagem.")
            return

        if confirmar_exclusao():
            del self.registros[self.selecionado]
            registrar_log("Viagem excluída.")
            self.atualizar_tabela()
            self.limpar()

    def limpar(self):

        for campo in self.campos.values():
            campo.set("")

        self.selecionado = None
        self.tabela.selection_remove(self.tabela.selection())