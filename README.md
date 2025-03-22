# Aplicativo de Previsão do Tempo

Este é um aplicativo simples que permite aos usuários se cadastrar, fazer login e obter previsões do tempo para uma cidade específica em um intervalo de datas. O aplicativo utiliza a API do OpenWeather para fornecer as informações climáticas.

## Funcionalidades

- **Cadastro de Usuário**: Os usuários podem se cadastrar fornecendo um nome de usuário e senha.
- **Login**: Os usuários podem fazer login com suas credenciais.
- **Seleção de Cidade e Datas**: Após o login, os usuários podem escolher uma cidade e um intervalo de datas (com um limite de 7 dias entre a data inicial e final).
- **Previsão do Tempo**: O aplicativo retorna a previsão do tempo para a cidade selecionada no intervalo de datas especificado em um arquivo .txt.

## Requisitos

- Python 3
- Biblioteca `requests` para fazer chamadas à API do OpenWeather.

## Estrutura do Projeto

- `Users.bd`: Banco de dados SQLite para armazenar informações dos usuários.
- `database.py`: Script para gerenciar o banco de dados.
- `login.py`: Script para gerenciar o login dos usuários.
- `main.py`: Script principal que inicia o aplicativo.
- `register.py`: Script para gerenciar o registro de novos usuários.
- `screen.py`: Script para gerenciar a interface do usuário.
- `weather.py`: Script para interagir com a API do OpenWeather e obter previsões do tempo.
