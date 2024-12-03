import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv("covid-eua.csv")

# Inicializar o app
app = dash.Dash(__name__)

# Layout do app
app.layout = html.Div([
    html.Div([
        dcc.Graph(id="map-graph"),
    ]),
    html.Div([
        dcc.RadioItems(
            id="variable-selector",
            options=[
                {"label": "Hospital Cases", "value": "hospital"},
                {"label": "ICU Cases", "value": "icu"}
            ],
            value="hospital",
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id="line-graph"),
    ]),
])

# Callback para atualizar o mapa
@app.callback(
    Output("map-graph", "figure"),
    Input("variable-selector", "value")
)
def update_map(selected_variable):
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        size="hospitalized_covid_confirmed_patients",
        hover_name="county",
        mapbox_style="carto-positron",
        center={"lat": 37.0902, "lon": -95.7129},  # Centralizado nos EUA
        zoom=4,
    )
    return fig

@app.callback(
    Output("line-graph", "figure"),
    [Input("map-graph", "selectedData"),
     Input("variable-selector", "value")]
)
def update_line(selected_data, selected_variable):
    # Filtrar cidades selecionadas
    if selected_data and "points" in selected_data:
        counties = [point["hovertext"] for point in selected_data["points"]]
        filtered_df = df[df["county"].isin(counties)]
    else:
        filtered_df = df

    # Escolher variáveis
    if selected_variable == "hospital":
        vars_to_plot = ["hospitalized_covid_confirmed_patients",
                        "hospitalized_suspected_covid_patients",
                        "all_hospital_beds"]
    else:
        vars_to_plot = ["icu_covid_confirmed_patients",
                        "icu_suspected_covid_patients",
                        "icu_available_beds"]

    # Somatório diário
    aggregated_df = filtered_df.groupby("todays_date")[vars_to_plot].sum().reset_index()

    # Gráfico de linhas
    fig = px.line(
        aggregated_df.melt(id_vars=["todays_date"], value_vars=vars_to_plot),
        x="todays_date",
        y="value",
        color="variable",
        labels={"value": "Cases", "todays_date": "Date"}
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
