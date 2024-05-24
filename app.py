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
    html.Div([
    html.H1("Dashboard zur Zufriedenheit in der Schweiz"),
    html.H2("Exploration der allgemeinen Lebensqualität"),
    ], className='header'),

    # Tabs:
    dcc.Tabs(id='tabs', value='tab_1', children=[

        # Tab 1:
        dcc.Tab(id='tab_1', label='Gesamtanalyse Schweiz', value='tab_1', className='tab', selected_className='tab-active', children=[
            html.Div([
                html.Div([
                    html.H3(
                        "In einer jährlichen Umfrage werden Teilnehmer und Teilnehmerinnen gebeten, ihre allgemeine Lebenszufriedenheit auf einer Skala von 0 bis 10 zu bewerten,"
                        " wobei 0 für 'gar nicht zufrieden' und 10 für 'vollständig zufrieden' steht. Folgende Teilbereiche werden dabei abgefragt:"),
                    html.Div([
                        html.Div([
                            html.Ul([
                                html.Li("die Allgemeine Zufriedenheit"),
                                html.Li("die finanzielle Lage"),
                                html.Li("das Alleinleben")
                            ])
                        ], className="three columns"),
                        html.Div([
                            html.Ul([
                                html.Li("das Zusammenleben"),
                                html.Li("persönliche Beziehungen"),
                                html.Li("die Gesundheit")
                            ])
                        ], className="three columns"),
                        html.Div([
                            html.Ul([
                                html.Li("die Wohnsituation"),
                                html.Li("die Arbeitsbedingungen"),
                                html.Li("das Arbeitsklima")
                            ])
                        ], className="three columns")
                    ], className="row")
                ], className="row"),
                html.Div([
                    html.Div(
                        id='container_1',
                        children=[
                            html.H4("Entwicklung der allgemeinen Zufriedenheit"),
                            dcc.Graph(id='graph_1'),
                            html.P("Auswahl der Analyse-Jahre:"),
                            dcc.RangeSlider(
                                id='slider_1',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()])
                        ]
                    )
                ], className="two columns"),
                html.Div([
                    html.Div(
                        id='container_2',
                        children=[
                            html.H4("Zufriedenheit in verschiedenen Teilbereichen"),
                            dcc.Graph(id='graph_2'),
                            html.P("Bitte wählen Sie die gewünschten Teilbereiche aus:"),
                            dcc.Dropdown(
                                id='dropdown_2',
                                options=[{'label': col, 'value': col} for col in df.columns[3:]],
                                value=None,
                                multi=True)
                        ]
                    )
                ], className="two columns")
            ], className="row")
        ]),

        # Tab 2:
        dcc.Tab(id='tab_2', label='Analyse nach Geschlecht', value='tab_2', className='tab', selected_className='tab-active', children=[
            html.Div([
                html.Div([
                    html.Div(
                        id='container_3',
                        children=[
                            html.H4("Entwicklung der allgemeinen Zufriedenheit, aufgeteilt nach Geschlecht"),
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
                ], className="two columns"),
                html.Div([
                    html.Div(
                        id='container_4',
                        children=[
                            html.H4("Zufriedenheit in verschiedenen Teilbereichen, aufgeteilt nach Geschlecht"),
                            dcc.Graph(id='graph_4'),
                            html.P("Bitte wählen Sie einen Teilbereich aus:"),
                            dcc.Dropdown(
                                id='dropdown_4',
                                options=[{'label': col, 'value': col} for col in df.columns[3:]],
                                value=None,
                                multi=False)
                        ]
                    )
                ], className="two columns")
            ], className="row")
        ]),

        # Tab 3:
        dcc.Tab(id='tab_3', label='Analyse nach demografischen Merkmalen', value='tab_3', className='tab', selected_className='tab-active', children=[
            html.Div([
                html.Div([
                    html.Div(
                        id='container_5',
                        children=[
                            html.H4("Hier entsteht eine weitere Grafik...")
                        ]
                    )
                ], className="two columns"),
                html.Div([
                    html.Div(
                        id='container_6',
                        children=[
                            html.H4("Hier entsteht ein weitere Grafik...")
                        ]
                    )
                ], className="two columns")
            ], className="row")
        ]),
    ])
], className='container')

"""
-----------------------------------------------------------------------------------------
Section 3:
Tab 1: Define Graph 1 - Linechart (Allgemein)
"""
@app.callback(
    Output('graph_1', 'figure'),
    Input('slider_1', 'value'))

def update_graph_1(selected_years):
    min_year, max_year = selected_years
    filtered_df = df[(df['Geschlecht'] == 'Alle') & (df['Jahr'] >= min_year) & (df['Jahr'] <= max_year)]

    fig = px.line(filtered_df,
                  x='Jahr',
                  y='Allgemein')

    fig.update_traces(marker=dict(size=12, symbol='circle', line=dict(width=1.5, color='#808080')),
                      line=dict(color='#04AAE9', width=4),
                      mode='markers+lines')

    fig.update_xaxes(dtick=1,
                     tickangle=45,
                     tickmode='linear',
                     tick0=filtered_df['Jahr'].min(),
                     showgrid=False,
                     showticklabels=True,
                     ticks="",
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080')

    fig.update_yaxes(showgrid=False,
                     showticklabels=True,
                     ticks='outside',
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080',
                     tickformat=".2f",
                     range=[7.80, 8.30])

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis_title="",
        yaxis_title="Zufriedenheits-Index",
        font=dict(color='#808080', size=14, family='Arial, sans-serif'))

    return fig

