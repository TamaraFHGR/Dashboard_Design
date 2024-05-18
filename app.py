from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'])

"""
-----------------------------------------------------------------------------------------
Section 1:
Data Import and Preparation
"""

# Data Import and Preparation
data_path = 'assets/Zufriedenheit_raw.csv'
df = pd.read_csv(data_path, sep=';', encoding='utf-8')

"""
-----------------------------------------------------------------------------------------
Section 2:
Definition of Dash Layout
"""

app.layout = html.Div([
    # Header:
    html.H1("Dashboard zur Zufriedenheit in der Schweiz"),
    html.H2("Exploration der allgemeinen Lebensqualität"),
    html.H3("Bitte wählen Sie eine bevorzugte Farbe für die Anzeige der Grafiken:"),
    dcc.Dropdown(id='dropdown_color',
                 options=[{'label': color, 'value': color} for color in
                          ['blue', 'red', 'green', 'orange']],
                 value='blue',
                 multi=False),
    # Tabs:
    dcc.Tabs([
        # Tab 1:
        dcc.Tab(label='Gesamtübersicht Schweiz', children=[
            html.Div([
                html.Div([
                    html.Div(
                        id='container_1',
                        children=[
                            html.H4("Entwicklung der subjektiven Zufriedenheit"),
                            dcc.Graph(id='graph_1'),
                            html.P("Auswahl der Analyse-Jahre:"),
                            dcc.RangeSlider(
                                id='slider_1',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()]),
                        ]
                    )
                ], className="columns"),
                html.Div([
                    html.Div(
                        id='container_2',
                        children=[
                            html.H4("Einflussfaktoren auf die allgemeine Zufriedenheit"),
                            dcc.Graph(id='graph_2'),
                            html.P("Bitte wählen Sie einen Einflussfaktor aus:"),
                            dcc.Dropdown(
                                id='dropdown_2',
                                options=[{'label': col, 'value': col} for col in df.columns[3:]],
                                value=None,
                                multi=False)
                        ]
                    )
                ], className="columns")
            ], className="row")
        ], className="tabs"),
        # Tab 2:
        dcc.Tab(label='Detail-Analyse nach demografischen Merkmalen', children=[
            html.Div([
                html.Div([
                    html.Div(
                        id='container_3',
                        children=[
                            html.H4("Titel zur Grafik noch anpassen..."),
                            dcc.Graph(id='graph_3'),
                            html.P("Auswahl der Analyse-Jahre:"),
                            dcc.RangeSlider(
                                id='slider_3',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()]),
                        ]
                    )
                ], className="columns"),
                html.Div([
                    html.Div(
                        id='container_4',
                        children=[
                            html.H4("Titel zur Grafik noch anpassen..."),
                            dcc.Graph(id='graph_4'),
                            html.P("Bitte wählen Sie ein Merkmal für den Vergleich aus:"),
                            dcc.Dropdown(
                                id='dropdown_4',
                                options=[{'label': col, 'value': col} for col in df.columns[3:]],
                                value=None,
                                multi=False)
                        ]
                    )
                ], className="columns")
            ], className="row")
        ], className="tabs")
    ])
])

"""
-----------------------------------------------------------------------------------------
Section 3:
Define Graph 1 - Linechart (Allgemein)
"""
@app.callback(
    Output('graph_1', 'figure'),
    Input('dropdown_color', 'value'),
    Input('slider_1', 'value'))

def update_graph_1(color_menue, selected_years):
    min_year, max_year = selected_years
    filtered_df = df[(df['Geschlecht'] == 'Alle') & (df['Jahr'] >= min_year) & (df['Jahr'] <= max_year)]

    fig = px.line(filtered_df,
                  x='Jahr',
                  y='Allgemein',
                  color_discrete_sequence=[color_menue])

    fig.update_xaxes(dtick=1,
                     tickangle=45,
                     tickmode='linear',
                     tick0=filtered_df['Jahr'].min(),
                     showgrid=False,
                     showticklabels=True,
                     ticks="",
                     tickfont=dict(color='#808080'), tickcolor='#808080')

    fig.update_yaxes(showgrid=False,
                     showticklabels=True,
                     ticks="",
                     tickfont=dict(color='#808080'), tickcolor='#808080')

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        bargap=0.05,
        xaxis_title="",
        yaxis_title="Allgemeiner Zufriedenheits-Index",
        font=dict(color='#808080')
    )

    return fig

