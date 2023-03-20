from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date
import random
import plotly.graph_objs as go
# from flask import Flask, redirect, url_for, render_template_string
# from flask_login import LoginManager
# server = Flask(__name__)
# server.secret_key = 'secretkey'

# login_manager = LoginManager()
app = Dash(__name__)
server = app.server



#lista de dataframes
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)
date_range = end_date - start_date
dates = [start_date + timedelta(days=i) for i in range(date_range.days + 1)]

df_sales = pd.DataFrame({
    "Date": dates,
    "Total Sold": [random.randint(1000, 5000) for _ in range(len(dates))]
})

#lista de figuras
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
fig2 = px.line(df_sales, x="Date", y="Total Sold")
fig3 = px.bar(df_sales, x='Date', y='Total Sold')


app.layout = html.Div(children=[
    html.H1(children='Charts examples in plotly'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    html.H3(children='''
        Example 1: simple bar chart
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    ),


    html.Div(children=[
        html.H3(children='''
        Example 2: simple bar chart with a dropdown
    '''),
        html.Div([
             dcc.Dropdown(
                 df['Fruit'].unique(),
                 'Bananas',
                 id='example2-dropdown-values'
             ),
             ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div(children=[
            dcc.Graph(id='example-graph-2', figure=fig)
        ]),
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div(children=[
        html.H3(children='''
        Example 3: simple bar chart with a radio select
    '''),
        html.Div([
            dcc.RadioItems(
                 df['City'].unique(),
                 'SF',
                 id='example3-radio-values',
                 inline=True
                 )
        ], style={'width': '48%', 'display': 'inline-block'}),
        html.Div(children=[
            dcc.Graph(id='example-graph-3', figure=fig)
        ]),
    ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div(children=[
        html.H3(children='''
        Example 4: line chart with a date picker range
    '''),

        # Add a date picker
        dcc.DatePickerRange(
            id='my-date-picker-range',
            start_date=date.today() - timedelta(days=14),
            end_date=date.today(),
            max_date_allowed=date.today()
        ),

        dcc.Graph(
            id='example-graph-4',
            figure=fig2
        ),
    ]
        , style={'width': '60%', 'display': 'inline-block'}),

   
   html.Div(children=[
       html.H3(children='''
        Example 6: bar chart with date picker range
    '''),

       dcc.Graph(id='example-graph-6'),
   ], style={'width': '40%', 'display': 'inline-block'}),

   
    html.H3(children='''
        Example 7: text input
    '''),

    html.Div(children='''
        Enter text to add a new div:
    '''),

    html.Div(children=[
        dcc.Input(id='example7-input', value='', type='text'),
        html.Button('Add', id='example7-button'),
    ]),
    html.Div(id='example7-output'),

    html.H3(children='''
        Example 8: text area
    '''),

    html.Textarea(),

    html.H3(children='''
        Example 9: Gráfico de barras dinâmico
    '''),

    html.P(children='''
        Insira dados separados por vírgula ou quebra de linha. Após isto, surgirá um gráfico que conta quantas vezes um dado elemento aparece na lista
    '''),

    html.Div([
        dcc.Textarea(
            id='input-box-example9',
            placeholder='Insira dados separados por vírgula ou quebra de linha',
            style={'width': '100%', 'height': 100}
        ),
        html.Button('Gerar Gráfico', id='button9'),
    ]),

    dcc.Graph(id='output-graph9'),

])




#------------- Exemplo 9 -------------------------
@app.callback(Output('output-graph9', 'figure'),
              Input('button9', 'n_clicks'),
              State('input-box-example9', 'value'))
def update_figure(n_clicks, input_value):
    if input_value:
        data = input_value.strip().replace('\n', ',').replace(',', ' ').split()
        df = pd.DataFrame({'Data': data})
        counts = df['Data'].value_counts()
        fig = go.Figure(data=[go.Bar(x=counts.index, y=counts)])
        fig.update_layout(title='Contagem de Dados',
                          xaxis_title='Dados', yaxis_title='Contagem')
        return fig
    else:
        return {}

#--------------- Exemplo 7 -------------------------
@app.callback(
    Output('example7-output', 'children'),
    Input('example7-button', 'n_clicks'),
    # obtem o valor atual do componente dcc.Input
    State('example7-input', 'value'),
    # obtem a lista atual de divs que já foram adicionados.
    State('example7-output', 'children')
)
def add_div(n_clicks, value, existing_children):
    if existing_children is None:
        existing_children = []
    if n_clicks and value:
        new_child = html.Div(children=value)
        children = [new_child]+existing_children
        return children
    else:
        return existing_children


#--------------- Exemplo 6 -------------------------
@app.callback(
    Output('example-graph-6', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_bar_chart(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the df_sales dataframe to include only the rows with dates between start_date and end_date
    filtered_df = df_sales[df_sales['Date'].between(start_date, end_date)]

    # Create a bar chart of the filtered data
    fig = px.bar(filtered_df, x='Date', y='Total Sold')
    return fig

#--------------- Exemplo 4 -------------------------
@app.callback(
    Output('example-graph-4', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date')
)
def update_chart(start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Filter the df_sales dataframe to include only the rows with dates between start_date and end_date
    filtered_df = df_sales[df_sales['Date'].between(start_date, end_date)]

    # Create a plot of the filtered data
    fig = px.line(filtered_df, x='Date', y='Total Sold')
    return fig



@app.callback(
    Output('example-graph-2', 'figure'),
    Input('example2-dropdown-values', 'value')
)
def filter_fruit(fruit):
    dff = df[df['Fruit'] == fruit]
    fig = px.bar(dff, x="Fruit", y="Amount", color="City", barmode="group")
    return fig


@app.callback(
    Output('example-graph-3', 'figure'),
    Input('example3-radio-values', 'value')
)
def filter_fruit(city):
    dff = df[df['City'] == city]
    fig = px.bar(dff, x="Fruit", y="Amount", color="City", barmode="group")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
