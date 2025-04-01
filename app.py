import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv('filtered_pink_morsel.csv')

# Data cleaning
df['price'] = df['price'].replace(r'[\$,]', '', regex=True).astype(float)
df['date'] = pd.to_datetime(df['date'])

# Dash App
app = dash.Dash(__name__)

# App Layout
app.layout = html.Div([
    html.H1('Pink Morsel Sales Dashboard', style={'textAlign': 'center'}),

    html.Div([
        html.Label('Select Metric:'),
        dcc.Dropdown(
            id='metric-dropdown',
            options=[
                {'label': 'Total Quantity Sold', 'value': 'quantity'},
                {'label': 'Average Price', 'value': 'price'}
            ],
            value='quantity',
            clearable=False
        ),

        html.Label('Select Region:'),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': region, 'value': region} for region in df['region'].unique()] + [{'label': 'All', 'value': 'All'}],
            value='All',
            clearable=False
        ),

        html.Label('Select Date Range:'),
        dcc.DatePickerRange(
            id='date-range',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
            display_format='YYYY-MM-DD'
        ),
    ], style={'width': '30%', 'display': 'inline-block', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='line-chart')
    ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'})
])

# Callback for interactive updates
@app.callback(
    Output('line-chart', 'figure'),
    [
        Input('metric-dropdown', 'value'),
        Input('region-dropdown', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    ]
)
def update_chart(metric, region, start_date, end_date):
    dff = df.copy()

    # Filter by region
    if region != 'All':
        dff = dff[dff['region'] == region]

    # Filter by date
    dff = dff[(dff['date'] >= pd.to_datetime(start_date)) & (dff['date'] <= pd.to_datetime(end_date))]

    # Aggregate
    agg_df = dff.groupby('date').agg({
        'quantity': 'sum',
        'price': 'mean'
    }).reset_index()

    # Create figure
    fig = px.line(
        agg_df,
        x='date',
        y=metric,
        title='Pink Morsel Sales Analysis'
    )

    # Price Hike Marker
    fig.add_vline(
        x=pd.Timestamp('2018-02-06'),
        line_width=2,
        line_dash='dash',
        line_color='red'
    )

    fig.add_annotation(
        x='2018-02-06',
        y=agg_df[metric].max() if not agg_df.empty else 0,
        text="Price Hike",
        showarrow=True,
        arrowhead=1
    )

    fig.update_layout(template='plotly_white')

    return fig

if __name__ == '__main__':
    app.run(debug=True)
