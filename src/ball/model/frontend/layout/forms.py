import dash_bootstrap_components as dbc
from ball.model.frontend.app import ball_options, planet_options, sim_options
import dash_html_components as html


def ball_data_form(callback_suffix):
    ball_select = dbc.Select(
        id=f"ball_select_{callback_suffix}",
        options=ball_options,
        value="Tennis Ball"
    )
    ball_data = [
        dbc.FormGroup(
            children=[
                dbc.Label("Weight 0.5 - 100 (kg):"),
                dbc.Input(
                    id=f"ball_weight_{callback_suffix}",
                    type="number",
                    min=0.01,
                    max=100,
                    step=0.01),
            ]),
        dbc.FormGroup(
            children=[
                dbc.Button(
                    "More",
                    id=f"collapse_button_{callback_suffix}",
                    className="mb-3",
                    color="primary",
                ),
                dbc.Collapse(
                    dbc.Card(
                        dbc.FormGroup(
                            children=[
                                dbc.Label("Radius 0.1 - 10 (m):"),
                                dbc.Input(
                                    id=f"ball_radius_{callback_suffix}",
                                    type="number",
                                    min=0.01,
                                    max=10,
                                    step=0.005),
                                dbc.Label("Ball cd (-):"),
                                dbc.Input(
                                    id=f"ball_cd_{callback_suffix}",
                                    type="number",
                                    min=0.01,
                                    max=0.9,
                                    step=0.01),
                            ]),
                    ),
                    id=f"collapse_{callback_suffix}",
                ),
            ]),
    ]
    ball_data_form = dbc.Form(ball_data)

    # planet fields
    def get_planet_select(suffix):
        planet_select = dbc.Select(
            id=f"planet_select_{suffix}",
            options=planet_options,
            value="Earth"
        )
        return planet_select

    def get_planet_data_form(suffix):
        # if transition:
            # suffix = suffix + '_transition'

        planet_data = [
            dbc.FormGroup(
                children=[
                    dbc.Label("Gravity 5 - 20 (m/s/s):"),
                    dbc.Input(
                        id=f"planet_gravity_{suffix}",
                        type="number",
                        min=5,
                        max=20,
                        step=0.01),
                ]),
            dbc.FormGroup(
                children=[
                    dbc.Button(
                        "More",
                        id=f"collapse_button_planet_{callback_suffix}",
                        className="mb-3",
                        color="primary",
                    ),
                    dbc.Collapse(
                        dbc.Card(
                            dbc.FormGroup(
                                children=[
                                    dbc.Label("Air Density 0 - 10 (kg/m3):"),
                                    dbc.Input(
                                        id=f"planet_density_{suffix}",
                                        type="number",
                                        min=0,
                                        max=10,
                                        step=0.01),
                                    dbc.Label("Planet Mass (kg):"),
                                    dbc.Input(
                                        id=f"planet_mass_{suffix}",
                                        type="number",
                                        min=1,
                                        max=10000000,
                                        step=1),
                                    dbc.Label("Planet Radius (m)"),
                                    dbc.Input(
                                        id=f"planet_raidus_{suffix}",
                                        type="number",
                                        min=1,
                                        max=1000000000,
                                        step=1),
                                ]),
                        ),
                        id=f"collapse_planet_{callback_suffix}",
                    ),
                ]),
        ]
        return dbc.Form(planet_data)

    # power fields
    sim_select = dbc.Select(
        id=f"sim_select_{callback_suffix}",
        options=sim_options,
        value="-"
    )
    sim_data = [
        dbc.FormGroup(
            children=[
                dbc.Label("Initial Velocity (m/s):"),
                dbc.Input(
                    id=f"v0_{callback_suffix}",
                    type="number",
                    min=0,
                    max=800,
                    step=0.01),
            ])]
    sim_data_form = dbc.Form(sim_data)

    ball_form = [
        # ball
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Label("Ball:"),
                        ball_select
                    ],
                    md=3
                ),
                dbc.Col(
                    children=[ball_data_form],
                    md=9
                )
            ],
        ),
        # planet
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Label("Planet:"),
                        get_planet_select(callback_suffix)
                    ],
                    md=3
                ),
                dbc.Col(
                    children=[get_planet_data_form(callback_suffix)],
                    md=9
                )
            ],
        ),
        # sim
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Label("Sim:"),
                        sim_select
                    ],
                    md=3
                ),
                dbc.Col(
                    children=[sim_data_form],
                    md=9
                )
            ],
        ),
    ]
    return ball_form
