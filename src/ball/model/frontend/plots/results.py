import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go

experiment_color = '#28A745'


def simulation_results_plot(baseline_data, experiment_data=None):
    baseline_race_time = str(datetime.timedelta(seconds=baseline_data['time'][-1])).split('.')[0]
    figure = make_subplots(rows=1, cols=1,
                           shared_xaxes=True,
                           vertical_spacing=0.02,
                           row_heights=[0.6]
                           )

    figure.add_trace(go.Scatter(x=baseline_data['distance'], y=baseline_data['velocity'],
                                name="Baseline: {}".format(baseline_race_time),
                                opacity=0.5, line={'color': '#e31d1a'}),
                     row=1, col=1)

    if experiment_data:
        experiment_race_time = str(datetime.timedelta(seconds=experiment_data['time'][-1])).split('.')[0]
        figure.add_trace(go.Scatter(x=experiment_data['distance'], y=experiment_data['velocity'],
                                    name="Experiment: {}".format(experiment_race_time), opacity=0.5,
                                    line={'color': experiment_color}),
                         row=1, col=1)
 
    figure.update_yaxes(title_text="velocity (m/s)", row=1, col=1)
    figure.update_xaxes(title_text="distance (m)", row=1, col=1)
    figure.update_layout(height=600)

    return figure