"""
-----------------------------------------------------------------------------------------
Section 4:
Tab 1: Define Graph 2 - Scatter-Plot (Allgemein und Einflussfaktoren)
"""
@app.callback(
    Output('graph_2', 'figure'),
    Input('dropdown_2', 'value'),
    Input('slider_1', 'value'))

def update_graph_2(col_menue, selected_years):
    if col_menue:  # Überprüfen, ob eine Vergleichsvariable ausgewählt ist
        min_year, max_year = selected_years
        filtered_df = df[(df['Jahr'] >= min_year) & (df['Jahr'] <= max_year) & (df['Geschlecht'] == 'Frauen') | (df['Geschlecht'] == 'Männer')]

        melted_df = filtered_df.melt(id_vars=['Jahr', 'Allgemein'], value_vars=col_menue,
                                     var_name='Variable', value_name='Value')

        fig = px.scatter(melted_df,
                         x='Value',
                         y='Allgemein',
                         color='Variable',
                         color_discrete_sequence=px.colors.qualitative.Dark24)

        fig.update_traces(marker=dict(size=12, line=dict(width=1.5, color='#808080')))

        fig.update_xaxes(showgrid=False,
                         showticklabels=True,
                         tickangle=45,
                         ticks='outside',
                         tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         tickcolor='#808080',
                         tickformat=".2f")
                         #dtick=0.1,
                         #range=[6.70, 9.50])

        fig.update_yaxes(showgrid=False,
                         showticklabels=True,
                         ticks='outside',
                         tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         tickcolor='#808080',
                         tickformat=".2f",
                         range=[7.80, 8.30])

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            xaxis_title='',
            yaxis_title="Allgemeine Zufriedenheit",
            font=dict(color='#808080', size=14, family='Arial, sans-serif'),
            title={
                'text': f"<i>Vergleich von {col_menue}<i>",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=16,
                    color='white',
                    family='Arial, sans-serif')})

        return fig

    else:
        fig = px.scatter()

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#808080'),
            title={'text': f"<i>Bitte wählen Sie mind. einen Teilbereich aus,<br>um Daten einzusehen<i>.",
                   'y': 0.6,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'font': dict(
                       size=16,
                       color='#808080',
                       family='Arial, sans-serif')})

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False)

        return fig

"""
-----------------------------------------------------------------------------------------
Section 5:
Tab 2: Define Graph 3 - Linechart (Allgemein Männer vs Frauen)
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
                  color_discrete_map={'Männer': '#0D9CF9', 'Frauen': '#EE1154'})

    fig.update_traces(marker=dict(size=12, symbol='circle', line=dict(width=1.5, color='#808080')),
                      mode='markers+lines',
                      line=dict(width=4))

    fig.update_xaxes(dtick=1,
                     tickangle=45,
                     tickmode='linear',
                     tick0=filtered_df['Jahr'].min(),
                     showgrid=False,
                     showticklabels=True,
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080')

    fig.update_yaxes(showgrid=False,
                     showticklabels=True,
                     ticks='outside',
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080',
                     tickformat = ".2f",
                     range=[7.80, 8.30])

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis_title="",
        yaxis_title="Zufriedenheits-Index",
        font=dict(color='#808080', size=14, family='Arial, sans-serif'))

    return fig

"""
-----------------------------------------------------------------------------------------
Section 6:
Tab 2: Define Graph 4 - Scatter-Plot (Frauen vs. Männer)
"""

@app.callback(
    Output('graph_4', 'figure'),
    Input('dropdown_4', 'value'),
    Input('slider_3', 'value'))

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
                         color_discrete_map={'Männer': '#0D9CF9', 'Frauen': '#EE1154'})

        fig.update_traces(marker=dict(size=12, line=dict(width=1.5, color='#808080')))

        fig.update_xaxes(showgrid=False,
                         showticklabels=True,
                         tickangle=45,
                         ticks='outside',
                         tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         tickcolor='#808080',
                         tickformat=".2f",
                         dtick=0.1)
                         #range=[6.70, 9.50])

        fig.update_yaxes(showgrid=False,
                         showticklabels=True,
                         ticks='outside',
                         tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         tickcolor='#808080',
                         tickformat=".2f",
                         range=[7.80, 8.30])

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            bargap=0.05,
            xaxis_title=f"{col_menue}",
            yaxis_title="Allgemeine Zufriedenheit",
            font=dict(color='#808080', size=14, family='Arial, sans-serif'),
            title={
                'text': f"<i>Vergleich mit {col_menue}<i>",
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=16,
                    color='white',
                    family='Arial, sans-serif')})

        return fig

    else:
        fig = px.scatter()

        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            font=dict(color='#808080'),
            title={'text': f"<i>Bitte wählen Sie einen Teilbereich aus,<br>um Daten einzusehen</i>.",
                   'y': 0.6,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top',
                   'font': dict(
                       size=16,
                       color='#808080',
                       family='Arial, sans-serif')})

        fig.update_xaxes(showgrid=False, zeroline=False, showline=False)
        fig.update_yaxes(showgrid=False, zeroline=False, showline=False)

        return fig

if __name__ == '__main__':
    # run the app in server port 8051:
    app.run_server(port=8051, debug=True)
