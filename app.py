import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go

# Sample data (replace with actual dataset)
data = {
    'Date': pd.date_range(start='2024-01-01', periods=12, freq='ME'),
    'Sales': [120, 115, 110, 95, 90, 88, 87, 89, 85, 83, 82, 80],
    'Price': [1.50]*3 + [1.80]*9
}
df = pd.DataFrame(data)

# Detect price increase date
price_increase_date = df[df['Price'] > df['Price'].iloc[0]].iloc[0]['Date']

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Impact of Price Increase on Pink Morsels Sales"),
    dcc.Graph(
        figure={
            'data': [
                go.Scatter(
                    x=df['Date'],
                    y=df['Sales'],
                    mode='lines+markers',
                    name='Sales'
                )
            ],
            'layout': go.Layout(
                title='Sales Over Time',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Units Sold'},
                shapes=[
                    {
                        'type': 'line',
                        'x0': price_increase_date,
                        'x1': price_increase_date,
                        'y0': 0,
                        'y1': max(df['Sales']),
                        'line': {'color': 'red', 'width': 2, 'dash': 'dash'}
                    }
                ],
                annotations=[
                    {
                        'x': price_increase_date,
                        'y': max(df['Sales']),
                        'text': 'Price Increase',
                        'showarrow': True,
                        'arrowhead': 2,
                        'ax': -40,
                        'ay': -40
                    }
                ]
            )
        }
    )
])

if __name__ == '__main__':
    app.run(debug=True)
