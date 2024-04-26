from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Initializing Dash-App:
app = Dash(__name__)

# Data reading:
data_path = 'assets/Hallwilersee_Halfmarathon.csv'
df = pd.read_csv(data_path, sep=';')

"""
columns:
df['Event_Year']
df['Running_Time_min']
df['Speed_km_h']
df['Runner_Age']
df['Runner_Gender']
"""
median = df.groupby('Event_Year')['Running_Time_min'].median()
max = df.groupby('Event_Year')['Running_Time_min'].max()
min = df.groupby('Event_Year')['Running_Time_min'].min()

# df_Frauen:
df_w = df[df['AG'].str.startswith('W')]
avg_laufzeit_w = df_w.groupby('AG')['Running_Time_min'].median()
counts_w = df_w['AG'].value_counts().loc[avg_laufzeit_w.index]  # Ensuring the order matches avg_laufzeit

# df_Männer:
df_m = df[df['AG'].str.startswith('M')]
avg_laufzeit_m = df_m.groupby('AG')['Running_Time_min'].median()
counts_m = df_m['AG'].value_counts().loc[avg_laufzeit_m.index]  # Ensuring the order matches avg_laufzeit

# print(df['Event_Name'].unique())

# App Layout:
app.layout = html.Div([
    # Header-Bereich:
    html.Div(
        id='header-area',
        children=[
            html.H1('Laufzeiten-Analyse von Schweizer Laufevents'),
            html.P("Analyse der Laufzeiten von Schweizer Laufevents von 1999 - 2019")
        ]
    ),
    # Event-Filter
    html.Div(
        id='dropdown-area',
        children=[
            html.H2("Wählen Sie ein Laufevent:"),
            html.P("Dieses Dropdown ermöglicht Ihnen die Auswahl des Laufevents."),
            dcc.Dropdown(
                id='dropdown_event',
                options=[{'label': event, 'value': event} for event in df['Event_Name'].unique()],
                multi=False
            ),
        ]
    ),
    # Zeile 1:
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="main_graph"),
            width=12)
    ]),
    # Zeile 2:
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="bar_female"),
            width=1),
        dbc.Col(
            dcc.Graph(id="bar_male"),
            width=1)
    ])
])

# Callback main_graph:
@app.callback(
    Output('main_graph', 'figure'),
    [Input('dropdown_event', 'value')])

# Scatterplot
def update_main_graph(dropdown_value_event):
    # Scatterplot erstellen:
    fig = px.scatter(df,
        x='Event_Year',
        y='Running_Time_min',
        color='Speed_km_h',
        color_continuous_scale='aggrnyl',
        hover_data=('Runner_Age', 'Runner_Gender')
        )    # temps #rdylgn #greens #greys
    # Layout für Scatterplot anpassen:
    fig.update_traces(
        marker=dict(size=17, line=dict(width=0))
    )
    # Gesamtlayout anpassen:
    fig.update_layout(
        title='Laufzeiten Hallwilersee-Halbmarathon',
        title_font=dict(size=20, color='grey'),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(y=1.1, x=0.8)
    )
    # Y-Achse bearbeiten:
    fig.update_yaxes(
        autorange="reversed",
        showgrid=False,
        showticklabels=True,
        ticks="outside",
        tickfont=dict(color='grey'),
        title_text='Laufzeit in Minuten',
        title_font=dict(size=14, color='grey')
    )
    # X-Achse bearbeiten:
    fig.update_xaxes(
        tickvals=list(range(1999, 2020)),
        showgrid=False,
        showticklabels=True,
        ticks="outside",
        tickfont=dict(color='grey'),
        title_text='Event Jahr',
        title_font=dict(size=14, color='grey')
    )
    # Liniendiagramm für Median hinzufügen:
    median_trace = px.line(
        x=median.index,
        y=median.values,
        labels={'x': 'Jahr', 'y': 'Laufzeit in Minuten'}).data[0]
    median_trace.update(
        line=dict(color='grey', width=2, dash='dot'),
        mode='lines',
        name='Median',
        showlegend=True
    )
    fig.add_trace(median_trace)
    # Liniendiagramm für Min hinzufügen:
    min_trace = px.line(
        x=min.index,
        y=min.values,
        labels={'x': 'Jahr', 'y': 'Laufzeit in Minuten'}).data[0]
    min_trace.update(
        line=dict(color='#edf05e', width=2, dash='dot'),
        mode='lines',
        name='Schnellster Läufer',
        showlegend=True
    )
    fig.add_trace(min_trace)
    # Liniendiagramm für Max hinzufügen:
    max_trace = px.line(
        x=max.index,
        y=max.values,
        labels={'x': 'Jahr', 'y': 'Laufzeit in Minuten'}).data[0]
    max_trace.update(
        line=dict(color='#24576a', width=2, dash='dot'),
        mode='lines',
        name='Langsamster Läufer',
        showlegend=True
    )
    fig.add_trace(max_trace)
    return fig

