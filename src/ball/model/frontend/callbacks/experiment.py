from collections import defaultdict
import dash_core_components as dcc
import pandas as pd
import dash_table
from dash_table.Format import Format, Scheme, Symbol
from dash.dependencies import Input, Output, State
from ball.model.frontend.app import app
from ball.model.frontend.plots.results import simulation_results_plot
import numpy as np
from ball.model.core.environment import Environment
from ball.model.core.ball import Ball
from ball.model.core.simulation import Simulation
from ball.model.frontend.app import ball_data, planet_data

callback_suffix = 'experiment'


@app.callback(
    Output(f"collapse_planet_{callback_suffix}", "is_open"),
    [Input(f"collapse_button_planet_{callback_suffix}", "n_clicks")],
    [State(f"collapse_planet_{callback_suffix}", "is_open")],
)
def toggle_collapse_planet(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output(f"collapse_{callback_suffix}", "is_open"),
    [Input(f"collapse_button_{callback_suffix}", "n_clicks")],
    [State(f"collapse_{callback_suffix}", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [
        Output(f"ball_weight_{callback_suffix}", "value"),
        Output(f"ball_radius_{callback_suffix}", "value"),
        Output(f"ball_cd_{callback_suffix}", "value")
    ],
    [
        Input(f"ball_select_{callback_suffix}", "value"),
    ],
)
def on_ball_select(ball_name):
    if ball_name in ball_data.keys():
        return ball_data[ball_name].mass, ball_data[ball_name].radius, ball_data[ball_name].cd
    else:
        return None, None, None


@app.callback(
    [
        Output(f"planet_gravity_{callback_suffix}", "value"),
        Output(f"planet_mass_{callback_suffix}", "value"),
        Output(f"planet_raidus_{callback_suffix}", "value"),
        Output(f"planet_density_{callback_suffix}", "value")
    ],
    [
        Input(f"planet_select_{callback_suffix}", "value"),
    ],
)
def on_planet_select(planet_name):
    if planet_name in planet_data.keys():
        return planet_data[planet_name].gravity, planet_data[planet_name].mass, \
                planet_data[planet_name].radius, \
                planet_data[planet_name].rho
    else:
        return None, None, None, None, None


@app.callback(
    Output(f"v0_{callback_suffix}", "value"),
    [
        Input(f"sim_select_{callback_suffix}", "value"),
    ],
)
def on_power_select(power_type):
    if power_type == "-":
        return 0.01
    else:
        return None


@app.callback(
    [
        Output("btn_experiment", "disabled"),
        Output("btn_experiment_nestor", "disabled"),
    ],
    [
        Input(f"ball_weight_{callback_suffix}", "value"),
        Input(f"planet_gravity_{callback_suffix}", "value"),
        Input(f"planet_mass_{callback_suffix}", "value"),
        Input(f"planet_density_{callback_suffix}", "value"),
        Input(f"v0_{callback_suffix}", "value")
    ],
)
def check_validity(*args):
    if all(args):
        return False, False
    return True, True


@app.callback(
    [
        Output("plot_experiment", "children"),
        Output("hidden_data_experiment", "value")
    ],
    [
        Input("btn_experiment", "n_clicks_timestamp")
    ],
    [
        State(f"ball_select_{callback_suffix}", "value"),
        State(f"ball_weight_{callback_suffix}", "value"),
        State(f"ball_radius_{callback_suffix}", "value"),
        State(f"ball_cd_{callback_suffix}", "value"),
        State(f"planet_select_{callback_suffix}", "value"),
        State(f"planet_gravity_{callback_suffix}", "value"),
        State(f"planet_mass_{callback_suffix}", "value"),
        State(f"planet_density_{callback_suffix}", "value"),
        State(f"planet_raidus_{callback_suffix}", "value"),
        State(f"v0_{callback_suffix}", "value"),
        State("experiment_name", "value"),
        State("hidden_data", "value"),
    ]
)
def generate_experiment(
        n_clicks_time,
        ball_name,
        ball_weight,
        ball_radius,
        ball_cd,
        planet_name,
        planet_gravity,
        planet_mass,
        planet_air_density,
        planet_radius,
        initial_velocity,
        experiment_name,
        baseline_data,
        ):

    # Run simulation
    env = Environment(
        gravity=planet_gravity,
        air_density=planet_air_density
    )    
    ball = Ball(name=ball_name, mass=ball_weight, radius=ball_radius, cda=ball_cd)

    distance = np.arange(0, 100, 1)
    simulation = Simulation(
            ball=ball,
            environment=env
        )

    velocity, time = simulation.solve_velocity_and_time(
            s=distance, 
            v0=initial_velocity, t0=0
        )

    experiment_data = defaultdict()
    experiment_data['time'] = time.tolist()
    experiment_data['distance'] = distance.tolist()
    experiment_data['velocity'] = velocity.tolist()
    experiment_data['ball_name'] = ball_name
    experiment_data['planet_name'] = planet_name
    experiment_data['experiment_name'] = experiment_name

    figure = simulation_results_plot(baseline_data, experiment_data)
    return dcc.Graph(figure=figure), experiment_data


@app.callback(
    Output('log-table', 'children'),
    [Input("hidden_data", "value"),
     Input("hidden_data_experiment", "value")],
    [State("hidden_data_merged", "value")])
def update_table(baseline_data, experiment_data, data):
    baseline_data = pd.DataFrame(baseline_data)
    baseline_data = baseline_data[[
        'experiment_name', 'ball_name', 'planet_name', 'time', 
        ]]

    if data is None:
        data = baseline_data.tail(1)

    if experiment_data is not None:
        experiment_data = pd.DataFrame(experiment_data)
        experiment_data = experiment_data[[
            'experiment_name', 'ball_name', 'planet_name', 'time', 
            ]]
        experiment_data = experiment_data.tail(1)
        data = data.append(experiment_data, ignore_index=True)
        baseline_time = data['time'].iloc[0]

    unit = ['', '', '', u's', u'J']
    table = dash_table.DataTable(
        columns=[{"name": name,
                  "id": name,
                  "type": "numeric",
                  "format": Format(precision=1,
                                   scheme=Scheme.fixed,
                                   symbol=Symbol.yes,
                                   symbol_suffix=u
                                   )
                  } for name, u in zip(data.columns, unit)
                 ],
        data=data.to_dict('records'),
        editable=True,
        style_as_list_view=True,
        style_header={'fontWeight': 'bold'},
    )

    return table  # , data TODO: still needs to be fixed
