from customtkinter import *  # Importa a biblioteca customtkinter para criar a interface gráfica
from register import Register  # Importa a classe Register do módulo register
from screen import Screen  # Importa a classe Screen do módulo screen
from database import Database  # Importa a classe Database do módulo database
from tkinter import messagebox  # Importa a função messagebox da biblioteca tkinter para exibir mensagens

# Define a classe Login que herda da classe Screen
class Login(Screen):
    def __init__(self):
        super().__init__()  # Chama o construtor da classe pai
        self.text = ("Arial", 20)  # Define a fonte e tamanho do texto
        self.Labels()  # Chama o método para criar os labels
        self.Entrys()  # Chama o método para criar os campos de entrada
        self.Checkboxs()  # Chama o método para criar os checkboxes
        self.Buttons()  # Chama o método para criar os botões

        self.sql = Database()  # Cria uma instância da classe Database para interagir com o banco de dados
        self.run()  # Chama o método para iniciar a interface

    # Método para criar os labels na interface
    def Labels(self):
        self.title = CTkLabel(master=self.screen, text="Sistema de Login", font=("Arial", 30))
        self.title.place(x=275, y=100)

        self.username = CTkLabel(master=self.screen, text="Username", font=self.text)
        self.username.place(x=250, y=170)

        self.password = CTkLabel(master=self.screen, text="Password", font=self.text)
        self.password.place(x=250, y=250)

    # Método para criar os campos de entrada na interface
    def Entrys(self):
        self.usernameE = CTkEntry(master=self.screen, width=300, placeholder_text="Digite seu nome de usuário...", font=self.text)
        self.usernameE.place(x=250, y=200)

        self.passwordE = CTkEntry(master=self.screen, width=300, placeholder_text="Digite sua senha...", font=self.text, show="*")
        self.passwordE.place(x=250, y=280)

    # Método para criar os checkboxes na interface
    def Checkboxs(self):
        self.check = CTkCheckBox(master=self.screen, text="Mostrar Senha", font=self.text, command=self.TogglePassword)
        self.check.place(x=250, y=350)

    # Método para criar os botões na interface
    def Buttons(self):
        self.login = CTkButton(master=self.screen, text="Fazer Login", width=300, font=self.text, command=self.Logged)
        self.login.place(x=250, y=400)

        self.register = CTkButton(master=self.screen, text="Cadastre-se", width=300, font=self.text, command=self.Register)
        self.register.place(x=250, y=450)

    # Método chamado quando o botão "Cadastre-se" é clicado
    def Register(self):
        self.screen.destroy()  # Fecha a tela atual
        Register()  # Chama a classe Register para abrir a tela de cadastro

    # Método chamado para alternar a visibilidade da senha
    def TogglePassword(self):
        if self.check.get():
            self.passwordE.configure(show="")  # Mostra a senha
        else:
            self.passwordE.configure(show="*")  # Oculta a senha

    # Método chamado quando o botão "Fazer Login" é clicado
    def Logged(self):
        self.usernameCad = self.usernameE.get()  # Obtém o nome de usuário inserido
        self.passwordCad = self.passwordE.get()  # Obtém a senha inserida

        # Executa uma consulta SQL para verificar se o usuário e a senha estão corretos
        self.sql.cursor.execute("""
            SELECT * FROM Users WHERE Username = ? AND Password = ?""", (self.usernameCad, self.passwordCad))

        self.verify = self.sql.cursor.fetchone()  # Obtém o resultado da consulta

        try:
            # Verifica se os campos estão vazios
            if self.usernameCad == "" or self.passwordCad == "":
                messagebox.showerror(title="Estado do Login", message="Por favor preencha todos os campos.")

            # Verifica se o usuário ou senha estão incorretos
            elif self.verify is None:
                messagebox.showerror(title="Estado do Login", message="Usuário ou senha incorretos.")

            # Verifica se o usuário e a senha estão corretos
            elif (self.usernameCad in self.verify and self.passwordCad in self.verify):
                messagebox.showinfo(title="Estado do Login", message="Usuário Logado com Sucesso!!")
                self.screen.destroy()  # Fecha a tela atual
                from weather import Weather  # Importa a classe Weather
                Weather()  # Chama a classe Weather para abrir a tela de previsão do tempo
        except:
            # Exibe uma mensagem de erro caso ocorra uma exceção
            messagebox.showerror(title="Estado do Login", message=f"Erro, por favor tente novamente.")


# Código principal para iniciar a aplicação
if __name__ == "__main__":
    Login()  # Cria uma instância da classe Login e inicia a aplicação
