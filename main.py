import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px

# Carregar dados
df = pd.read_csv("covid-eua.csv")
df["todays_date"] = pd.to_datetime(df["todays_date"])

# Gerar marcas de anos únicas para o slider
years = sorted(df["todays_date"].dt.year.unique())
year_marks = {i: str(year) for i, year in enumerate(years)}

# Inicializar o app
app = dash.Dash(__name__)

# Layout do app
app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px"}, children=[
    # Controles no topo
    html.Div([
        html.Div([
            html.Div("Selecione o Tipo de Dados:", style={"fontWeight": "bold", "marginBottom": "10px"}),
            dcc.RadioItems(
                id="variable-selector",
                options=[
                    {"label": "Hospital Cases", "value": "hospital"},
                    {"label": "ICU Cases", "value": "icu"}
                ],
                value="hospital",
                labelStyle={
                    "display": "inline-block",
                    "marginRight": "10px",
                    "padding": "5px 10px",
                    "border": "1px solid #ccc",
                    "borderRadius": "5px",
                    "cursor": "pointer"
                },
                inputStyle={"marginRight": "5px"}
            ),
        ], style={"marginBottom": "20px"}),

        html.Div("Selecione o Intervalo de Tempo:", style={"fontWeight": "bold", "marginBottom": "10px"}),
        dcc.RangeSlider(
            id="time-slider",
            min=0,
            max=len(years) - 1,
            step=1,
            value=[0, len(years) - 1],
            marks=year_marks,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
    ], style={"marginBottom": "30px"}),

    # Divisão principal: mapa e gráfico lado a lado
    html.Div([
        html.Div([
            dcc.Graph(id="map-graph"),
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top", "paddingRight": "10px"}),

        html.Div([
            dcc.Graph(id="line-graph"),
        ], style={"width": "48%", "display": "inline-block", "verticalAlign": "top", "paddingLeft": "10px"}),
    ], style={"marginBottom": "20px"}),

    # Lista de cidades
    html.Div([
        html.H4("Cidades Selecionadas", style={"textAlign": "center", "marginBottom": "10px", "color": "#2c3e50"}),
        html.Ul(id="selected-cities", style={
            "listStyleType": "none",
            "padding": "10px",
            "backgroundColor": "#ecf0f1",
            "border": "1px solid #bdc3c7",
            "borderRadius": "5px",
            "maxHeight": "200px",
            "overflowY": "auto",
            "textAlign": "center",
            "margin": "0 auto",
            "width": "50%"
        })
    ]),
])

# Callback para atualizar o mapa com transparência nas bolinhas
@app.callback(
    Output("map-graph", "figure"),
    Input("variable-selector", "value")
)
def update_map(selected_variable):
    # Ajustar o gráfico de dispersão com opacidade nas bolinhas
    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lng",
        size="hospitalized_covid_confirmed_patients",
        hover_name="county",
        mapbox_style="carto-positron",
        center={"lat": 37.0902, "lon": -95.7129},
        zoom=3,
        opacity=0.5,  # Definindo transparência para as bolinhas
        size_max=20,  # Ajuste do tamanho máximo das bolinhas para evitar sobrecarga
    )
    
    # Definir transparência proporcional ao tamanho das bolinhas
    fig.update_traces(marker=dict(opacity=0.5))
    return fig


# Callback para atualizar gráfico de linhas e lista de cidades
@app.callback(
    [Output("line-graph", "figure"),
     Output("selected-cities", "children")],
    [Input("map-graph", "selectedData"),
     Input("variable-selector", "value"),
     Input("time-slider", "value")],
    State("map-graph", "relayoutData")
)
def update_line(selected_data, selected_variable, time_range, relayout_data):
    # Filtrar cidades selecionadas
    if selected_data and "points" in selected_data:
        counties = list(set([point["hovertext"] for point in selected_data["points"]]))
        filtered_df = df[df["county"].isin(counties)]
        selected_cities = [html.Li(city) for city in sorted(counties)]
    else:
        filtered_df = df
        selected_cities = [html.Li("Todas as cidades")]

    # Filtrar por intervalo de tempo (apenas anos)
    start_year, end_year = years[time_range[0]], years[time_range[1]]
    filtered_df = filtered_df[
        (filtered_df["todays_date"].dt.year >= start_year) &
        (filtered_df["todays_date"].dt.year <= end_year)
    ]

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
    return fig, selected_cities

if __name__ == "__main__":
    app.run_server(debug=False)
