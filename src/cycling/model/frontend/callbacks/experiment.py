import dash_core_components as dcc
import pandas as pd
import dash_table
from dash_table.Format import Format, Scheme, Symbol
from dash.dependencies import Input, Output, State
from cycling.model.frontend.app import app
from cycling.model.frontend.plots.results import simulation_results_plot
import numpy as np
from cycling.model.core.bike import Bike
from cycling.model.core.environment import Environment
from cycling.model.core.ball import Ball
# from cycling.model.core.stage import Stage
from cycling.model.core.simulation import Simulation
# from cycling.model.core.critical_power import CriticalPowerModel
from cycling.model.etl.utils import interpolate
from cycling.model.frontend.app import ball_data, planet_data

callback_suffix = 'experiment'


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
        Output(f"bike_gradient_climbing_{callback_suffix}", "value"),
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
                planet_data[planet_name].gradient_climbing, \
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
        # State(f"bike_gradient_climbing_{callback_suffix}", "value"),
        State(f"planet_raidus_{callback_suffix}", "value"),
        State(f"v0_{callback_suffix}", "value"),
        State("experiment_name", "value"),
        State("hidden_data", "value"),
        State("hidden_data_stage", "value")
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
        # bike_gradient_climbing,
        initial_velocity,
        # power_target,
        experiment_name,
        baseline_data,
        selected_stage):

    # Run simulation
    env = Environment(
        gravity=planet_gravity,
        air_density=planet_air_density
    )    
    ball = Ball(name=ball_name, mass=ball_weight, radius=ball_radius, cda=ball_cd)
    # bike = Bike(
    #     name=ball_name,
    #     mass=1,
    #     cda=1,
    #     cda_climb=1,
    #     r_gradient_switch=1 /
    #     100,
    #     crr=0)

    # stage = Stage(name='Stage', file_name=f'{selected_stage}.csv', s_step=50)
    # stage = None

    distance = np.arange(0, 100, 1)
    simulation = Simulation(
        ball=ball,
        # bike_1=bike,
        # stage=stage,
        environment=env)

    # power = power_target * np.ones(len(stage.distance))
    power = 0 * np.ones(len(distance))

    # velocity, time, _, _ = simulation.solve_velocity_and_time(
    #     s=stage.distance, power=power, v0=0.1, t0=0)

    velocity, time, _, _ = simulation.solve_velocity_and_time(
        s=distance, power=power, v0=initial_velocity, t0=0)

    # seconds = np.arange(0, int(time[-1] + 1))
    # power_per_second = power_target * np.ones(len(seconds))
    # cpm = CriticalPowerModel(cp=rider_cp, w_prime=rider_w_prime)
    # w_prime_balance_per_second = cpm.w_prime_balance(power=power_per_second)
    # w_prime_balance = interpolate(seconds, w_prime_balance_per_second, time)
    experiment_data = dict()
    experiment_data['time'] = time.tolist()
    # experiment_data['distance'] = stage.distance.tolist()
    experiment_data['distance'] = distance.tolist()

    experiment_data['velocity'] = velocity.tolist()
    # experiment_data['elevation'] = stage.elevation.tolist()
    # experiment_data['elevation'] = distance.tolist()

    # experiment_data['w_prime_balance'] = w_prime_balance
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
        # 'w_prime_balance'
        ]]

    if data is None:
        data = baseline_data.tail(1)

    if experiment_data is not None:
        experiment_data = pd.DataFrame(experiment_data)
        experiment_data = experiment_data[[
            'experiment_name', 'ball_name', 'planet_name', 'time', 
            # 'w_prime_balance'
            ]]
        experiment_data = experiment_data.tail(1)
        data = data.append(experiment_data, ignore_index=True)
        baseline_time = data['time'].iloc[0]
    #     baseline_pb = data['w_prime_balance'].iloc[0]
    #     style_data_conditional = [
    #         {
    #             'if': {
    #                 'column_id': 'time',
    #                 'filter_query': '{time} < ' + str(baseline_time)
    #             },
    #             'backgroundColor': '#3D9970',
    #             'color': 'white',
    #         },
    #         {
    #             'if': {
    #                 'column_id': 'w_prime_balance',
    #                 'filter_query': '{w_prime_balance} >' + str(baseline_pb)
    #             },
    #             'backgroundColor': '#3D9970',
    #             'color': 'white',
    #         },
    #         {
    #             'if': {
    #                 'column_id': 'time',
    #                 'filter_query': '{time} > ' + str(baseline_time)
    #             },
    #             'backgroundColor': '#e0001c',
    #             'color': 'white',
    #         },
    #         {
    #             'if': {
    #                 'column_id': 'w_prime_balance',
    #                 'filter_query': '{w_prime_balance} < ' + str(baseline_pb)
    #             },
    #             'backgroundColor': '#e0001c',
    #             'color': 'white',
    #         }
    #     ]
    # else:
    #     style_data_conditional = []

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
        # style_data_conditional=style_data_conditional
    )

    return table  # , data TODO: still needs to be fixed
