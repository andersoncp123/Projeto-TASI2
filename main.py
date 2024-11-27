import pandas as pd

# Carregar o dataset combinado
merged_data = pd.read_csv("covid-eua.csv")

# Preencher os valores ausentes com 0 para todas as colunas numéricas
merged_data.fillna(0, inplace=True)

# Salvar o dataset atualizado
merged_data.to_csv("covid-eua.csv", index=False)

print("Valores ausentes preenchidos com 0. Arquivo 'covid-eua.csv' atualizado com sucesso!")
