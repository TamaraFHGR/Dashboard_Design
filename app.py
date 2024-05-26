from dash import Dash, dcc, html, Input, Output, State
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
    # Theme Dropdown:
    html.Div([
        html.Div(
            dcc.Dropdown(
                id='theme_dropdown',
                options=[
                    {'label': 'Light Mode', 'value': 'light'},
                    {'label': 'Dark Mode', 'value': 'dark'}],
                value='dark',
                clearable=False,
                style={'width': '100%'},
                className=''),
            className='dropdown-container'
        ),
        html.Button("Für Kontext-Info hier klicken", id='text_button', className='text_button')
    ], className='theme_dropdown'),

    # Hidden Text Box:
    html.Div(id='text_box', className='text_box', children=[
        html.H3("In einer jährlichen Umfrage wird das subjektive Wohlbefinden der Schweizer Bevölkerung erhoben. Dabei"
                " wird die allgemeine Lebenszufriedenheit auf einer Skala von 0 bis 10 bewertet:"
                " 0 = gar nicht zufrieden, 10 = vollständig zufrieden. Neben der generellen Zufriedenheit"
                " wird auch die Zufriedenheit in nachfolgenden Lebensbereichen gemessen:"),
        html.Div(className='text_box_content', children=[
            html.Div([
                html.Ul([
                    html.Li("die finanzielle Lage"),
                    html.Li("das Alleinleben"),
                    html.Li("das Zusammenleben"),
                    html.Li("persönliche Beziehungen")
                ], className='first-column')
            ]),
            html.Div([
                html.Ul([
                    html.Li("die Gesundheit"),
                    html.Li("die Wohnsituation"),
                    html.Li("die Arbeitsbedingungen"),
                    html.Li("das Arbeitsklima")
                ], className='second-column'),
            ]),
        ]),
        html.H3("Quelle: © BFS – Erhebung über die Einkommen und Lebensbedingungen, Datenstand: 20.12.2023")
    ]),

    # Header:
    html.Div([
    html.H1("Dashboard zur Zufriedenheit in der Schweiz – Exploration der subjektiven Lebensqualität"),
    ], className='header'),

    # Tabs:
    dcc.Tabs(id='tabs', value='tab_1', children=[

        # Tab 1:
        dcc.Tab(id='tab_1', label='Gesamtanalyse Schweiz', value='tab_1', className='tab dark-tab', selected_className='tab-active', children=[
            html.Div([
                html.Div([
                    html.Div(
                        id='container_1',
                        children=[
                            html.H4("Entwicklung der allgemeinen Zufriedenheit"),
                            dbc.Button('Info', id='hover-button_1', n_clicks=0, className="hover-button"),
                            dbc.Tooltip(
                                "Das Liniendiagramm zeigt die erhobenen Mittelwerte der 'allgemeinen Zufriedenheit' der "
                                " Gesamtbevölkerung in der Schweiz pro Jahr.",
                                target='hover-button_1'),
                            dcc.Graph(id='graph_1', style={'height': '250px'}),
                            html.P("Auswahl der Analyse-Jahre:"),
                            dcc.RangeSlider(
                                id='slider_1',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()])
                        ], className='container_1',
                    )
                ], className="two columns"),
                html.Div([
                    html.Div(
                        id='container_2',
                        children=[
                            html.H4("Zufriedenheit in verschiedenen Teilbereichen"),
                            dbc.Button('Info', id='hover-button_2', n_clicks=0, className="hover-button"),
                            dbc.Tooltip(
                                "Das Streudiagramm ermöglicht den Vergleich zwischen verschiedenen Teilbereichen"
                                " und der 'allgemeinen Zufriedenheit'. Sie können eine oder mehrere Variablen aus dem Dropdown-Menü"
                                " auswählen, um zu sehen, ob ein Zusammenhang zwischen den Variablen besteht. Darüber hinaus zeigt"
                                " die Grafik, in welchen Teilbereichen die Bevölkerung am zufriedensten oder am wenigsten zufrieden ist.",
                                target='hover-button_2'),
                            dcc.Graph(id='graph_2', style={'height': '250px'}),
                            html.P("Bitte wählen Sie die gewünschten Teilbereiche aus:"),
                            dcc.Dropdown(
                                id='dropdown_2',
                                options=[{'label': col, 'value': col} for col in df.columns[4:]],
                                value=None,
                                multi=True,
                                className='dark-dropdown-menu')
                        ], className='container_2',
                    )
                ], className="two columns")
            ],className="row")
        ]),

        # Tab 2:
        dcc.Tab(id='tab_2', label='Analyse nach Geschlecht', value='tab_2', className='tab dark-tab', selected_className='tab-active', children=[
            html.Div([
                html.Div([
                    html.Div(
                        id='container_3',
                        children=[
                            html.H4("Entwicklung der allgemeinen Zufriedenheit, aufgeteilt nach Geschlecht"),
                            dbc.Button('Info', id='hover-button_3', n_clicks=0, className="hover-button"),
                            dbc.Tooltip(
                                "Das Liniendiagramm zeigt die durchschnittliche 'allgemeine Zufriedenheit' der Schweizer Bevölkerung,"
                                " aufgeschlüsselt nach Geschlecht.",
                                target='hover-button_3'),
                            dcc.Graph(id='graph_3', style={'height': '250px'}),
                            html.P("Auswahl der Analyse-Jahre:"),
                            dcc.RangeSlider(
                                id='slider_3',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()]),
                        ], className='container_3',
                    )
                ], className="two columns"),
                html.Div([
                    html.Div(
                        id='container_4',
                        children=[
                            html.H4("Zufriedenheit in verschiedenen Teilbereichen, aufgeteilt nach Geschlecht"),
                            dbc.Button('Info', id='hover-button_4', n_clicks=0, className="hover-button"),
                            dbc.Tooltip(
                                "Das Streudiagramm vergleicht einen Teilbereich mit der 'allgemeinen Zufriedenheit'."
                                " Sie können die gewünschte Variable aus dem Dropdown-Menü auswählen. Daraus lassen sich"
                                " Unterschiede oder Ähnlichkeiten zwischen der Zufriedenheit von Männer und Frauen erschliessen.",
                                target='hover-button_4'),
                            dcc.Graph(id='graph_4', style={'height': '250px'}),
                            html.P("Bitte wählen Sie einen Teilbereich aus:"),
                            dcc.Dropdown(
                                id='dropdown_4',
                                options=[{'label': col, 'value': col} for col in df.columns[4:]],
                                value=None,
                                multi=False,
                                className='dark-dropdown-menu')
                        ], className='container_4',
                    )
                ], className="two columns")
            ], className="row")
        ]),

        # Tab 3:
        dcc.Tab(id='tab_3', label='Analyse nach demografischen Merkmalen', value='tab_3', className='tab dark-tab', selected_className='tab-active', children=[
            html.Div([
                html.Div([
                    html.Div(
                        id='container_5',
                        children=[
                            html.H4("Entwicklung der allgemeinen Zufriedenheit in verschiedenen Alterskategorien"),
                            dbc.Button('Info', id='hover-button_5', n_clicks=0, className="hover-button"),
                            dbc.Tooltip(
                                "...",
                                target='hover-button_5'),
                            dcc.Graph(id='graph_5', style={'height': '250px'}),
                            html.P("Auswahl der Analyse-Jahre:"),
                            dcc.RangeSlider(
                                id='slider_5',
                                min=df['Jahr'].min(),
                                max=df['Jahr'].max(),
                                step=1,
                                marks={str(year): str(year) for year in df['Jahr'].unique()},
                                value=[df['Jahr'].min(), df['Jahr'].max()])
                        ], className='container_5',
                    )
                ], className="two columns"),
                html.Div([
                    html.Div(
                        id='container_6',
                        children=[
                            html.H4("Vergleich der Zufriedenheit in verschiedenen Teilbereichen und Alterskategorien"),
                            dbc.Button('Info', id='hover-button_6', n_clicks=0, className="hover-button"),
                            dbc.Tooltip("...",  target='hover-button_6'),
                            dcc.Graph(id='graph_6', style={'height': '250px'}),
                            html.P("Bitte wählen Sie eine Variable aus:"),
                            dcc.Dropdown(
                                id='dropdown_6',
                                options=[{'label': col, 'value': col} for col in df.columns[3:]],
                                value='Allgemein',
                                multi=False,
                                className='dark-dropdown-menu')
                        ], className='container_6',
                    )
                ], className="two columns")
            ], className="row")
        ]),
    ])
], id='page_content', className='container')



