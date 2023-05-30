from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import numpy as np
import pandas as pd
from google.oauth2 import service_account
from scipy import stats

import dash_bootstrap_components as dbc

from PIL import Image



#Using Pillow to read the the image




app = Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX] )

app.layout = html.Div([
   
   dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row to 
                dbc.Row(
                    [
                        dbc.Col(html.Img(src= Image.open("v8.png"), height="125px"  ) ),
                        #dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                    ],
                    
                ),
                
                
            ),
            
           html.H4(children='Factor investing', style={ 'color' : 'black'}) ,
        ]
    ),
    color="white",
    
),


      
    html.Br(),
    
     html.Br(),
    
    dbc.Row([
                dbc.Col([
                    
                   html.H6("EV/EBITDA menor que:", style={'justifyContent': 'center'} )
                ], width= 2,   ),
                dbc.Col([
                   
                   html.H6("LPA maior que:", style={'justifyContent': 'center'} )
                ], width= 2,     ),], justify="center" ),
    
    dbc.Row([
                dbc.Col([
                   dcc.Input( id='EV',  type="number", value = 10),
                ], width= 2, style={'justifyContent': 'center'} ),
                dbc.Col([
                   dcc.Input( id='LPA',  type="number", value = 2),
                ], width= 2, style={'justifyContent': 'center'} ),  ], justify="center" ),
    
    
    html.Br(),
    html.Br(),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('EV', 'value'),
    Input('LPA', 'value')
)
def update_graph(EV, LPA,):
    
    DF = pd.read_excel('appbase.xlsx')
    
    Begin_Date = '2023-05-02'
    EV_EBITDA = EV
    LPA = LPA
    
    DF = DF.query( " Data == @Begin_Date and `EV/EBITDA emp|Em moeda orig|no exercício|consolid:sim*` < @EV_EBITDA and `LPA| Em moeda orig| no exercício| consolid:sim*| ajust p/ prov` > @LPA  "   )

    fig = px.bar( 
             pd.DataFrame ( [ DF['Ativo'] ,stats.zscore(DF['EV/EBITDA emp|Em moeda orig|no exercício|consolid:sim*']) ] ).T.sort_values(by=['EV/EBITDA emp|Em moeda orig|no exercício|consolid:sim*']
).rename(columns={'EV/EBITDA emp|Em moeda orig|no exercício|consolid:sim*': 'EV/EBITDA Z Score' } ),
             x='Ativo', y='EV/EBITDA Z Score', template = "plotly_white", color_discrete_sequence= [px.colors.qualitative.Dark24[-2]] )
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)


#