"""
-----------------------------------------------------------------------------------------
Section 4:
Define Graph 2 - Scatter-Plot (Allgemein und Einflussfaktoren)
"""
@app.callback(
    Output('graph_2', 'figure'),
    Input('dropdown_color', 'value'),
    Input('dropdown_2', 'value'))

def update_graph_2(color_menue, col_menue):
    if col_menue:  # Überprüfen, ob eine Vergleichsvariable ausgewählt ist
        filtered_df = df[df['Geschlecht'] == 'Alle']

        fig = px.scatter(filtered_df,
                         x=col_menue,
                         y='Allgemein',
                         title=f"Zusammenhang allgemeinen Zufriedenheit und {col_menue}",
                         color_discrete_sequence=[color_menue])

        fig.update_xaxes(dtick=1,
                         tickangle=0,
                         tickmode='linear',
                         showgrid=False,
                         showticklabels=True,
                         ticks="",
                         tickfont=dict(color='#808080'), tickcolor='#808080')

        fig.update_yaxes(showgrid=False,
                         showticklabels=True,
                         ticks="",
                         tickfont=dict(color='#808080'), tickcolor='#808080')

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0.05,
            xaxis_title=f"{col_menue}-Index",
            yaxis_title="Allgemeiner Zufriedenheits-Index",
            font=dict(color='#808080')
        )

        return fig
    else:
        return px.scatter(title="Bitte wählen Sie einen Einflussfaktor aus.")

"""
-----------------------------------------------------------------------------------------
Section 5:
Define Graph 3 - Linechart (Allgemein Männer vs Frauen)
"""

@app.callback(
    Output('graph_3', 'figure'),
    Input('slider_3', 'value'))

def update_graph_3(selected_years):
    min_year, max_year = selected_years
    # Daten filtern, um nur Männer und Frauen zu erhalten
    filtered_df = df[
        (df['Jahr'] >= min_year) & (df['Jahr'] <= max_year) & (df['Geschlecht'].isin(['Männer', 'Frauen']))]

    fig = px.line(filtered_df,
                  x='Jahr',
                  y='Allgemein',
                  color='Geschlecht',
                  color_discrete_map={'Männer': 'blue', 'Frauen': 'red'})

    fig.update_xaxes(dtick=1,
                     tickangle=45,
                     tickmode='linear',
                     tick0=filtered_df['Jahr'].min(),
                     showgrid=False,
                     showticklabels=True,
                     ticks="",
                     tickfont=dict(color='#808080'), tickcolor='#808080')

    fig.update_yaxes(showgrid=False,
                     showticklabels=True,
                     ticks="",
                     tickfont=dict(color='#808080'), tickcolor='#808080')

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        bargap=0.05,
        xaxis_title="",
        yaxis_title="Allgemeiner Zufriedenheits-Index",
        font=dict(color='#808080')
    )
    return fig

"""
-----------------------------------------------------------------------------------------
Section 6:
Define Graph 4 - Scatter-Plot (Frauen vs. Männer)
"""

@app.callback(
    Output('graph_4', 'figure'),
    Input('dropdown_4', 'value'),
    Input('slider_1', 'value'))

def update_graph_4(col_menue, selected_years):
    if col_menue:  # Überprüfen, ob eine Vergleichsvariable ausgewählt ist
        min_year, max_year = selected_years
        # Daten filtern, um nur die Jahre im Bereich und nur Männer und Frauen zu erhalten
        filtered_df = df[
            (df['Jahr'] >= min_year) & (df['Jahr'] <= max_year) & (df['Geschlecht'].isin(['Männer', 'Frauen']))]

        fig = px.scatter(filtered_df,
                         x=col_menue,
                         y='Allgemein',
                         color='Geschlecht',
                         title=f"Zusammenhang allgemeinen Zufriedenheit und {col_menue}",
                         color_discrete_map={'Männer': 'blue', 'Frauen': 'red'})

        fig.update_xaxes(dtick=1,
                         tickangle=0,
                         tickmode='linear',
                         showgrid=False,
                         showticklabels=True,
                         ticks="",
                         tickfont=dict(color='#808080'), tickcolor='#808080')

        fig.update_yaxes(showgrid=False,
                         showticklabels=True,
                         ticks="",
                         tickfont=dict(color='#808080'), tickcolor='#808080')

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0.05,
            xaxis_title=f"{col_menue}-Index",
            yaxis_title="Allgemeiner Zufriedenheits-Index",
            font=dict(color='#808080')
        )
        return fig
    else:
        return px.scatter(title="Bitte wählen Sie einen Einflussfaktor aus.")


if __name__ == '__main__':
    # run the app in server port 8051:
    app.run_server(port=8051, debug=True)
