import pandas as pd
import plotly.express as px
import json
import numpy as np
import random
from collections import Counter
import datetime
import plotly.graph_objects as go

## Defauult Variables
zombies = 1

infection_radius = 10

infection_chance = .8

birth_rate = 0.005

nat_death = 0.001

zombie_lifespan = 7

total_pop = 100

days = 30

zombie_speed = 0.4

human_speed = 0.7

immunity_chance = 0.01

vaccine_day = 20

min_travel = -20.5
max_travel = 20.5

map_size = 400

# max variables to change during simulation runs
max_zombies = 2

max_infection_radius = 25

max_infection_chance = 1

max_birth_rate = 0.0005

max_nat_death = 0.0001

max_zombie_lifespan = 10

max_immunity_chance = 0.06

max_vaccine_day = 60

max_vaccine_efficacy = 0.8

max_zombie_speed = 1

max_human_speed = 1

run_id = 0

import sys
sys.path.append('C:\\Users\\alex_\\PycharmProjects\\Zombie')

import zombie_library as zl




for zombies in np.arange(1, max_zombies+1, 1):
    for infection_radius in np.arange(10, max_infection_radius+5, 5):
        for infection_chance in np.arange(0.1, max_infection_chance, 0.1):
            for zombie_speed in np.arange(0.1, max_zombie_speed, 0.1):
                for human_speed in np.arange(0.1, max_human_speed, 0.1):
                    for zombie_lifespan in np.arange(5, max_zombie_lifespan, 1):
                        for vaccine_day in np.arange(20,max_vaccine_day,10):
                            for immunity_chance in np.arange(0.0, max_immunity_chance, 0.01):
                                for vaccine_efficacy in np.arange(0.5, max_vaccine_efficacy, 0.1):
                                    run_id = run_id + 1
                                    if run_id % 100 == 0:
                                        print(f'{timenow()} {run_id}')
                                    df_hist = zl.Zombie_sim(infection_chance, infection_radius, birth_rate, nat_death, zombie_lifespan, total_pop, days, zombie_speed, human_speed, map_size, zombies, immunity_chance, vaccine_day, vaccine_efficacy, min_travel, max_travel)
                                    df_hist['zombies'] = zombies
                                    df_hist['infection_radius'] = infection_radius
                                    df_hist['infection_chance'] = infection_chance
                                    df_hist['zombie_speed'] = zombie_speed
                                    df_hist['human_speed'] = human_speed
                                    df_hist['zombie_lifespan'] = zombie_lifespan
                                    df_hist['vaccine_day'] = vaccine_day
                                    df_hist['run_id'] = run_id
                                    if run_id == 1:
                                        df_tracker = df_hist.copy()
                                    else:
                                        df_tracker = df_tracker.append(df_hist, ignore_index=True)

    print(f'Done for {zombies}')
t = round(zl.timenow().timestamp())
df_tracker.to_csv(f'zombie_tracker_{t}.csv')