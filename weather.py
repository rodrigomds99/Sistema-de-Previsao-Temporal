import requests  # Importa a biblioteca requests para fazer requisições HTTP
from customtkinter import *  # Importa a biblioteca customtkinter para criar a interface gráfica
from tkinter import messagebox  # Importa a função messagebox da biblioteca tkinter para exibir mensagens
from datetime import datetime  # Importa a classe datetime da biblioteca datetime para trabalhar com datas e horários
from screen import Screen  # Importa a classe Screen do módulo screen
import os  # Importa a biblioteca os para interagir com o sistema operacional


# Define a classe Weather que herda da classe Screen
class Weather(Screen):
    def __init__(self):
        super().__init__()  # Chama o construtor da classe pai

        self.key = "fc9f5ef49b8128228586adbe1e77b31f"  # Chave de API para acessar o OpenWeatherMap
        self.Labels()  # Chama o método para criar os labels
        self.Entrys()  # Chama o método para criar os campos de entrada
        self.Buttons()  # Chama o método para criar os botões

        self.run()  # Chama o método para iniciar a interface

    # Método para criar os labels na interface
    def Labels(self):
        self.title = CTkLabel(master=self.screen, text="Previsão do Tempo", font=("Arial", 30))
        self.title.place(x=265, y=100)

        self.city = CTkLabel(master=self.screen, text="Cidade", font=self.text)
        self.city.place(x=250, y=170)

        self.dateI = CTkLabel(master=self.screen, text="Data Inicial", font=self.text)
        self.dateI.place(x=250, y=250)

        self.dateF = CTkLabel(master=self.screen, text="Data Final", font=self.text)
        self.dateF.place(x=250, y=330)

    # Método para criar os campos de entrada na interface
    def Entrys(self):
        self.cityE = CTkEntry(master=self.screen, placeholder_text="Digite uma cidade...", width=300, font=self.text)
        self.cityE.place(x=250, y=200)

        # Cria o campo para a data inicial com formatação
        self.dateI_var = StringVar()
        self.dateFormateI = DateFormater(self.dateI_var, None)  # Inicializa sem entry no momento
        self.dateI_var.trace("w", lambda name, index, mode, sv=self.dateI_var: self.dateFormateI.FormateDate())
        self.dateIE = CTkEntry(master=self.screen, placeholder_text="Digite a Data Inicial...",
                               textvariable=self.dateI_var, width=300, font=self.text)
        self.dateIE.place(x=250, y=280)
        self.dateFormateI.entry = self.dateIE  # Atribui a entry após criação

        # Cria o campo para a data final com formatação
        self.dateF_var = StringVar()
        self.dateFormateF = DateFormater(self.dateF_var, None)  # Inicializa sem entry no momento
        self.dateF_var.trace("w", lambda name, index, mode, sv=self.dateF_var: self.dateFormateF.FormateDate())
        self.dateFE = CTkEntry(master=self.screen, placeholder_text="Digite a Data Final...",
                               textvariable=self.dateF_var, width=300, font=self.text)
        self.dateFE.place(x=250, y=360)
        self.dateFormateF.entry = self.dateFE  # Atribui a entry após criação

        # Configura a data inicial como a data atual e desabilita o campo
        self.today = datetime.now().strftime("%d/%m/%Y")
        self.dateI_var.set(self.today)
        self.dateIE.configure(state="disabled")

    # Método para criar os botões na interface
    def Buttons(self):
        self.file = CTkButton(master=self.screen, text="Gerar Arquivo", width=300, font=self.text, command=self.Link)
        self.file.place(x=250, y=410)

        self.back = CTkButton(master=self.screen, text="Voltar", width=300, fg_color="green", font=self.text,
                              command=self.Back)
        self.back.place(x=250, y=450)

    # Método chamado quando o botão "Gerar Arquivo" é clicado
    def Link(self):
        self.city = self.cityE.get()
        self.dateI = self.dateIE.get()
        self.dateF = self.dateFE.get()

        # Verifica se algum campo está vazio
        if self.city == "" or self.dateI == "" or self.dateF == "":
            messagebox.showerror(title="Erro", message="Por favor preencha todos os campos.")
        else:
            try:
                # Valida e formata as datas
                self.dateI = self.dateFormateI.ValidateDate(self.dateI)
                self.dateF = self.dateFormateF.ValidateDate(self.dateF)

                # Verifica se a data inicial é a data atual
                if self.dateI != datetime.now().strftime("%d/%m/%Y"):
                    raise ValueError("A data inicial deve ser a data atual.")

                # Calcula a diferença entre as datas
                self.dateI_obj = datetime.strptime(self.dateI, "%d/%m/%Y")
                self.dateF_obj = datetime.strptime(self.dateF, "%d/%m/%Y")
                self.dateDiff = (self.dateF_obj - self.dateI_obj).days

                # Verifica se a diferença entre as datas é válida (entre 1 e 5 dias)
                if self.dateDiff < 0 or self.dateDiff > 5:
                    raise ValueError("A diferença entre a data inicial e a data final deve ser entre 1 e 5 dias.")

                # Faz a requisição para obter a previsão futura
                self.futureLink = f"https://api.openweathermap.org/data/2.5/forecast?q={self.city}&appid={self.key}&lang=pt_br"
                self.futureRequest = requests.get(self.futureLink)
                self.futureData = self.futureRequest.json()

                # Verifica se a cidade é válida
                if self.futureData.get("cod") != "200":
                    raise ValueError("Cidade inválida. Por favor, digite uma cidade válida.")

                # Faz a requisição para obter os dados atuais
                self.currentLink = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.key}&lang=pt_br"
                self.currentRequest = requests.get(self.currentLink)
                self.currentData = self.currentRequest.json()

                # Define o caminho para a pasta "Arquivos-Prova2" na área de trabalho
                self.path = os.path.join(os.path.expanduser("~"), "Área de Trabalho")
                self.folderPath = os.path.join(self.path, "Arquivos-Prova2")
                os.makedirs(self.folderPath, exist_ok=True)

                self.filePath = os.path.join(self.folderPath, f"{self.city}_clima.txt")

                # Cria e escreve no arquivo com os dados climáticos
                with open(self.filePath, "w", encoding="utf-8") as file:
                    file.write(f"Dados Climáticos da cidade '{self.city}'\n\n")

                    # Escreve os dados atuais no arquivo
                    current_weather = self.currentData["weather"][0]["description"]
                    current_temperature = self.currentData["main"]["temp"] - 273.15
                    current_temp_max = self.currentData["main"]["temp_max"] - 273.15
                    current_temp_min = self.currentData["main"]["temp_min"] - 273.15
                    current_feels = self.currentData["main"]["feels_like"] - 273.15

                    file.write("Dados Atuais:\n")
                    file.write(f"Clima Atual: {current_weather}\n")
                    file.write(f"Temperatura Atual: {current_temperature:.0f}ºC\n")
                    file.write(f"Temperatura Máxima Atual: {current_temp_max:.0f}ºC\n")
                    file.write(f"Temperatura Mínima Atual: {current_temp_min:.0f}ºC\n")
                    file.write(f"Sensação Térmica Atual: {current_feels:.0f}ºC\n\n")

                    # Escreve a previsão futura no arquivo, até a data final
                    for i in range(0, len(self.futureData["list"]), 8):
                        previsao = self.futureData["list"][i]
                        data_hora_str = previsao["dt_txt"]
                        data_hora_obj = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M:%S")

                        if data_hora_obj.date() > self.dateF_obj.date():
                            break

                        data_hora_formatada = data_hora_obj.strftime("%d/%m/%Y %H:%M")

                        clima = previsao["weather"][0]["description"]
                        temperatura = previsao["main"]["temp"] - 273.15
                        temperatura_max = previsao["main"]["temp_max"] - 273.15
                        temperatura_min = previsao["main"]["temp_min"] - 273.15
                        sensacao = previsao["main"]["feels_like"] - 273.15

                        file.write(f"Previsão para {data_hora_formatada}\n")
                        file.write(f"Clima: {clima}\n")
                        file.write(f"Temperatura: {temperatura:.0f}ºC\n")
                        file.write(f"Temperatura Máxima: {temperatura_max:.0f}ºC\n")
                        file.write(f"Temperatura Mínima: {temperatura_min:.0f}ºC\n")
                        file.write(f"Sensação Térmica: {sensacao:.0f}ºC\n\n")

                # Exibe mensagem de sucesso
                messagebox.showinfo(title="Sucesso", message="Arquivo gerado com sucesso!")

            # Trata erros e exibe mensagem de erro
            except Exception as e:
                messagebox.showerror(title="Erro", message=f"Por favor, tente novamente. Erro: {str(e)}")

    # Método chamado quando o botão "Voltar" é clicado
    def Back(self):
        self.screen.destroy()  # Fecha a tela atual
        from login import Login  # Importa a classe Login
        Login()  # Chama a classe Login para voltar à tela de login


