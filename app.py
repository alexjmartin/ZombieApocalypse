import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output
import numpy as np
import plotly.graph_objects as go
import datetime
import sys
sys.path.append('C:\\Users\\alex_\\PycharmProjects\\Zombie')
import zombie_library as zl

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

variable_list = ['zombies', 'infection_chance', 'infection_radius', 'birth_rate', 'nat_death', 'zombie_lifespan', 'total_pop', 'days',
               'zombie_speed', 'human_speed', 'map_size', 'immunity_chance', 'vaccine_day', 'vaccine_efficacy']

variable_dict = {'zombies': 1, 'infection_chance': 0.8, 'infection_radius': 20, 'birth_rate': 0.005, 'nat_death': 0.001, 'zombie_lifespan': 7, 'total_pop': 400, 'days': 30,
               'zombie_speed': 0.5, 'human_speed': 0.7, 'map_size': 400, 'immunity_chance': 0.01, 'vaccine_day': 20, 'vaccine_efficacy': 0.8}

default_list = []

pop_colours = {"Population_1": "forestgreen",
	"Population_2": "deepskyblue",
	"Zombie": "coral",
	"Immune": "slateblue",
	"Dead": "crimson"
}

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[

    html.Div(dcc.Markdown('''
    # Zombie Simulator
    ##### This app allows for the simulation of various possible scenarios for the spread of an infectious Zombie disease. For details on what each variable affects please see [README](https://github.com/alexjmartin/ZombieApocalypse/blob/main/README.md)
    ##### Please note that for populations of over X size the simulator may take a number of seconds to run
    >For the initial simulation default values of:
    >zombies=1, infection_chance=0.8, infection_radius=20, birth_rate=0.005, nat_death=0.001, zombie_lifespan=7, total_pop=400, days=30,
    >           zombie_speed=0.5, human_speed=0.7, immunity_chance=0.01, vaccine_day=20, vaccine_efficacy = 0.8, map_size=400 are used 
     ''')

        ),

html.Div([dcc.Markdown('''
Zombies | Infection chance 
     ''')

    ]),
    html.Div(
        [

            dcc.Input(
                id="input_{}".format(var),
                type='text',
              #  value='{}'.format(val),
                placeholder="{}".format(var),
            )

            for var, val in variable_dict.items()
        ]
        + [html.Div(id="out-all-types")]
    ),

     html.Div([
        html.Button('Start Simulation', id='show-secret'),
    ]),



    html.Div([dcc.Graph(
            id='graph1'
        ),]),

    html.Div([dcc.Graph(
                id='graph2'
            ),]),


])


@app.callback(
    [Output('graph1', 'figure'),
    Output('graph2', 'figure')],
    Input(component_id='input_zombies', component_property='value'),
    Input(component_id='input_infection_chance', component_property='value'),
    Input(component_id='input_infection_radius', component_property='value'),
    Input(component_id='input_birth_rate', component_property='value'),
    Input(component_id='input_nat_death', component_property='value'),
    Input(component_id='input_zombie_lifespan', component_property='value'),
    Input(component_id='input_total_pop', component_property='value'),
    Input(component_id='input_days', component_property='value'),
    Input(component_id='input_zombie_speed', component_property='value'),
    Input(component_id='input_human_speed', component_property='value'),
    Input(component_id='input_map_size', component_property='value'),
    Input(component_id='show-secret', component_property='n_clicks')
)

def update_output_div(input_zombies, input_infection_chance, input_infection_radius, input_birth_rate, input_nat_death, input_zombie_lifespan, input_total_pop, input_days, input_zombie_speed, input_human_speed, input_map_size, n_clicks):
    if n_clicks is None:
        df_hist = zl.Zombie_sim()
        dfp = df_hist.groupby(['population', 'day']).count().reset_index()
        fig = px.line(dfp, x='day', y='id', color='population', color_discrete_map=pop_colours, title=f'Population counts over the specified number of simulation days')
        fig.update_layout(yaxis_title='population count')
        fig2 = px.scatter(df_hist, x="x_coord", y="y_coord", animation_frame="day", animation_group="id",
                          color="population", color_discrete_map=pop_colours,  hover_name="population", title='Scatter map showing the progression of the simulated zombie apocalypse over time',
                          range_x=[0, input_map_size], range_y=[0, input_map_size])
        fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
        fig2.add_trace(go.Scatter(x=[input_map_size], y=[input_map_size],
                                  mode='markers',
                                  name='Immune',
                                  legendgroup='Immune',
                                  marker=dict(
                                      color='slateblue'
                                  ),
                                  showlegend=True))

        fig2.add_trace(go.Scatter(x=[input_map_size], y=[input_map_size],
                                  mode='markers',
                                  name='Dead',
                                  legendgroup='Dead',
                                  marker=dict(
                                      color='crimson'
                                  ),
                                  showlegend=True))
    else:
        print(zl.timenow(), 'start sim')
        input_zombies, input_infection_chance, input_infection_radius, input_birth_rate, input_nat_death, input_zombie_lifespan, input_total_pop, input_days, input_zombie_speed, input_human_speed, input_map_size = int(
            input_zombies), float(input_infection_chance), int(input_infection_radius), float(
            input_birth_rate), float(input_nat_death), int(input_zombie_lifespan), int(input_total_pop), int(
            input_days), float(input_zombie_speed), float(input_human_speed), int(input_map_size)
        print(zl.timenow(), input_infection_chance, input_infection_radius, input_birth_rate, input_nat_death, input_zombie_lifespan, input_total_pop, input_days, input_zombie_speed, input_human_speed, input_map_size, input_zombies)
        df_hist = zl.Zombie_sim(input_infection_chance, input_infection_radius, input_birth_rate, input_nat_death, input_zombie_lifespan, input_total_pop, input_days, input_zombie_speed, input_human_speed, input_map_size, input_zombies)
        dfp = df_hist.groupby(['population', 'day']).count().reset_index()
        n_clicks = 0
        fig = px.line(dfp, x='day', y='id', color='population', color_discrete_map=pop_colours, title=f'Population counts over {input_days} simulation days')
        fig.update_layout(yaxis_title='population count')
        fig2 = px.scatter(df_hist, x="x_coord", y="y_coord", animation_frame="day", animation_group="id",
                          color="population", color_discrete_map=pop_colours, hover_name="population", title='Scatter map showing the progression of the simulated zombie apocalypse over time',
                          range_x=[0, input_map_size], range_y=[0, input_map_size])
        fig2.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
        fig2.add_trace(go.Scatter(x=[input_map_size], y=[input_map_size],
                                  mode='markers',
                                  name='Immune',
                                  legendgroup='Immune',
                                  marker=dict(
                                      color='slateblue'
                                  ),
                                  showlegend=True))

        fig2.add_trace(go.Scatter(x=[input_map_size], y=[input_map_size],
                                  mode='markers',
                                  name='Dead',
                                  legendgroup='Dead',
                                  marker=dict(
                                      color='crimson'
                                  ),
                                  showlegend=True))

    return fig, fig2

port = 8011

if __name__ == '__main__':
    app.run_server()