from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Initializing Dash-App:
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Data Import and Preparation
data_path = 'assets/Zufriedenheit_raw.csv'
df = pd.read_csv(data_path, sep=';', encoding='utf-8')

# Definition of Dash Layout
app.layout = html.Div([
    html.H1("Dashboard zur Zufriedenheit in der Schweiz", style={'textAlign': 'center'}),  # Titel für das Dashboard

    dcc.Tabs([
        dcc.Tab(label='Tab 1', children=[
            html.Div([  # Zeile für Spalten 1 und 2
                html.Div([  # Tab 1 / Spalte 1
                    html.Div(
                        id='container_1',  # Tab 1 / Spalte 1 / Container 1
                        children=[
                            html.H2("Allgemeine Lebensqualität in der Schweiz", style={'color': 'black'}),
                            html.H3("Einschätzung der subjektiven Lebensqualität", style={'color': 'black'}),
                            html.P("Bitte wählen Sie eine bevorzugte Farbe:", style={'color': 'black'}),  # Textfarbe schwarz
                            dcc.Dropdown(
                                id='dropdown_1',
                                options=[{'label': color, 'value': color} for color in
                                         ['blue', 'red', 'green', 'orange']],
                                value='blue',
                                multi=False
                            )
                        ]
                    ),
                    html.Div(
                        id='container_2',  # Tab 1 / Spalte 1 / Container 2
                        children=[
                            dcc.Graph(id='graph_1'),
                            html.P("Auswahl der Analyse-Jahre", style={'color': 'black'}),  # Textfarbe schwarz
                            dcc.RangeSlider(
                                id='slider_1',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()]
                            ),
                        ]
                    )
                ], className="columns_1_2"),  # Ende Spalte 1 (Tab 1)
                html.Div([  # Spalte 2
                    html.Div(
                        id='container_3',  # Tab 1 / Spalte 2 / Container 1
                        children=[
                            dcc.Graph(id='graph_2'),
                            html.P("Bitte wählen Sie ein Merkmal für den Vergleich aus:", style={'color': 'black'}),  # Textfarbe schwarz
                            dcc.Dropdown(
                                id='dropdown_2',
                                options=[{'label': col, 'value': col} for col in df.columns[3:]],
                                value=None,
                                multi=False
                            )
                        ]
                    )
                ], className="columns_1_2")  # Ende Spalte 2 (Tab 1)
            ], className="row")
        ]),
        # Layout-Anpassung für den Tab 2
        dcc.Tab(label='Tab 2', children=[
            html.Div([  # Zeile für Spalten 1 und 2
                html.Div([  # Tab 2 / Spalte 1
                    html.Div(
                        id='container_4',  # Tab 2 / Spalte 1 / Container 1
                        children=[
                            html.H2("Allgemeine Lebensqualität in der Schweiz", style={'color': 'black'}),
                            html.H3("Einschätzung der subjektiven Lebensqualität nach Geschlecht", style={'color': 'black'}),
                        ]
                    ),
                    html.Div(
                        id='container_5',  # Tab 2 / Spalte 1 / Container 2
                        children=[
                            dcc.Graph(id='graph_3'),
                            html.P("Auswahl der Analyse-Jahre", style={'color': 'black'}),  # Textfarbe schwarz
                            dcc.RangeSlider(
                                id='slider_2',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()]
                            ),
                        ]
                    )
                ], className="columns_1_2"),  # Ende Spalte 1 (Tab 2)
                html.Div([  # Spalte 2
                    html.Div(
                        id='container_6',  # Tab 2 / Spalte 2 / Container 1
                        children=[
                            dcc.Graph(id='graph_4'),
                            html.P("Bitte wählen Sie ein Merkmal für den Vergleich aus:", style={'color': 'black'}),  # Textfarbe schwarz
                            dcc.Dropdown(
                                id='dropdown_4',
                                options=[{'label': col, 'value': col} for col in df.columns[3:]],
                                value=None,
                                multi=False
                            )
                        ]
                    )
                ], className="columns_1_2")  # Ende Spalte 2 (Tab 2)
            ], className="row")
        ], style={'backgroundColor': 'white'})
    ])
], style={'backgroundColor': 'white'})  # Hintergrund auf Weiß setzen

