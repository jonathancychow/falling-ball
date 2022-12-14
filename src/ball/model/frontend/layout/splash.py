import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

splash_layout =[
    dbc.Jumbotron(
    children=[
        html.H1("Falling Ball", className="display-3", style={"text-align": "left"}),
        html.P("Model to simulate a ball falling through the air under gravity", className="lead", style={"text-align": "left"}),
        html.Hr(className="my-2"),

    ]
    ),
    dbc.Row(
        children=[
            dbc.Col(dbc.Button("Get Started!", id="itt", color="primary", size="lg", block=True)),
        ]
    ),
    dbc.Row(
        children=[
            html.Br(),
            html.P([
                "The simulation models a spherical ball falling through the air under the influence of gravity and aerodynamic drag.",
                html.Br(),
                html.Br(),
                "1. Set up a baseline simulation",
                html.Br(),
                "2. Change variables and do an experiment",
                html.Br()
            ],
                className="lead",
                style={"text-align": "left",
                       'word-wrap': 'break-word',
                       }
            ),
        ]
    ),
    html.Div(dcc.Markdown('''
            &nbsp;  
            &nbsp;  
            Documention [here](https://github.com/jonathancychow/falling-ball)  
            '''),
             style={
                 'textAlign': 'left',
                 'color': '#BEBEBE',
                 'width': '100%',
                 'float': 'center',
                 'display': 'inline-block'}
             )
]
