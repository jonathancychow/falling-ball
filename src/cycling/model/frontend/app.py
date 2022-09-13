import dash

import dash_bootstrap_components as dbc

from collections import namedtuple

THEME = 'Light'
if THEME == 'Dark':
    bootswatch_theme = dbc.themes.DARKLY
else:
    bootswatch_theme = dbc.themes.BOOTSTRAP

# Mock rider database
BallData = namedtuple(
    'RiderData', [
        'mass', 
        'radius', 
        'cd', 
        ])  # schema
ball_data = {
    "Tennis Ball": BallData(
        mass = 0.15,
        radius = 0.035,
        cd = 0.2,
        ),
    "Basketball": BallData(
        mass = 0.7,
        radius = 0.15,
        cd = 0.3,
        )
        }

# Mock bike database
PlanetData = namedtuple('BikeData',
                      ['gravity',
                       'mass',
                       'radius',
                       'gradient_climbing',
                       'rho',
                       'track_mu',
                       'eff_drive'])  # schema
planet_data = {
    "Earth": PlanetData(
        gravity=9.81,
        mass=5.972e24,
        radius=6371000,
        gradient_climbing=5,
        rho=1.2,
        track_mu=0.0025,
        eff_drive=0.974),
    "Mars": PlanetData(
        gravity=8.20,
        mass=6.39e23,
        radius=3389000,
        gradient_climbing=5,
        rho=0.003,
        track_mu=0.0025,
        eff_drive=0.974)}

ball_options = sorted([{"label": key, "value": key}
                        for key in ball_data.keys()], key=lambda x: x['value'])
planet_options = sorted([{"label": key, "value": key}
                       for key in planet_data.keys()], key=lambda x: x['value'])
power_options = [{"label": "Constant", "value": "Constant"}]

app = dash.Dash(__name__, external_stylesheets=[bootswatch_theme])

app.title = 'Cycling Simulation'

app.config.suppress_callback_exceptions = True

server = app.server