"""
-----------------------------------------------------------------------------------------
Section 3:
Define Graph 1
"""
@app.callback(
    Output('graph_1', 'figure'),
    Input('dropdown_1', 'value'),
    Input('slider_1', 'value')
)
def update_graph_1(color_menue, selected_years):
    min_year, max_year = selected_years
    filtered_df = df[(df['Geschlecht'] == 'Alle') & (df['Jahr'] >= min_year) & (df['Jahr'] <= max_year)]

    fig = px.line(filtered_df,
                  x='Jahr',
                  y='Allgemein',
                  title='Entwicklung der subjektiven Zufriedenheit in der Schweiz',
                  color_discrete_sequence=[color_menue])
    fig.update_layout(bargap=0.05)
    fig.update_xaxes(tickmode='linear', tick0=filtered_df['Jahr'].min(), dtick=1, tickangle=270)  # Hier wird die x-Achsen-Beschriftung um 180 Grad gedreht
    return fig

"""
-----------------------------------------------------------------------------------------
Section 4:
Define Graph 2
"""
@app.callback(
    Output('graph_2', 'figure'),
    Input('dropdown_1', 'value'),
    Input('dropdown_2', 'value')
)
def update_graph_2(color_menue, col_menue):
    if col_menue:  # Überprüfen, ob eine Vergleichsvariable ausgewählt ist
        filtered_df = df[df['Geschlecht'] == 'Alle']
        fig = px.scatter(filtered_df,
                         x=col_menue,
                         y='Allgemein',
                         title=col_menue,  # Titel, wenn eine Vergleichsvariable ausgewählt ist
                         color_discrete_sequence=[color_menue])
        return fig
    else:
        return px.scatter(title='Wähle eine Vergleichvariable')  # Wenn keine Vergleichsvariable ausgewählt ist

"""
-----------------------------------------------------------------------------------------
Section 5:
Define Graph 3
"""
@app.callback(
    Output('graph_3', 'figure'),
    Input('slider_2', 'value')
)
def update_graph_3(selected_years):
    min_year, max_year = selected_years
    # Daten filtern, um nur Männer und Frauen zu erhalten
    filtered_df = df[(df['Jahr'] >= min_year) & (df['Jahr'] <= max_year) & (df['Geschlecht'].isin(['Männer', 'Frauen']))]

    fig = px.line(filtered_df,
                  x='Jahr',
                  y='Allgemein',
                  color='Geschlecht',
                  title='Entwicklung der subjektiven Zufriedenheit in der Schweiz (Männer vs Frauen)',
                  color_discrete_map={'Männer': 'blue', 'Frauen': 'red'})

    fig.update_layout(bargap=0.05)
    fig.update_xaxes(tickmode='linear', tick0=filtered_df['Jahr'].min(), dtick=1, tickangle=270)
    return fig

"""
-----------------------------------------------------------------------------------------
Section 6:
Define Graph 4
"""
@app.callback(
    Output('graph_4', 'figure'),
    Input('dropdown_4', 'value'),
    Input('slider_2', 'value')
)
def update_graph_4(col_menue, selected_years):
    if col_menue:  # Überprüfen, ob eine Vergleichsvariable ausgewählt ist
        min_year, max_year = selected_years
        # Daten filtern, um nur die Jahre im Bereich und nur Männer und Frauen zu erhalten
        filtered_df = df[(df['Jahr'] >= min_year) & (df['Jahr'] <= max_year) & (df['Geschlecht'].isin(['Männer', 'Frauen']))]
        
        fig = px.scatter(filtered_df,
                         x=col_menue,
                         y='Allgemein',
                         color='Geschlecht',
                         title=f'{col_menue} Vergleich (Männer vs Frauen)',
                         color_discrete_map={'Männer': 'blue', 'Frauen': 'red'})

        return fig
    else:
        return px.scatter(title='Wähle eine Vergleichvariable')  # Wenn keine Vergleichsvariable ausgewählt ist


"""
-----------------------------------------------------------------------------------------
Finish
"""
if __name__ == '__main__':
    #run the app in server port 8051:
    app.run_server(port=8051, debug=True)
