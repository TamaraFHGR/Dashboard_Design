from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import math

# Initializing Dash-App:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

"""
-----------------------------------------------------------------------------------------
Section 1:
Data Import and Preparation
"""

data_path = 'assets/city_happiness_train_data.csv'
df = pd.read_csv(data_path, sep=',', encoding='utf-8')
df_2024 = df[df['Year'] == 2024]

"""
-----------------------------------------------------------------------------------------
Section 2:
Definition of Dash Layout
"""

app.layout = html.Div([
    html.Div([                          # Spalte 1
        html.Div(
            id='container_1',                   # Spalte 1 / Container 1
            children=[
                html.H1("Titel - Irgendeine Happiness Studie.."),
                html.H2("Platzhalter für Einleitungstext..."),
                html.P("Hier könnte ein weiterer Text stehen..."),
                dcc.Dropdown(
                    id='dropdown_1',
                    options=['red', 'green', 'orange'],
                    value='red',
                    multi=False)]
        ),
        html.Div(
            id='container_2',                   # Spalte 1 / Container 2
            children=[
                html.P("Platzhalter für mehr Text ..."),
                dcc.Graph(
                    id='graph_1'),
                dcc.Slider(
                    id='slider_1',
                    min=math.floor(df['Happiness_Score'].min()),
                    max=math.ceil(df['Happiness_Score'].max()))]
        )], className="columns_1_2"),           # Ende Spalte 1
    html.Div([                          # Spalte 2
        html.Div(
            id='container_3',                   # Spalte 2 / Container 1
            children=[
                dcc.Dropdown(
                    id='dropdown_2',
                    options=['red', 'green', 'orange'],
                    value='red',
                    multi=False),
                dcc.Graph(
                    id='graph_2')]
        )
    ], className="columns_1_2")            # Ende Spalte 2
], className="row")

"""
-----------------------------------------------------------------------------------------
Section 3:
Define Graph 1
"""

@app.callback(
    Output('graph_1', 'figure'),
    Input('dropdown_1', 'value')
)

def update_graph_1(color_menue):
    fig = px.histogram(df_2024,
                       x='Happiness_Score',
                       title='Distribution of Happiness Score',
                       color_discrete_sequence=[color_menue])
    fig.update_layout(bargap=0.05)
    return fig

"""
-----------------------------------------------------------------------------------------
Section 4:
Define Graph 2
"""

@app.callback(
    Output('graph_2', 'figure'),
    Input('dropdown_2', 'value')
)

def update_graph_2(color_menue):
    fig = px.scatter(df_2024,
                     x='Happiness_Score',
                     y='Cost_of_Living_Index',
                     title='Happiness Score and Cost of Living Index',
                     color_discrete_sequence=[color_menue])
                     #color='City',
                     #size='Population',
                     #hover_data=['City', 'Happiness_Score', 'Cost_of_Living_Index'])
    return fig

if __name__ == '__main__':
    #run the app in server port 8051:
    app.run_server(port=8051, debug=True)