"""
-----------------------------------------------------------------------------------------
Section 3:
Select Theme Mode
"""
@app.callback(
    [Output('page_content', 'style'),
     Output('dropdown_2', 'className'),
     Output('dropdown_4', 'className'),
     Output('dropdown_6', 'className'),
     Output('theme_dropdown', 'className'),
     Output('tab_1', 'className'),
     Output('tab_2', 'className'),
     Output('tab_3', 'className')],
    [Input('theme_dropdown', 'value')]
)
def update_theme(selected_theme):
    if selected_theme == 'dark':
        page_style = {'backgroundColor': '#12163b', 'color': 'white', 'padding': '20px'}
        dropdown_class = 'dark-dropdown-menu'
        tab_class = 'dark-tab'
    else:
        page_style = {'backgroundColor': '#EEEEEE', 'color': 'black', 'padding': '20px'}
        dropdown_class = 'light-dropdown-menu'
        tab_class = 'light-tab'

    return page_style, dropdown_class, dropdown_class, dropdown_class, dropdown_class, tab_class, tab_class, tab_class

"""
-----------------------------------------------------------------------------------------
Section 4:
Kontext Info Box
"""

@app.callback(
    Output('text_box', 'style'),
    Input('text_button', 'n_clicks'),
    State('text_box', 'style')
)
def toggle_text_box(n_clicks, current_style):
    if n_clicks is None:
        return {'display': 'none'}

    if current_style['display'] == 'none':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


