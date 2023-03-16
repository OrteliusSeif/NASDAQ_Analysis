import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas_datareader
import pandas_datareader.data as web
from datetime import datetime
import pandas as pd
import dash_bootstrap_components as dbc


nsdq = pd.read_csv('/Users/seifammar/Desktop/Data_viz/main_folder/Tutorials/Tutorial_replicats/Nasdaq_Analysis/NASDAQcompanylist.csv')

nsdq.set_index('Symbol', inplace=True)
options=[]


for tic in nsdq.index:
    #{'label': 'user sees', 'value': 'script sees'}
    mydict = {}
    mydict['label'] = nsdq.loc[tic]['Name'] + ' ' + tic #Apple Co. APPL
    mydict['value'] = tic
    options.append(mydict)



# Set your API key
api_key = 'pk_824a5++++d695++++++88+++9456d++++8588b1****2**e1305c270'


app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.BOOTSTRAP])


card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "Some quick example text to build on the card title and make up the bulk of the card's content.",
                className="card-text",
            ),
            dbc.Button("Go somewhere", color="primary"),
        ]
    ),
    style={"width": "18rem"},
)


app.layout = html.Div([
             html.H1('Stock Ticker Dashboard', style={'font-family': 'Arial', 'text-align': 'center'}),
             html.Div([html.H3('Enter a stock symbol:', style={'font-family': 'Arial'}),
             dcc.Dropdown(
                      id='my_stock_picker',
                      options = options,

                      value= ['TSLA'], #stes a default value
                      multi=True

             )
             ], style={'display':'inline-block', 'verticalAlign':'top', 'width': '30%' }),
             html.Div ([html.H3('Select a start and end date:', style={'font-family': 'Arial'}),
             dcc.DatePickerRange(id='my_date_picker',
                                   min_date_allowed=datetime(2015,1,1),
                                   max_date_allowed=datetime.today(),
                                   start_date = datetime(2018,1,1),
                                   end_date = datetime.today()
                                   )
             ], style={'display':'inline-block'}),

              html.Div([

                html.Button(
                    id='submit-button',
                    n_clicks=0,
                    children='Submit',
                    style={'fontSize':18, 'marginLeft':'30px'}
                ),
              ], style={'display':'inline-block'}),
            dcc.Graph(id='my_graph',
                          figure={'data':[
                                  {'x':[1,2], 'y':[3,1]}
                                  ], 
                                  'layout': {
                                      
            'plot_bgcolor': '#F2F2F2',
            'paper_bgcolor': '#F2F2F2',
            'font': {'color': 'white', 'family': 'Roboto'},
            'xaxis': {'gridcolor': 'white'},
            'yaxis': {'gridcolor': 'white'}                  
                                 }
    }
)
], style={'backgroundColor': '#F2F2F2', 'fontFamily': 'Roboto'})

@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_stock_picker', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])


def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, 'iex', start, end, api_key=api_key)
        traces.append({'x':df.index, 'y':df.close, 'name':tic})

    # Pass the API key to the DataReader Function
    fig = {
        'data':traces,
        'layout':{'title':', '.join(stock_ticker)}
    }
    return fig

if __name__ == '__main__':
    app.run_server(port=5000)