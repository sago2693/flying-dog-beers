import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import dash_bootstrap_components as dbc
from urllib.request import urlopen
from dash.dependencies import Input, Output, State
import plotly.express as px
import json

import mexico_content
# this was added by David

df= px.data.gapminder().query('year==2007')   # this is plotted, it was 2007

# the style arguments for the sidebar
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '20%',     # this sizes the left hand side of the board to 20%
    'padding': '20px 10px',
    'background-color': '#f8f9fa'   # this means a light gray
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',   # this was 25%
    'margin-right': '5%',   #this was 5%, by controlling the margins, you control the border
    'padding': '20px 10px'    # this was 20px 10p   The CSS padding properties are used to generate space around an element's content, inside of any defined borders.
                            # i am not sure what this refers to
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'    # Midnight blue
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'    #Pure (or mostly pure) blue.
}


sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Choose one of the following features", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Search Engine", href="/page-1", id="page-1-link"),
                dbc.NavLink("Highlight text", href="/page-2", id="page-2-link"),
                dbc.NavLink("Incentives by country", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content_first_row = dbc.Row(dbc.Col(html.Div(dcc.Input(id="input-1",placeholder= "Search for the type of policy that you are interested in",style={"width":"100%"})))) #this was 100%, this with controls only the with of the search window

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='graph_1'), md=4  #md was 4, i dont know what this is
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4   #md was 4,
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4  #md was 4,
        )
    ]
)

content_third_row = dbc.Row(  #this one is active!!!!!!!!!!!
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_fourth_row = dbc.Row(   #this one is not  active
    [
        dbc.Col(
            dcc.Graph(id='graph_5'), md=6  #md (, optional): Specify column behaviour on a medium screen. Valid arguments are boolean, an integer in the range 1-12 inclusive, or a dictionary with keys 'offset', 'order', 'size'. See the documentation for more details.
        ),
        dbc.Col(
            dcc.Graph(id='graph_6'), md=6
        )
    ]
)

content_fifth_row = dbc.Row(   #this one is an experiment, created by David !!!!!!!!!!!
    [
        dbc.Col(
            dash_table.DataTable(id='table_1',
                                 columns=[
                                     {'name': i, 'id': i, 'deletable': False} for i in sorted(df.columns)  # it was 'deletable': True
                                 ],
                                 page_current=0,
                                 page_size=10,  # it was PAGE_SIZE,
                                 page_action='custom',    # it was custom
                                 sort_action='custom',     #these two have to be 'custom' so that you can manipuate it 
                                 sort_mode='single',
                                 sort_by=[]

                                 ), md=12,
        )
    ]
)

###Search by region collapse

collapse = html.Div(
    [
        dbc.Button(
            "Submit", # it was México D.F
            id="collapse-button",
            className="mb-3",  #m - for classes that set margin, b - for classes that set margin-bottom or padding-bottom, 3 - (by default) for classes that set the margin or padding to $spacer
            color="primary",  #this means some kind of blue color
        ),
        dbc.Collapse(
            [dbc.Card(dbc.CardBody("Document 1")),dbc.Card(dbc.CardBody("Document 2")),dbc.Card(dbc.CardBody("Document 3"))],
            id="collapse",
        )
    ]
)

#Content element
content = html.Div(id="page-content", style=CONTENT_STYLE)

page_1_content = html.Div(
    [
        html.H2('Economic incentive search for forest land restoration', style=TEXT_STYLE),
        html.Hr(),  #break
        content_first_row,  # placeholder= "Search for the type of policy that you are interested in"
        html.Hr(),  # break
        content_third_row,
        html.Div(html.H1("Best match")),
        html.Div(html.H5("""Some text regarding user's query.""")),
        content_fifth_row, # this is experiment added by David!!!!
        html.Hr(),  # break, this was modified by David
        collapse

        #content_second_row,
        #content_fourth_row
    ],
    style=CONTENT_STYLE
)




app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([dcc.Location(id="url"),sidebar, content])                   #this is the key of the division!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


## URL callback
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return page_1_content
    elif pathname == "/page-2":
        
        return html.Div("En construcción")
    elif pathname == "/page-3":
        return mexico_content.content
    # If the user tries to reach a different page, return a 404 message
    else:
        return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

if __name__ == '__main__':
    app.run_server()



@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value,
                   radio_items_value):  # this figure is being called
    print(n_clicks)
    print(dropdown_value)
    print(range_slider_value)
    print(check_list_value)
    print(radio_items_value)  # Sample data and figure


    with urlopen(
            'https://raw.githubusercontent.com/davidlararamos/mexico_geojson/master/mx_states.json') as response:
        mexican_states = json.load(response)



    state_id_map = {}

    for feature in mexican_states['features']:  # we are creating new keys for our dictionary
        feature['id'] = feature['properties']['id']
        # feature['state_name'] = feature['properties']['state_name']
        state_id_map[feature['properties']['state_name']] = feature['id']

    url = 'https://es.wikipedia.org/wiki/Anexo:Entidades_federativas_de_M%C3%A9xico_por_PIB'
    df = pd.read_html(url)
    df_gdp_state = df[1]
    df_gdp_state_inter = df_gdp_state[['Estado', '2015p']]
    df_gdp_state_inter['Estado'] = df_gdp_state_inter['Estado'].replace(
        ['Ciudad de México', 'Estado de México', '50x36px Veracruz'], ['Distrito Federal', 'México', 'Veracruz'])
    df_gdp_state_corrected = df_gdp_state_inter.rename(columns={"Estado": "State", "2015p": "GDP"})
    df_gdp_state_corrected_final = df_gdp_state_corrected.drop(df_gdp_state_corrected.index[0])
    df_gdp_state_corrected_final['id'] = df_gdp_state_corrected_final['State'].apply(lambda x: state_id_map[x])

    df_gdp_state_corrected_final['GDP_nospace'] = ['2312562', '1230628', '1041797', '889703', '676899', '591414',
                                                   '570172', '464771', '401342', '435028', '400916', '409317', '433857',
                                                   '423215', '318401', '314979', '290580', '271982', '227598', '224237',
                                                   '223435', '213783', '203685', '196744', '169885', '161902', '159797',
                                                   '131983', '103406', '92149', '81672', '75578']

    df_gdp_state_corrected_final['GDP_int'] = df_gdp_state_corrected_final['GDP_nospace'].astype(int)
    df_gdp_state_corrected_final['GDP_int_scale'] = np.log10(df_gdp_state_corrected_final['GDP_int'])


    fig = px.choropleth(df_gdp_state_corrected_final, locations='id', geojson=mexican_states, scope='north america',color='GDP_int',
                        hover_name='State')


    fig.update_geos(fitbounds='locations', visible=False)


    fig.update_layout({
        'height': 600
    })
    return fig