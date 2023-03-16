import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

# Load data
nsdq = pd.read_csv('/Users/seifammar/Desktop/Data_viz/main_folder/Tutorials/Tutorial_replicats/Nasdaq_Analysis/NASDAQcompanylist.csv')

# Set up app and layout
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Nasdaq Stock Analysis'),
    html.Div(children='''
        Select a sector to display stock tickers:
    '''),
    dcc.Dropdown(
        id='sector-dropdown',
        options=[{'label': sector, 'value': sector} for sector in nsdq['Sector'].unique()],
        value='Health Care'
    ),
    dcc.Graph(id='price-graph'),
    dcc.Graph(id='volume-graph'),
])

# Define callback for updating ticker options when sector is changed
@app.callback(
    dash.dependencies.Output('price-graph', 'figure'),
    dash.dependencies.Output('volume-graph', 'figure'),
    [dash.dependencies.Input('sector-dropdown', 'value')])
def update_graphs(sector):
    # Filter dataframe by selected sector
    df = nsdq[nsdq['Sector'] == sector]
    
    # Create options for ticker dropdown
    ticker_options = [{'label': row['Name'] + ' (' + row['Symbol'] + ')', 'value': row['Symbol']} for _, row in df.iterrows()]
    
    # Create price graph
    price_fig = px.line(df, x='Symbol', y='Price', labels={'Symbol': 'Ticker Symbol', 'Price': 'Stock Price ($)'})
    
    # Create volume graph
    volume_fig = px.bar(df, x='Symbol', y='Volume', labels={'Symbol': 'Ticker Symbol', 'Volume': 'Volume (Shares)'})
    
    return price_fig, volume_fig

if __name__ == '__main__':
    app.run_server(port=5000)
