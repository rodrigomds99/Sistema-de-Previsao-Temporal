from screen import Screen  # Importa a classe Screen do módulo screen
from customtkinter import *  # Importa a biblioteca customtkinter para criar a interface gráfica
from tkinter import messagebox  # Importa a função messagebox da biblioteca tkinter para exibir mensagens
from database import Database  # Importa a classe Database do módulo database

# Define a classe Register que herda da classe Screen
class Register(Screen):
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
        self.title = CTkLabel(master=self.screen, text="Sistema de Cadastro", font=("Arial", 30))
        self.title.place(x=260, y=100)

        self.username = CTkLabel(master=self.screen, text="Username", font=self.text)
        self.username.place(x=250, y=170)

        self.password = CTkLabel(master=self.screen, text="Password", font=self.text)
        self.password.place(x=250, y=250)

        self.passwordConfirm = CTkLabel(master=self.screen, text="Confirm Password", font=self.text)
        self.passwordConfirm.place(x=250, y=330)

    # Método para criar os campos de entrada na interface
    def Entrys(self):
        self.usernameE = CTkEntry(master=self.screen, width=300, placeholder_text="Digite seu nome de usuário...", font=self.text)
        self.usernameE.place(x=250, y=200)

        self.passwordE = CTkEntry(master=self.screen, width=300, placeholder_text="Digite sua senha...", font=self.text, show="*")
        self.passwordE.place(x=250, y=280)

        self.passwordCE = CTkEntry(master=self.screen, width=300, placeholder_text="Confirme sua senha...", font=self.text, show="*")
        self.passwordCE.place(x=250, y=360)

    # Método para criar os checkboxes na interface
    def Checkboxs(self):
        self.check = CTkCheckBox(master=self.screen, text="Mostrar Senha", font=self.text, command=self.TogglePassword)
        self.check.place(x=250, y=410)

    # Método para criar os botões na interface
    def Buttons(self):
        self.register = CTkButton(master=self.screen, text="Cadastre-se", width=145, font=self.text, command=self.SaveUser)
        self.register.place(x=250, y=460)

        self.back = CTkButton(master=self.screen, text="Voltar", width=145, font=self.text, fg_color="green", command=self.Back)
        self.back.place(x=410, y=460)

    # Método chamado quando o botão "Voltar" é clicado
    def Back(self):
        self.screen.destroy()  # Fecha a tela atual
        from login import Login  # Importa a classe Login
        Login()  # Chama a classe Login para voltar à tela de login

    # Método chamado para alternar a visibilidade das senhas
    def TogglePassword(self):
        if self.check.get():
            self.passwordE.configure(show="")  # Mostra a senha
            self.passwordCE.configure(show="")  # Mostra a confirmação da senha
        else:
            self.passwordE.configure(show="*")  # Oculta a senha
            self.passwordCE.configure(show="*")  # Oculta a confirmação da senha

    # Método chamado quando o botão "Cadastre-se" é clicado
    def SaveUser(self):
        self.usernameCad = self.usernameE.get()  # Obtém o nome de usuário inserido
        self.passwordCad = self.passwordE.get()  # Obtém a senha inserida
        self.passwordConCad = self.passwordCE.get()  # Obtém a confirmação da senha inserida

        try:
            # Verifica se algum campo está vazio
            if self.usernameCad == "" or self.passwordCad == "" or self.passwordConCad == "":
                messagebox.showerror(title="Estado do Cadastro", message="Por favor preencha todos os campos.")
            # Verifica se o nome de usuário tem pelo menos 4 caracteres
            elif len(self.usernameCad) < 4:
                messagebox.showerror(title="Estado do Cadastro", message="Escolha um nome pelo menos 4 caracteres.")
            # Verifica se a senha tem pelo menos 4 caracteres
            elif len(self.passwordCad) < 4:
                messagebox.showerror(title="Estado do Cadastro", message="Escolha uma senha com pelo menos 4 caracteres.")
            # Verifica se as senhas são iguais
            elif self.passwordCad != self.passwordConCad:
                messagebox.showerror(title="Estado do Cadastro", message="Senhas incorretas.")
            else:
                # Verifica se o nome de usuário já existe no banco de dados
                self.sql.cursor.execute("SELECT * FROM Users WHERE Username = ?", (self.usernameCad,))
                self.verify = self.sql.cursor.fetchone()

                if self.verify:
                    messagebox.showerror(title="Estado do Cadastro", message="Usuário já existe.")
                else:
                    # Insere o novo usuário no banco de dados
                    self.sql.cursor.execute("""
                                            INSERT INTO Users (Username, Password) VALUES (?, ?)""",
                                            (self.usernameCad, self.passwordCad))
                    self.sql.conn.commit()  # Confirma a inserção no banco de dados
                    messagebox.showinfo(title="Estado do Cadastro", message="Usuário Cadastrado com Sucesso!!")
                    self.screen.destroy()  # Fecha a tela atual
                    from login import Login  # Importa a classe Login
                    Login()  # Chama a classe Login para voltar à tela de login
        except:
            # Exibe uma mensagem de erro caso ocorra uma exceção
            messagebox.showerror(title="Estado do Cadastro", message=f"Erro, por favor tente novamente.")


# Código principal para iniciar a aplicação
if __name__ == "__main__":
    Register()  # Cria uma instância da classe Register e inicia a aplicação
