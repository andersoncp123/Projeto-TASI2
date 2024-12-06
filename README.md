# TASI2

Este é um trabalho para a faculdade sobre visualização de dados usando datasets de Covid nas cidades dos Estados Unidos.

As bases de dados fontes utilizadas são:

- **statewide-covid-19-hospital-county-data.csv**: Contém informações sobre os casos de COVID-19.
- **uscities.csv**: Contém dados sobre os pontos de latitude e longitude das cidades dos EUA.

A base de dados **covid-eua.csv** é um merge das duas bases anteriores, com o seguinte pré-processamento aplicado:

- Remoção de dados duplicados.
- Agrupamento dos dados por mês.
- Exclusão de registros com dados faltantes.
- Atribuição de um único ponto de latitude e longitude para cada condado.

## Requisitos

- Python 3.x
- Virtual Environment (venv)

## Como Rodar o Projeto

1. Clone o repositório com o comando:
   
   `git clone https://github.com/andersoncp123/Projeto-TASI2.git`
   
   Depois entre na pasta do projeto com:
   
   `cd nome-do-repositorio`

2. Crie um ambiente virtual com o comando:
   
   `python -m venv venv`
   
   (Caso ainda não tenha o `virtualenv` instalado, instale com `pip install virtualenv`).

3. Ative o ambiente virtual:

   - No Windows: `.\venv\Scripts\activate`
   
   - No macOS/Linux: `source venv/bin/activate`

4. Instale as dependências com:
   
   `pip install -r requirements.txt`

5. Finalmente, execute o código com:
   
   `python main.py`
