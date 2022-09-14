import dash

import dash_bootstrap_components as dbc

from collections import namedtuple

THEME = 'Light'
if THEME == 'Dark':
    bootswatch_theme = dbc.themes.DARKLY
else:
    bootswatch_theme = dbc.themes.BOOTSTRAP

# Mock database
BallData = namedtuple(
    'BallData', [
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

# Mock database
PlanetData = namedtuple('PlanetData',
                      ['gravity',
                       'mass',
                       'radius',
                       'rho',
                       ])  # schema
planet_data = {
    "Earth": PlanetData(
        gravity=9.81,
        mass=5.972e24,
        radius=6371000,
        rho=1.2,
        ),
    "Mars": PlanetData(
        gravity=8.20,
        mass=6.39e23,
        radius=3389000,
        rho=0.003,
        )}

ball_options = sorted([{"label": key, "value": key}
                        for key in ball_data.keys()], key=lambda x: x['value'])
planet_options = sorted([{"label": key, "value": key}
                       for key in planet_data.keys()], key=lambda x: x['value'])
sim_options = [{"label": "-", "value": "-"}]

app = dash.Dash(__name__, external_stylesheets=[bootswatch_theme])

app.title = 'Falling Ball Simulation'

app.config.suppress_callback_exceptions = True

server = app.server
