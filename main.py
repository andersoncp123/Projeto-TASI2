import pandas as pd
import plotly.express as px

# Carregar o dataset atualizado
merged_data = pd.read_csv("covid-eua.csv")

# Verificar se as colunas lat e lng estão corretas
merged_data = merged_data.dropna(subset=["lat", "lng"])

# Agrupar os dados por cidade/condado e mês, somando as colunas numéricas (por exemplo, hospitalizados)
monthly_data = merged_data.groupby(["county", "todays_date"]).agg({
    "hospitalized_covid_confirmed_patients": "sum",
    "hospitalized_suspected_covid_patients": "sum",
    "hospitalized_covid_patients": "sum",
    "all_hospital_beds": "sum",
    "icu_covid_confirmed_patients": "sum",
    "icu_suspected_covid_patients": "sum",
    "icu_available_beds": "sum",
    "lat": "first",  # Mantém a lat constante
    "lng": "first",  # Mantém a lng constante
}).reset_index()

# Criar o gráfico de mapa
fig = px.scatter_geo(
    monthly_data,
    lat="lat",  # Coluna de lat
    lon="lng",  # Coluna de lng
    hover_name="county",  # Nome da cidade/condado que aparece ao passar o mouse
    size="hospitalized_covid_patients",  # Tamanho dos pontos de acordo com o número de pacientes
    color="hospitalized_covid_patients",  # Cor dos pontos de acordo com o número de pacientes
    title="Mapa de Casos de COVID-19 nos EUA - Por Mês",
    template="plotly_dark",  # Usar o tema de fundo escuro
    projection="albers usa",  # Projeção focada nos EUA
    animation_frame="todays_date",  # Animação por mês (se desejar ver a evolução)
)

# Exibir o gráfico
fig.show()
