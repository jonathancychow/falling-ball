import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from ball.model.frontend.app import app
from ball.model.frontend.plots.results import simulation_results_plot
import numpy as np
from ball.model.core.bike import Bike
from ball.model.core.environment import Environment
from ball.model.core.ball import Ball
from ball.model.core.simulation import Simulation
from ball.model.etl.utils import interpolate
from ball.model.frontend.app import ball_data, planet_data

callback_suffix = 'baseline'


@app.callback(
    Output(f"collapse_planet_{callback_suffix}", "is_open"),
    [Input(f"collapse_button_planet_{callback_suffix}", "n_clicks")],
    [State(f"collapse_planet_{callback_suffix}", "is_open")],
)
def toggle_collapse_bike(n, is_open):
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
        return None, None


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
        return planet_data[planet_name].gravity, planet_data[planet_name].mass, planet_data[
            planet_name].radius, planet_data[planet_name].rho
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
        Output("btn_baseline", "disabled"),
        Output("btn_baseline_nestor", "disabled")
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
        Output("plot_baseline", "children"),
        Output("hidden_data", "value"),
        Output("experiment-link", "className"),
        Output("explore-link", "className"),
        Output("btn_to_experiment", "disabled"),
        Output("btn_to_explore", "disabled")
    ],
    [
        Input("btn_baseline", "n_clicks_timestamp"),
    ],
    [
        State(f"ball_select_{callback_suffix}", "value"),
        State(f"ball_weight_{callback_suffix}", "value"),
        State(f"ball_radius_{callback_suffix}", "value"),
        State(f"ball_cd_{callback_suffix}", "value"),
        State(f"planet_select_{callback_suffix}", "value"),
        State(f"planet_gravity_{callback_suffix}", "value"),
        State(f"planet_mass_{callback_suffix}", "value"),
        State(f"planet_raidus_{callback_suffix}", "value"),
        State(f"planet_density_{callback_suffix}", "value"),
        State(f"v0_{callback_suffix}", "value"),
    ]
)
def generate_baseline(
        n_clicks_time,
        ball_name,
        ball_weight,
        ball_radius,
        ball_cd,
        planet_name,
        planet_gravity,
        planet_mass,
        planet_radius,
        planet_air_density,
        initial_velocity,
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

    velocity, time, _, _ = simulation.solve_velocity_and_time(
            s=distance, 
            v0=initial_velocity, 
            t0=0
        )

    baseline_data = dict()
    baseline_data['time'] = time.tolist()
    baseline_data['distance'] = distance.tolist()
    baseline_data['velocity'] = velocity.tolist()
    baseline_data['ball_name'] = ball_name
    baseline_data['planet_name'] = planet_name
    baseline_data['experiment_name'] = "baseline"

    figure = simulation_results_plot(baseline_data)
    return dcc.Graph(
        figure=figure), baseline_data, 'nav_link', 'nav_link', False, False
