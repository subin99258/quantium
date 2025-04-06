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

# Custom CSS styles
app.layout = html.Div([
    # Main container
    html.Div([
        # Header
        html.H1('Pink Morsel Sales Dashboard', 
                style={
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'fontFamily': 'Arial, sans-serif',
                    'marginBottom': '30px',
                    'padding': '20px',
                    'backgroundColor': '#ecf0f1',
                    'borderRadius': '10px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
                }),

        # Controls container
        html.Div([
            # Metric selection
            html.Div([
                html.Label('Select Metric:', 
                          style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'Total Quantity Sold', 'value': 'quantity'},
                        {'label': 'Average Price', 'value': 'price'}
                    ],
                    value='quantity',
                    clearable=False,
                    style={'marginBottom': '20px'}
                ),
            ]),

            # Region selection
            html.Div([
                html.Label('Select Region:', 
                          style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                dcc.RadioItems(
                    id='region-radio',
                    options=[
                        {'label': 'North', 'value': 'north'},
                        {'label': 'East', 'value': 'east'},
                        {'label': 'South', 'value': 'south'},
                        {'label': 'West', 'value': 'west'},
                        {'label': 'All', 'value': 'all'}
                    ],
                    value='all',
                    labelStyle={'display': 'block', 'marginBottom': '10px'},
                    style={'marginBottom': '20px'}
                ),
            ]),

            # Date range selection
            html.Div([
                html.Label('Select Date Range:', 
                          style={'fontWeight': 'bold', 'marginBottom': '10px'}),
                dcc.DatePickerRange(
                    id='date-range',
                    start_date=df['date'].min(),
                    end_date=df['date'].max(),
                    display_format='YYYY-MM-DD',
                    style={'marginBottom': '20px'}
                ),
            ]),
        ], style={
            'width': '30%',
            'display': 'inline-block',
            'padding': '20px',
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'marginRight': '20px'
        }),

        # Chart container
        html.Div([
            dcc.Graph(id='line-chart')
        ], style={
            'width': '65%',
            'display': 'inline-block',
            'verticalAlign': 'top',
            'padding': '20px',
            'backgroundColor': 'white',
            'borderRadius': '10px',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
        })
    ], style={
        'padding': '20px',
        'backgroundColor': '#f5f6fa',
        'minHeight': '100vh'
    })
])

# Callback for interactive updates
@app.callback(
    Output('line-chart', 'figure'),
    [
        Input('metric-dropdown', 'value'),
        Input('region-radio', 'value'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    ]
)
def update_chart(metric, region, start_date, end_date):
    dff = df.copy()

    # Filter by region
    if region != 'all':
        dff = dff[dff['region'].str.lower() == region]

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

    # Update layout with custom styling
    fig.update_layout(
        template='plotly_white',
        plot_bgcolor='white',
        paper_bgcolor='white',
        title={
            'x': 0.5,
            'y': 0.95,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 24, 'color': '#2c3e50'}
        },
        xaxis_title='Date',
        yaxis_title='Value',
        font=dict(family='Arial, sans-serif'),
        margin=dict(l=50, r=50, t=100, b=50)
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
