# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

df2 = pd.read_csv('https://plotly.github.io/datasets/country_indicators.csv')

#lista de figuras
fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

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

    html.Br(),

    html.Div([

        html.Div([
             dcc.Dropdown(
                 df2['Indicator Name'].unique(),
                 'Fertility rate, total (births per woman)',
                 id='xaxis-column'
             ),
             dcc.RadioItems(
                 ['Linear', 'Log'],
                 'Linear',
                 id='xaxis-type',
                 inline=True
             )
             ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                df2['Indicator Name'].unique(),
                'Life expectancy at birth, total (years)',
                id='yaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        df2['Year'].min(),
        df2['Year'].max(),
        step=None,
        id='year--slider',
        value=df2['Year'].max(),
        marks={str(year): str(year) for year in df2['Year'].unique()},

    ),

    html.Br(),

    dcc.Input(
        id='num-multi',
        type='number',
        value=5
    ),
    html.Table([
        html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
        html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
        html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
        html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
        html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
    ]),

])

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


@app.callback(
    Output('square', 'children'),#id do que estou modificando e parâmetro ue quero que seja modificado
    Output('cube', 'children'),
    Output('twos', 'children'),
    Output('threes', 'children'),
    Output('x^x', 'children'),
    Input('num-multi', 'value'))
def callback_a(value):
    value = 1 if value is None else int(value)
    return value**2, value**3, 2**value, 3**value, value**value





@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    Input('xaxis-type', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value'))
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 year_value):
    dff = df2[df2['Year'] == year_value]

    fig = px.scatter(x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
                     y=dff[dff['Indicator Name'] ==
                           yaxis_column_name]['Value'],
                     hover_name=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'])

    fig.update_layout(
        margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type='linear' if xaxis_type == 'Linear' else 'log')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
