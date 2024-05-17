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

data_path = 'assets/Zufriedenheit_raw.csv'
df = pd.read_csv(data_path, sep=';', encoding='utf-8')
"""
-----------------------------------------------------------------------------------------
Section 2:
Definition of Dash Layout
"""

app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Tab 1', children=[
            html.Div([  # Zeile für Spalten 1 und 2
                html.Div([  # Spalte 1
                    html.Div(
                        id='container_1',  # Spalte 1 / Container 1
                        children=[
                            html.H1("Lebensqualität in der Schweiz"),
                            html.H2("Einschätzung der subjektiven Lebensqualität"),
                            html.P("Wie hat sich die Lebensqualität in der Schweiz entwickelt und welche Faktoren bilden dafür eine Rolle?"),
                            dcc.Dropdown(
                                id='dropdown_1',
                                options=[{'label': color, 'value': color} for color in ['red', 'green', 'orange']],
                                value='red',
                                multi=False
                            )
                        ]
                    ),
                    html.Div(
                        id='container_2',  # Spalte 1 / Container 2
                        children=[
                            html.P("Platzhalter für mehr Text ..."),
                            dcc.Graph(id='graph_1'),
                            dcc.Slider(
                                id='slider_1',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max()
                            )
                        ]
                    )
                ], className="columns_1_2"),  # Ende Spalte 1

                html.Div([  # Spalte 2
                    html.Div(
                        id='container_3',  # Spalte 2 / Container 1
                        children=[
                            dcc.Dropdown(
                                id='dropdown_2',
                                options=[{'label': color, 'value': color} for color in ['red', 'green', 'orange']],
                                value='red',
                                multi=False
                            ),
                            dcc.Graph(id='graph_2'),
                            dcc.Dropdown(
                                id='dropdown_3',
                                options=[{'label': col, 'value': col} for col in df.columns],
                                value=None,
                                multi=False
                            )
                        ]
                    )
                ], className="columns_1_2")  # Ende Spalte 2
            ], className="row")  # Zeilencontainer für Spalten 1 und 2
        ]),
        dcc.Tab(label='Tab 2', children=[
            html.Div([  # Zeile für Spalten 1 und 2
                html.Div([  # Spalte 1
                    html.Div(
                        id='container_4',  # Spalte 1 / Container 1
                        children=[
                            html.H1("Zusätzliche Analyse"),
                            html.H2("Vergleich der Lebensqualität"),
                            html.P("Vergleich der Lebensqualität mit anderen Faktoren."),
                            dcc.Dropdown(
                                id='dropdown_4',
                                options=[{'label': col, 'value': col} for col in df.columns],
                                value='GDP',
                                multi=False
                            )
                        ]
                    ),
                    html.Div(
                        id='container_5',  # Spalte 1 / Container 2
                        children=[
                            html.P("Platzhalter für mehr Text ..."),
                            dcc.Graph(id='graph_3')
                        ]
                    )
                ], className="columns_1_2")  # Ende Spalte 1
            ], className="row")  # Zeilencontainer für Spalten 1 und 2
        ])
    ])
], className="row")  # Hauptcontainer

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
    filtered_df = df[df['Geschlecht'] == 'Alle']

    fig = px.line(filtered_df,
                  x='Jahr',
                  y='Allgemein',
                  title='Entwicklung der subjektiven Zufriedenheit in der Schweiz',
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
    Input('dropdown_2', 'value'),
    Input('dropdown_3', 'value')
)

def update_graph_2(color_menue, col_menue):
    filtered_df = df[df['Geschlecht'] == 'Alle']

    fig = px.scatter(filtered_df,
                     x=col_menue,
                     y='Allgemein',
                     title='Abhängigkeit der Zufriedenheit von unterschiedlichen Faktoren',
                     color_discrete_sequence=[color_menue])
    return fig

if __name__ == '__main__':
    #run the app in server port 8051:
    app.run_server(port=8051, debug=True)