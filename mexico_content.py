
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.express as px
import dash_table


#Data

df = px.data.gapminder().query('year==2007')


#Styles
TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'    # Midnight blue
}


#Content
content_first_row = dbc.Row(dbc.Col(html.Div(dcc.Input(id="input-1",placeholder= "Search for the type of policy that you are interested in",style={"width":"100%"}))))

content_third_row = dbc.Row(  # this one is active!!!!!!!!!!!
    [
        dbc.Col(
            dcc.Graph(id='graph_4'), md=12,
        )
    ]
)

content_fifth_row = dbc.Row(  # this one is an experiment, created by David !!!!!!!!!!!
    [
        dbc.Col(
            dash_table.DataTable(id='table_1',
                                 columns=[
                                     {'name': i, 'id': i, 'deletable': False} for i in sorted(df.columns)
                                     # it was 'deletable': True
                                 ],
                                 page_current=0,
                                 page_size=10,  # it was PAGE_SIZE,
                                 page_action='custom',  # it was custom
                                 sort_action='custom',  # these two have to be 'custom' so that you can manipuate it
                                 sort_mode='single',
                                 sort_by=[]

                                 ), md=12,
        )
    ]
)

collapse = html.Div(
    [
        dbc.Button(
            "Submit",  # it was México D.F
            id="collapse-button",
            className="mb-3",
            # m - for classes that set margin, b - for classes that set margin-bottom or padding-bottom, 3 - (by default) for classes that set the margin or padding to $spacer
            color="primary",  # this means some kind of blue color
        ),
        dbc.Collapse(
            [dbc.Card(dbc.CardBody("Document 1")), dbc.Card(dbc.CardBody("Document 2")),
             dbc.Card(dbc.CardBody("Document 3"))],
            id="collapse",
        )
    ]
)



content = html.Div(
    [
        html.H2('Economic incentive search for forest land restoration', style=TEXT_STYLE),
        html.Hr(),  # break
        content_first_row,  # placeholder= "Search for the type of policy that you are interested in"
        html.Hr(),  # break
        content_third_row,
        html.Div(html.H1("Best match")),
        html.Div(html.H5("""Some text regarding user's query.""")),
        content_fifth_row,  # this is experiment added by David!!!!
        html.Hr(), collapse]
        )