"""
-----------------------------------------------------------------------------------------
Section 5:
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

    fig.update_traces(marker=dict(size=8, symbol='circle', line=dict(width=0.5, color='#808080')),
                      line=dict(color='#04AAE9', width=4),
                      mode='markers+lines')

    fig.update_xaxes(dtick=2,
                     tickangle=0,
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
        xaxis_title=None,
        yaxis_title="Zufriedenheits-Index",
        font=dict(color='#808080', size=14, family='Arial, sans-serif'),
        margin=dict(l=40, r=20, t=20, b=10),
        legend_title_text='')

    return fig

"""
-----------------------------------------------------------------------------------------
Section 6:
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
                         trendline='ols',
                         color_discrete_sequence=px.colors.qualitative.Dark24)

        fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color='#808080')))

        fig.update_xaxes(showgrid=False,
                         showticklabels=True,
                         tickangle=0,
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
            xaxis_title=None,
            yaxis_title="Allgemeine Zufriedenheit",
            font=dict(color='#808080', size=14, family='Arial, sans-serif'),
            title={
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=16,
                    family='Arial, sans-serif')},
            margin=dict(l=40, r=20, t=20, b=10),
            legend_title_text='')

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
Section 7:
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
                  color_discrete_map={'Männer': '#41A1C6', 'Frauen': '#AA8539'})

    fig.update_traces(marker=dict(size=8, symbol='circle', line=dict(width=0.5, color='#808080')),
                      mode='markers+lines',
                      line=dict(width=4))

    fig.update_xaxes(dtick=2,
                     tickangle=0,
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
        font=dict(color='#808080', size=14, family='Arial, sans-serif'),
        margin=dict(l=40, r=20, t=20, b=10),
        legend_title_text='')

    return fig

