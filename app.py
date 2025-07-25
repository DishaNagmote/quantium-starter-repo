import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Simulated sample data
regions = ['north', 'east', 'south', 'west']
dates = pd.date_range(start='2024-01-01', periods=12, freq='ME')
sales_pattern = [120, 115, 110, 95, 90, 88, 87, 89, 85, 83, 82, 80]
price_pattern = [1.50]*3 + [1.80]*9

df = pd.DataFrame({
    'date': np.tile(dates, len(regions)),
    'region': np.repeat(regions, len(dates)),
    'sales': sales_pattern * len(regions),
    'price': price_pattern * len(regions)
})

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Dashboard"),

    dcc.Dropdown(
        id='region-selector',
        options=[{'label': r.title(), 'value': r} for r in regions],
        value='north'
    ),

    dcc.Graph(id='sales-graph')
])

@app.callback(
    Output('sales-graph', 'figure'),
    Input('region-selector', 'value')
)
def update_graph(selected_region):
    filtered_df = df[df['region'] == selected_region]
    return {
        'data': [go.Scatter(x=filtered_df['date'], y=filtered_df['sales'], mode='lines+markers')],
        'layout': go.Layout(title=f'Sales in {selected_region.title()}', xaxis={'title': 'Date'}, yaxis={'title': 'Sales'})
    }

if __name__ == '__main__':
    app.run(debug=True)
