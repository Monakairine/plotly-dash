from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta, date
import random

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


    html.H3(children='''
        Example 5: text input
    '''),

    html.Div(children='''
        Enter text to add a new div:
    '''),

    dcc.Input(id='example5-input', value='', type='text'),

    html.Div(id='example5-output'),

])


@app.callback(
    Output('example5-output', 'children'),
    Input('example5-input', 'value'),
    State('example5-output', 'children')
)
def add_div(value, existing_children):

    existing_children = html.Div()
    if value:
        new_child = html.Div(children=value)
        children = [new_child] + existing_children
        return children
    else:
        return existing_children


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
