import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv('filtered_pink_morsel.csv')

# Fix regex and datetime
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
df['date'] = pd.to_datetime(df['date'])

# Aggregate by date
daily_summary = df.groupby('date').agg({
    'quantity': 'sum',
    'price': 'mean'
}).reset_index()

# Create figure
fig = go.Figure()

# Line plot
fig.add_trace(go.Scatter(
    x=daily_summary['date'],
    y=daily_summary['quantity'],
    mode='lines+markers',
    name='Total Quantity Sold'
))

# ✅ THIS is the fixed way to add a vline on a datetime axis
fig.add_shape(
    type="line",
    x0='2021-01-15',
    x1='2021-01-15',
    y0=0,
    y1=1,
    xref='x',
    yref='paper',
    line=dict(
        color="red",
        width=2,
        dash="dash",
    )
)

# Add annotation manually
fig.add_annotation(
    x='2021-01-15',
    y=max(daily_summary['quantity']),
    text="Price Hike",
    showarrow=True,
    arrowhead=1
)

# Layout
fig.update_layout(
    title='Pink Morsel Sales Interpretation Before and After Price Hike',
    xaxis_title='Date',
    yaxis_title='Total Quantity Sold',
    template='plotly_white'
)

# Dash App
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Pink Morsel Sales Dashboard'),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)
