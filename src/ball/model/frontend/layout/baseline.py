import dash_core_components as dcc
import dash_bootstrap_components as dbc
from ball.model.frontend.layout.forms import ball_data_form
import dash_html_components as html

callback_suffix = 'baseline'

ball_form = ball_data_form(callback_suffix)
generate_baseline = [
    dbc.Row(
        children=[
            dbc.Col(
                dbc.Button("Start simulation", id="btn_baseline", color="primary", size="lg",
                           block=True, disabled=True),
                md=12
            ),
        ],
        className='mt-3 mb-3'
    ),
    dbc.Row(
        dbc.Col(children=[
            dcc.Loading(id="plot_baseline"),
        ],
            md=12
        )
    ),
    dbc.Row(
        children=[
            dbc.Col(dbc.Button("Go to Experiment", id="btn_to_experiment", color="primary", size="lg", block=True,
                               href="experiment", disabled=True)
                    )
        ],
        className='mt-3 mb-3'),
]
header = [
    dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Label("Step 2 - Configure you ball, planet and simulation set up.", className="bold"),
                    html.P("Click on 'More' to see more variables you could change. "
                           "Once you have generated a baseline, click on 'Go to Experiment'.", className="lead"),
                ],
                width="auto",
            ),
        ],
        className='mb-3'
    ),
]

baseline_page_layout = header + ball_form + generate_baseline
