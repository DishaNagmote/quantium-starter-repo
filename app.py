import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go
import numpy as np

# Simulated sample data
regions = ['north', 'east', 'south', 'west']
dates = pd.date_range(start='2024-01-01', periods=12, freq='ME')

# Create dataset with same lengths
sales_pattern = [120, 115, 110, 95, 90, 88, 87, 89, 85, 83, 82, 80]
price_pattern = [1.50]*3 + [1.80]*9

df = pd.DataFrame({
    'Date': np.tile(dates, len(regions)),  # 12 * 4 = 48
    'Sales': sales_pattern * len(regions),
    'Price': price_pattern * len(regions),
    'Region': np.repeat(regions, 12)
})

# Find the date of first price increase
price_increase_date = df[df['Price'] > 1.50].iloc[0]['Date']

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div(className="app-container", children=[
    html.H1("Impact of Price Increase on Pink Morsels Sales"),

    html.Div(className="radio-container", children=[
        html.Label("Select Region:"),
        dcc.RadioItems(
            id='region-selector',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            labelStyle={'display': 'block'}
        )
    ]),

    dcc.Graph(id='sales-graph')


])

@app.callback(
    Output('sales-graph', 'figure'),  # ✅ match layout
    Input('region-selector', 'value')
)

def update_chart(region):
    if region == 'all':
        filtered_df = df.groupby('Date', as_index=False)['Sales'].mean()
    else:
        filtered_df = df[df['Region'] == region]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=filtered_df['Date'],
        y=filtered_df['Sales'],
        mode='lines+markers',
        name='Sales'
    ))

    fig.update_layout(
        title=f"Sales Over Time ({region.title() if region != 'all' else 'All Regions'})",
        xaxis_title='Date',
        yaxis_title='Units Sold',
        shapes=[
            {
                'type': 'line',
                'x0': price_increase_date,
                'x1': price_increase_date,
                'y0': 0,
                'y1': max(filtered_df['Sales']),
                'line': {'color': 'red', 'width': 2, 'dash': 'dash'}
            }
        ],
        annotations=[
            {
                'x': price_increase_date,
                'y': max(filtered_df['Sales']),
                'text': 'Price Increase',
                'showarrow': True,
                'arrowhead': 2,
                'ax': -40,
                'ay': -40
            }
        ]
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)
