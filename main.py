import pandas as pd

# Carregar o dataset
merged_data = pd.read_csv("covid-eua.csv")

# Converter a coluna 'todays_date' para o formato de data
merged_data["todays_date"] = pd.to_datetime(merged_data["todays_date"])

# Agrupar os dados por mês e cidade, somando as colunas numéricas
monthly_data = merged_data.groupby([merged_data["county"], merged_data["todays_date"].dt.to_period("M")]).agg({
    "hospitalized_covid_confirmed_patients": "sum",
    "hospitalized_suspected_covid_patients": "sum",
    "hospitalized_covid_patients": "sum",
    "all_hospital_beds": "sum",
    "icu_covid_confirmed_patients": "sum",
    "icu_suspected_covid_patients": "sum",
    "icu_available_beds": "sum",
    "lat": "first",  # Mantém a lat constante (o valor da primeira linha)
    "lng": "first",  # Mantém a long constante (o valor da primeira linha)
}).reset_index()

# Atualizar a coluna 'todays_date' para mostrar apenas o ano e mês no formato YYYY-MM
monthly_data["todays_date"] = monthly_data["todays_date"].dt.strftime('%Y-%m')

# Salvar o dataset mensal
monthly_data.to_csv("covid-eua.csv", index=False)

print("Dados transformados de diário para mensal (ano/mês). Arquivo 'covid-eua-mensal.csv' criado com sucesso!")