# Callback bar_female:
@app.callback(
    Output('bar_female', 'figure'),
    [Input('dropdown_event', 'value')])

# Bar Chart Female:
def update_bar_female(dropdown_value_event):
    fig = make_subplots(
        specs=[[{"secondary_y": True}]])
    # Histogramm erstellen:
    fig.add_trace(go.Bar(
        x=counts_w.index,
        y=counts_w.values,
        name='Anzahl Läuferinnen',
        marker_color='#15947f'),
        secondary_y=False
    )
    # Liniendiagramm auf Sekundärachse hinzufügen:
    fig.add_trace(go.Scatter(
        x=avg_laufzeit_w.index,
        y=avg_laufzeit_w.values,
        mode='lines+markers',
        name='Durchschnittliche Laufzeit',
        line=dict(color='grey', width=3, dash='dot')),
        secondary_y=True
    )
    # Gesamtlayout anpassen:
    fig.update_layout(
        title='Female-Runners',
        title_font=dict(size=24, color='grey'),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    # Y-Sekundärachse bearbeiten:
    fig.update_yaxes(
        title_text='Laufzeit in Minuten',
        secondary_y=True,
        title_font=dict(size=14, color='grey'),
        tickfont=dict(color='grey')
    )
    # Y-Primärachse bearbeiten:
    fig.update_yaxes(
        title_text='Anzahl Läuferinnen',
        secondary_y=False,
        title_font=dict(size=14, color='grey'),
        tickfont=dict(color='grey')
    )
    # X-Achse bearbeiten:
    fig.update_xaxes(
        title_text='Alterskategorie',
        title_font=dict(size=14, color='grey'),
        tickfont=dict(color='grey'))
    return fig

# Callback bar_male:
@app.callback(
    Output('bar_male', 'figure'),
    [Input('dropdown_event', 'value')])

# Bar Chart Male:
def update_bar_male(dropdown_value_event):
    fig = make_subplots(
        specs=[[{"secondary_y": True}]])
    # Histogramm erstellen:
    fig.add_trace(go.Bar(
        x=counts_m.index,
        y=counts_m.values,
        name='Anzahl Läufer',
        marker_color='#15947f'),
        secondary_y=False
    )
    # Liniendiagramm auf Sekundärachse hinzufügen:
    fig.add_trace(go.Scatter(
        x=avg_laufzeit_m.index,
        y=avg_laufzeit_m.values,
        mode='lines+markers',
        name='Durchschnittliche Laufzeit',
        line=dict(color='grey', width=3, dash='dot')),
        secondary_y=True
    )
    # Gesamtlayout anpassen:
    fig.update_layout(
        title='Male-Runners',
        title_font=dict(size=24, color='grey'),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    # Y-Sekundärachse bearbeiten:
    fig.update_yaxes(
        title_text='Laufzeit in Minuten',
        secondary_y=True,
        title_font=dict(size=14, color='grey'),
        tickfont=dict(color='grey')
    )
    # Y-Primärachse bearbeiten:
    fig.update_yaxes(
        title_text='Anzahl Läufer',
        secondary_y=False,
        title_font=dict(size=14, color='grey'),
        tickfont=dict(color='grey')
    )
    # X-Achse bearbeiten:
    fig.update_xaxes(
        title_text='Alterskategorie',
        title_font=dict(size=14, color='grey'),
        tickfont=dict(color='grey'))
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