"""
-----------------------------------------------------------------------------------------
Section 8:
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
                         trendline='ols',
                         color_discrete_map={'Männer': '#41A1C6', 'Frauen': '#AA8539'})

        fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color='#808080')))

        fig.update_xaxes(showgrid=False,
                         showticklabels=True,
                         tickangle=0,
                         ticks='outside',
                         tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                         tickcolor='#808080',
                         tickformat=".2f",
                         dtick=0.2)
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
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(
                    size=16,
                    family='Arial, sans-serif')},
            margin=dict(l=40, r=20, t=20, b=10),
            legend_title_text='')

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

"""
-----------------------------------------------------------------------------------------
Section 9:
Tab 3: Define Graph 5 - Linechart (Alterskategorien)
"""
@app.callback(
    Output('graph_5', 'figure'),
        Input('slider_5', 'value'))

def update_graph_5(selected_years):
    min_year, max_year = selected_years
    # Daten filtern, um nur Daten ohne Geschlecht zu erhalten
    filtered_df = df[
        (df['Jahr'] >= min_year) & (df['Jahr'] <= max_year) & (df['Geschlecht'].isna())]

    fig = px.line(filtered_df,
                  x='Jahr',
                  y='Allgemein',
                  color='Alterskategorie',
                  color_discrete_map={'16-17 Jahre': '#7fc97f',
                                      '18-24 Jahre': '#beaed4',
                                      '25-49 Jahre': '#fdc086',
                                      '50-64 Jahre': '#ffff99',
                                      '65 Jahre +': '#386cb0'})

    fig.update_traces(marker=dict(size=8, symbol='circle', line=dict(width=0.5, color='#808080')),
                      mode='markers+lines',
                      line=dict(width=4))

    fig.update_xaxes(dtick=2,
                     tickangle=0,
                     tickmode='linear',
                     tick0=filtered_df['Jahr'].min(),
                     showgrid=False,
                     showticklabels=True,
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080')

    fig.update_yaxes(dtick=0.2,
                     showgrid=False,
                     showticklabels=True,
                     ticks='outside',
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080',
                     tickformat = ".2f",
                     range=[7.60, 8.90])

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis_title="",
        yaxis_title="Zufriedenheits-Index",
        font=dict(color='#808080', size=14, family='Arial, sans-serif'),
        margin=dict(l=40, r=20, t=20, b=10),
        legend_title_text='')

    return fig

"""
-----------------------------------------------------------------------------------------
Section 10:
Tab 3: Define Graph 6 - Barchart (Alterskategorien)
"""
@app.callback(
    Output('graph_6', 'figure'),
    Input('slider_5', 'value'),
    Input('dropdown_6', 'value')
)
def update_graph_6(selected_years, selected_variable):
    min_year, max_year = selected_years
    # Daten filtern, um nur Daten ohne Geschlecht zu erhalten
    filtered_df = df[
        (df['Jahr'] >= min_year) & (df['Jahr'] <= max_year) & (df['Geschlecht'].isna())]

    # Mittelwert der ausgewählten Variablen für jede Alterskategorie berechnen
    mean_df = filtered_df.groupby('Alterskategorie')[selected_variable].mean().reset_index()

    fig = px.bar(mean_df,
                 x=selected_variable,
                 y='Alterskategorie',
                 orientation='h',
                 color='Alterskategorie',
                 text='Alterskategorie',
                 color_discrete_map={'16-17 Jahre': '#7fc97f',
                                     '18-24 Jahre': '#beaed4',
                                     '25-49 Jahre': '#fdc086',
                                     '50-64 Jahre': '#ffff99',
                                     '65 Jahre +': '#386cb0'})

    fig.update_traces(marker=dict(line=dict(width=0.5, color='#808080')),
                      textposition='inside',
                      textfont=dict(color='black', size=14, family='Arial, sans-serif'))

    fig.update_xaxes(showgrid=False,
                     showticklabels=True,
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080')

    fig.update_yaxes(showgrid=False,
                     showticklabels=False,
                     ticks=None,
                     tickfont=dict(color='#808080', size=14, family='Arial, sans-serif'),
                     tickcolor='#808080')

    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis_title=selected_variable,
        yaxis_title=None,
        font=dict(color='#808080', size=14, family='Arial, sans-serif'),
        margin=dict(l=40, r=20, t=20, b=10),
        legend_title_text='',
        showlegend=False)

    return fig




if __name__ == '__main__':
    # run the app in server port 8051:
    app.run_server(port=8051, debug=True)
