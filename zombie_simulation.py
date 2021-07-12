import pandas as pd
import plotly.express as px
import json
import numpy as np
import random
from collections import Counter
import datetime
import plotly.graph_objects as go
# from numba import jit
# import numba

## Variables
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

min_travel = -20.5
max_travel = 20.5

map_size = 400

variable_list = (
'zombies', 'infection_radius', 'infection_chance', 'birth_rate', 'nat_death', 'zombie_lifespan', 'total_pop',
'map_size')


def infect(current_status):
    if (random.random() < infection_chance) & (current_status != 5):
        status = 3
    else:
        status = 5
    return status

def proximity_test(zombie_x, zombie_y, person_x, person_y):
    in_radii = (zombie_x - person_x) ** 2 + (zombie_y - person_y) ** 2 <= infection_radius ** 2
    # calc = (person_x - zombie_x)^2 + (person_y - zombie_y)^2
    in_radius = True in in_radii
    return in_radius


def movement(speed, x_coord, y_coord, random_move):
    x = x_coord + speed * random_move
    y = y_coord + speed * random_move
    return x, y


def timenow():
    now = datetime.datetime.now()
    return now

def pop_add(n, pop='uninfected'):
    pop_list = []
    for num in range(n):
        if pop == 'Zombie':
            a = random.choices(range(int(map_size / 2), map_size), k=2)
            a.append(3)  # 3 demarks a Zombie population
        else:
            pop = random.choice([1, 2])  # Select population person is added to
            if pop == 1:
                a = random.choices(range(int(map_size / 2)), k=2)
            else:
                a = random.choices(range(int(map_size / 2), map_size), k=2)
            a.append(pop)
        a.append(0)  # everyone starts with zero days infected
        pop_list.append(a)
    return pop_list


# def zombie_death(zombie_lifespan):


def Zombie_sim(infection_chance, infection_radius, birth_rate, nat_death, zombie_lifespan, total_pop, days,
               zombie_speed, human_speed, min_travel, max_travel, map_size, zombies=1):
    start_time = timenow()
    df = pd.DataFrame({0: [], 1: [], 2: [], 3: []})
    df = df.append(pd.DataFrame(pop_add(total_pop)))

    df = df.append(pd.DataFrame(pop_add(zombies, 'Zombie')))

    df = df.rename(columns={0: 'x_coord', 1: 'y_coord', 2: 'population', 3: 'days_infected'})

    df['id'] = range(total_pop + zombies)

    df.index = df['id']

    stage1 = timenow() - start_time

    uninfected_list = []
    df_hist = pd.DataFrame({0: [], 1: [], 2: [], 3: [], 4: []})

    df_hist = df_hist.rename(columns={0: 'x_coord', 1: 'y_coord', 2: 'population', 3: 'days_infected', 4: 'day'})

    for day in range(days):
        df['day'] = day
        #  print(f'{timenow()} Start of day {day}')
        df_hist = df_hist.append(df)

        infect_list = []

        zombie_list = []

        uninfected_list = list(df.query('population not in [3,4]').id.values)

        zombie_x, zombie_y = df[df['population'] == 3][['x_coord']].values, df[df['population'] == 3][
            ['y_coord']].values

        stage2 = timenow() - stage1

        for nz in uninfected_list:
            #            print('nz is', nz)
            if random.random() < nat_death:
                #                print('nat death')
                df.iloc[nz, 2] = 4
            else:
                person_x = df['x_coord'][nz]
                person_y = df['y_coord'][nz]
                if proximity_test(zombie_x, zombie_y, person_x, person_y) == True:
                    df.iloc[nz, 2] = infect(df.iloc[nz, 2])

        # Movement of non-dead people
        a = df.query("population not in [4,3]").iloc[:, 0]
        b = df.query("population not in [4,3]").iloc[:, 1]

        random_movement = np.random.uniform(min_travel, max_travel, len(a))

        df.iloc[a.index, 0], df.iloc[a.index, 1] = movement(human_speed, a, b, random_movement)

        # Movement of zombies
        a = df.query("population == 3").iloc[:, 0]
        b = df.query("population == 3").iloc[:, 1]

        random_movement = np.random.uniform(min_travel, max_travel, len(a))

        df.iloc[a.index, 0], df.iloc[a.index, 1] = movement(zombie_speed, a, b, random_movement)
        #    print(f'{timenow()} Movement done for day {day}')

        # determine any births
        remaining_humans = len(uninfected_list)
        birthlist = np.array([])
        for i in range(remaining_humans):
            n = random.random()
            birthlist = np.append(birthlist, n)

        new_borns = Counter(birthlist < birth_rate)[True]

        a = pop_add(new_borns)

        aaa = []

        d = df['id'].max()

        for p in a:
            d = d + 1
            ddd = {}
            ddd['x_coord'] = p[0]
            ddd['y_coord'] = p[1]
            ddd['population'] = p[2]
            ddd['days_infected'] = p[3]
            ddd['id'] = d
            ddd['day'] = day
            aaa.append(ddd)

        df = df.append(aaa, ignore_index=True)

        infections = Counter(df.query('population == 3 and days_infected == 1')['population'])[3]

        ndeaths = Counter(df.query('population == 4')['population'])[4]

       # print(
       #     f'{timenow()} Day {day}: {infections} people were infected today, {new_borns} babies were born, {ndeaths} deaths occured naturally')

        # increment days infected for Zombies
        df.loc[df['population'] == 3, 'days_infected'] += 1

    end_time = timenow()
    delta = end_time - start_time
 #   print(f'Duration of run for {days} days was {delta}')
    return df_hist

max_zombies = 2

max_infection_radius = 25

max_infection_chance = 1

max_birth_rate = 0.005

max_nat_death = 0.001

max_zombie_lifespan = 7

max_zombie_speed = 1

max_human_speed = 1

run_id = 0

import sys
sys.path.append('C:\\Users\\alex_\\PycharmProjects\\Zombie')

import zombie_library as zl




for zombies in np.arange(1, max_zombies+1, 1):
    for infection_radius in np.arange(5, max_infection_radius+5, 5):
        for infection_chance in np.arange(0.1, max_infection_chance, 0.1):
            for zombie_speed in np.arange(0.1, max_zombie_speed, 0.1):
                for human_speed in np.arange(0.1, max_human_speed, 0.1):
                    run_id = run_id + 1
                    if run_id % 100 == 0:
                        print(f'{timenow()} {run_id}')
                    df_hist = zl.Zombie_sim(infection_chance, infection_radius, birth_rate, nat_death, zombie_lifespan, total_pop, days, zombie_speed, human_speed, map_size, zombies, min_travel, max_travel)
                    df_hist['zombies'] = zombies
                    df_hist['infection_radius'] = infection_radius
                    df_hist['infection_chance'] = infection_chance
                    df_hist['zombie_speed'] = zombie_speed
                    df_hist['human_speed'] = human_speed
                    df_hist['zombie_lifespan'] = zombie_lifespan
                    df_hist['run_id'] = run_id
                    if run_id == 1:
                        df_tracker = df_hist.copy()
                    else:
                        df_tracker = df_tracker.append(df_hist, ignore_index=True)

    print(f'Done for {zombies}')
t = round(timenow().timestamp())
df_tracker.to_csv(f'zombie_tracker_{t}.csv')
#df_hist.to_csv('zombie_tracker.csv')