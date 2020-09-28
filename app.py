import pandas
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

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
        return html.Div("En construcción")
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
