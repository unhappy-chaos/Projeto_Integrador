import customtkinter as ctk

from tkinter import ttk, messagebox

from seguranca import (
    validar_campos,
    validar_cpf,
    validar_email,
    verificar_duplicado,
    confirmar_exclusao,
    registrar_log,
    registrar_erro
)

from componentes.botoes import BotaoAcao


class TelaMotorista(ctk.CTkFrame):

    def __init__(self, master, temas):

        super().__init__(
            master,
            fg_color=temas.cor("fundo")
        )

        self.temas = temas
        self.registros = []
        self.selecionado = None

        self.criar_interface()
        self.atualizar_tabela()

    def criar_interface(self):

        ctk.CTkLabel(
            self,
            text="Motoristas",
            font=("Arial", 27, "bold"),
            text_color=self.temas.cor("texto")
        ).pack(anchor="w", padx=30, pady=25)

        self.formulario = ctk.CTkFrame(
            self,
            fg_color=self.temas.cor("card"),
            corner_radius=12
        )

        self.formulario.pack(fill="x", padx=30, pady=5)

        nomes = [
            "Nome",
            "CPF",
            "CNH",
            "Categoria CNH",
            "Telefone",
            "Email"
        ]

        self.campos = {}

        for i, nome in enumerate(nomes):

            linha = i // 3
            coluna = i % 3

            campo = ctk.CTkFrame(
                self.formulario,
                fg_color="transparent"
            )

            campo.grid(
                row=linha,
                column=coluna,
                padx=12,
                pady=12,
                sticky="ew"
            )

            self.formulario.grid_columnconfigure(
                coluna,
                weight=1
            )

            ctk.CTkLabel(
                campo,
                text=nome,
                text_color=self.temas.cor("texto_secundario")
            ).pack(anchor="w")

            entrada = ctk.CTkEntry(
                campo,
                placeholder_text=f"Digite {nome}",
                fg_color=self.temas.cor("campo"),
                border_color=self.temas.cor("borda"),
                text_color=self.temas.cor("texto")
            )

            entrada.pack(fill="x", pady=5)

            self.campos[nome] = entrada

        botoes = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        botoes.pack(anchor="w", padx=30, pady=15)

        BotaoAcao(
            botoes, "Cadastrar", self.cadastrar,
            self.temas
        ).pack(side="left", padx=5)

        BotaoAcao(
            botoes, "Editar", self.editar,
            self.temas, "secundario"
        ).pack(side="left", padx=5)

        BotaoAcao(
            botoes, "Excluir", self.excluir,
            self.temas, "excluir"
        ).pack(side="left", padx=5)

        BotaoAcao(
            botoes, "Limpar", self.limpar,
            self.temas, "secundario"
        ).pack(side="left", padx=5)

        self.tabela = ttk.Treeview(
            self,
            columns=(
                "Nome", "CPF", "CNH",
                "Categoria CNH", "Telefone", "teste"
            ),
            show="headings"
        )

        self.temas.configurar_tabela(self.tabela)

        for coluna in self.tabela["columns"]:

            self.tabela.heading(
                coluna,
                text=coluna
            )

            self.tabela.column(
                coluna,
                width=140
            )

        self.tabela.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        self.tabela.bind(
            "<<TreeviewSelect>>",
            self.selecionar
        )

    def ler_campos(self):

        return {
            nome: campo.get().strip()
            for nome, campo in self.campos.items()
        }

    def cadastrar(self):

        registro = self.ler_campos()

        if not validar_campos(registro):
            return

        if not validar_cpf(registro["CPF"]):

            messagebox.showwarning(
                "CPF inválido",
                "Informe um CPF válido."
            )

            return

        if not validar_email(registro["Email"]):

            messagebox.showwarning(
                "E-mail inválido",
                "Informe um e-mail válido."
            )

            return

        if verificar_duplicado(
            self.registros,
            "CPF",
            registro["CPF"]
        ):

            messagebox.showwarning(
                "Duplicidade",
                "Este CPF já está cadastrado."
            )

            return

        try:

            self.registros.append(registro)

            registrar_log("Motorista cadastrado.")

            self.atualizar_tabela()
            self.limpar()

            messagebox.showinfo(
                "Sucesso",
                "Motorista cadastrado."
            )

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

            campo.insert(
                0,
                registro[nome]
            )

    def editar(self):

        if self.selecionado is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um motorista."
            )

            return

        registro = self.ler_campos()

        if not validar_campos(registro):
            return

        if not validar_cpf(registro["CPF"]):

            messagebox.showwarning(
                "CPF inválido",
                "Informe um CPF válido."
            )

            return

        if not validar_email(registro["Email"]):

            messagebox.showwarning(
                "E-mail inválido",
                "Informe um e-mail válido."
            )

            return

        if verificar_duplicado(
            self.registros,
            "CPF",
            registro["CPF"],
            ignorar=self.selecionado
        ):

            messagebox.showwarning(
                "Duplicidade",
                "Este CPF já está cadastrado."
            )

            return

        self.registros[self.selecionado] = registro

        registrar_log("Motorista editado.")

        self.atualizar_tabela()
        self.limpar()

        messagebox.showinfo(
            "Sucesso",
            "Motorista atualizado."
        )

    def excluir(self):

        if self.selecionado is None:

            messagebox.showwarning(
                "Atenção",
                "Selecione um motorista."
            )

            return

        if confirmar_exclusao():

            del self.registros[self.selecionado]

            registrar_log("Motorista excluído.")

            self.atualizar_tabela()
            self.limpar()

    def limpar(self):

        for campo in self.campos.values():
            campo.delete(0, "end")

        self.selecionado = None

        self.tabela.selection_remove(
            self.tabela.selection()
        )

    def atualizar_tabela(self):

        self.tabela.delete(
            *self.tabela.get_children()
        )

        for indice, registro in enumerate(self.registros):

            self.tabela.insert(
                "",
                "end",
                iid=str(indice),
                values=list(registro.values())
            )