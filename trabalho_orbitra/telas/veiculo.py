import customtkinter as ctk
from tkinter import ttk, messagebox

from seguranca import (
    validar_campos, verificar_duplicado,
    confirmar_exclusao, registrar_log, registrar_erro
)
from componentes.botoes import BotaoAcao


class TelaVeiculo(ctk.CTkFrame):

    def __init__(self, master, temas):

        super().__init__(master, fg_color=temas.cor("fundo"))

        self.temas = temas
        self.registros = []
        self.selecionado = None

        self.criar_interface()

    def criar_interface(self):

        ctk.CTkLabel(
            self, text="Veículos",
            font=("Arial", 27, "bold"),
            text_color=self.temas.cor("texto")
        ).pack(anchor="w", padx=30, pady=25)

        form = ctk.CTkFrame(
            self, fg_color=self.temas.cor("card"),
            corner_radius=12
        )
        form.pack(fill="x", padx=30)

        nomes = [
            "Placa", "Marca", "Modelo",
            "Ano", "Tipo", "Quilometragem"
        ]

        self.campos = {}

        for i, nome in enumerate(nomes):

            box = ctk.CTkFrame(form, fg_color="transparent")
            box.grid(row=i//3, column=i%3, padx=12, pady=12, sticky="ew")
            form.grid_columnconfigure(i%3, weight=1)

            ctk.CTkLabel(
                box, text=nome,
                text_color=self.temas.cor("texto_secundario")
            ).pack(anchor="w")

            entrada = ctk.CTkEntry(
                box,
                placeholder_text=f"Digite {nome}",
                fg_color=self.temas.cor("campo")
            )
            entrada.pack(fill="x", pady=5)
            self.campos[nome] = entrada

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
            self.tabela.column(nome, width=140)

        self.tabela.pack(fill="both", expand=True, padx=30, pady=15)
        self.tabela.bind("<<TreeviewSelect>>", self.selecionar)

    def ler_campos(self):
        return {n: c.get().strip() for n, c in self.campos.items()}

    def atualizar_tabela(self):

        self.tabela.delete(*self.tabela.get_children())

        for i, registro in enumerate(self.registros):
            self.tabela.insert(
                "", "end", iid=str(i),
                values=list(registro.values())
            )

    def cadastrar(self):

        registro = self.ler_campos()

        if not validar_campos(registro):
            return

        if verificar_duplicado(self.registros, "Placa", registro["Placa"]):
            messagebox.showwarning("Duplicidade", "Esta placa já está cadastrada.")
            return

        try:
            self.registros.append(registro)
            registrar_log("Veículo cadastrado.")
            self.atualizar_tabela()
            self.limpar()
            messagebox.showinfo("Sucesso", "Veículo cadastrado.")
        except Exception:
            registrar_erro()

    def selecionar(self, evento=None):

        selecionados = self.tabela.selection()

        if not selecionados:
            return

        self.selecionado = int(selecionados[0])
        registro = self.registros[self.selecionado]

        for nome, campo in self.campos.items():
            campo.delete(0, "end")
            campo.insert(0, registro[nome])

    def editar(self):

        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Selecione um veículo.")
            return

        registro = self.ler_campos()

        if not validar_campos(registro):
            return

        if verificar_duplicado(
            self.registros, "Placa", registro["Placa"],
            ignorar=self.selecionado
        ):
            messagebox.showwarning("Duplicidade", "Esta placa já está cadastrada.")
            return

        self.registros[self.selecionado] = registro
        registrar_log("Veículo editado.")
        self.atualizar_tabela()
        self.limpar()

    def excluir(self):

        if self.selecionado is None:
            messagebox.showwarning("Atenção", "Selecione um veículo.")
            return

        if confirmar_exclusao():
            del self.registros[self.selecionado]
            registrar_log("Veículo excluído.")
            self.atualizar_tabela()
            self.limpar()

    def limpar(self):

        for campo in self.campos.values():
            campo.delete(0, "end")

        self.selecionado = None
        self.tabela.selection_remove(self.tabela.selection())