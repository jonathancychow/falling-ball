import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from cycling.model.frontend.app import app
from cycling.model.frontend.plots.results import simulation_results_plot
import numpy as np
from cycling.model.core.bike import Bike
from cycling.model.core.environment import Environment
from cycling.model.core.ball import Ball
from cycling.model.core.stage import Stage
from cycling.model.core.simulation import Simulation
from cycling.model.core.critical_power import CriticalPowerModel
from cycling.model.etl.utils import interpolate
from cycling.model.frontend.app import ball_data, bike_data

callback_suffix = 'baseline'


@app.callback(
    Output(f"collapse_bike_{callback_suffix}", "is_open"),
    [Input(f"collapse_button_bike_{callback_suffix}", "n_clicks")],
    [State(f"collapse_bike_{callback_suffix}", "is_open")],
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
def on_ball_select(rider_name):
    if rider_name in ball_data.keys():
        return ball_data[rider_name].mass, ball_data[rider_name].radius, ball_data[rider_name].cda
    else:
        return None, None


@app.callback(
    [
        Output(f"planet_gravity_{callback_suffix}", "value"),
        Output(f"planet_mass_{callback_suffix}", "value"),
        Output(f"planet_raidus_{callback_suffix}", "value"),
        Output(f"bike_gradient_climbing_{callback_suffix}", "value"),
        Output(f"planet_density_{callback_suffix}", "value")
    ],
    [
        Input(f"planet_select_{callback_suffix}", "value"),
    ],
)
def on_planet_select(bike_name):
    if bike_name in bike_data.keys():
        return bike_data[bike_name].mass, bike_data[bike_name].cda, bike_data[
            bike_name].cda_climbing, bike_data[bike_name].gradient_climbing, bike_data[bike_name].crr
    else:
        return None, None, None, None, None


@app.callback(
    Output(f"power_target_{callback_suffix}", "value"),
    [
        Input(f"power_select_{callback_suffix}", "value"),
    ],
)
def on_power_select(power_type):
    if power_type == "Constant":
        return 370
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
        Input(f"power_target_{callback_suffix}", "value")
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
        State(f"bike_gradient_climbing_{callback_suffix}", "value"),
        State(f"planet_density_{callback_suffix}", "value"),
        State(f"power_target_{callback_suffix}", "value"),
        State("hidden_data_stage", "value"),
    ]
)
def generate_baseline(
        n_clicks_time,
        ball_name,
        ball_weight,
        ball_radius,
        ball_cd,
        bike_name,
        bike_weight,
        bike_cda,
        bike_cda_climbing,
        bike_gradient_climbing,
        bike_crr,
        power_target,
        selected_stage
        ):

    # Run simulation
    env = Environment()
    ball = Ball(name=ball_name, mass=ball_weight, radius=ball_radius, cda=ball_cd)
    bike = Bike(
        name=bike_name,
        mass=bike_weight,
        cda=bike_cda,
        cda_climb=bike_cda_climbing,
        r_gradient_switch=bike_gradient_climbing /
        100,
        crr=bike_crr)

    # stage = Stage(name='Stage', file_name=f'{selected_stage}.csv', s_step=50)
    stage = None

    distance = np.arange(0, 5000, 5)
    simulation = Simulation(
        ball=ball,
        bike_1=bike,
        stage=stage,
        environment=env)

    # power = power_target * np.ones(len(stage.distance))
    power = 0 * np.ones(len(distance))
    print(f"{distance[0]} : {distance[-1]}")

    # velocity, time, _, _ = simulation.solve_velocity_and_time(
    #     s=stage.distance, power=power, v0=0.1, t0=0)
    velocity, time, _, _ = simulation.solve_velocity_and_time(
        s=distance, 
        power=power, 
        v0=0.1, 
        t0=0
        )

    seconds = np.arange(0, int(time[-1] + 1))
    power_per_second = power_target * np.ones(len(seconds))
    # cpm = CriticalPowerModel(cp=rider_cp, w_prime=rider_w_prime)
    # w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
    # w_prime_balance = interpolate(seconds, w_prime_balance_per_second, time)
    
    baseline_data = dict()
    baseline_data['time'] = time.tolist()
    # baseline_data['distance'] = stage.distance.tolist()
    baseline_data['distance'] = distance.tolist()
    baseline_data['velocity'] = velocity.tolist()
    # baseline_data['elevation'] = stage.elevation.tolist()
    baseline_data['elevation'] = distance.tolist()
    # baseline_data['w_prime_balance'] = w_prime_balance
    baseline_data['rider_name'] = ball_name
    baseline_data['bike_name'] = bike_name
    baseline_data['experiment_name'] = "baseline"

    figure = simulation_results_plot(baseline_data)
    return dcc.Graph(
        figure=figure), baseline_data, 'nav_link', 'nav_link', False, False