# Classe para formatar e validar datas
class DateFormater:
    def __init__(self, sv, entry):
        self.sv = sv  # StringVar que contém a data
        self.entry = entry  # Campo de entrada correspondente

    # Método para formatar a data enquanto é digitada
    def FormateDate(self):
        self.value = self.sv.get().replace("/", "")  # Remove barras da data
        self.formatted_value = ""

        # Adiciona barras conforme necessário
        if len(self.value) >= 2:
            self.formatted_value += self.value[:2] + "/"
        else:
            self.formatted_value += self.value

        if len(self.value) >= 4:
            self.formatted_value += self.value[2:4] + "/"
        elif len(self.value) > 2:
            self.formatted_value += self.value[2:4]

        if len(self.value) > 4:
            self.formatted_value += self.value[4:]

        self.sv.set(self.formatted_value[:10])  # Define o valor formatado no StringVar

        # Move o cursor para o final do texto
        self.entry.icursor(len(self.formatted_value))

    # Método para validar a data
    def ValidateDate(self, date_str):
        try:
            self.date_obj = datetime.strptime(date_str, "%d/%m/%Y")  # Tenta converter a string em um objeto datetime
            return date_str  # Retorna a string de data se for válida
        except ValueError:
            raise ValueError("Data inválida. Use o formato DD/MM/AAAA.")  # Levanta um erro se a data for inválida


# Código principal para iniciar a aplicação
if __name__ == "__main__":
    Weather()  # Cria uma instância da classe Weather e inicia a aplicação
