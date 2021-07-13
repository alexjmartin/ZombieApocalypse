# Module to define the Zombie simulation functions
import random
import datetime
import numpy as np
import pandas as pd
from collections import Counter

def infect(current_status, infection_chance, immunity_chance):
    if (random.random() < immunity_chance) & (current_status != 5):
        status = 5
    elif (random.random() < infection_chance) & (current_status != 5):
        status = 3
    else:
        status = current_status
    return status

def proximity_test(zombie_x, zombie_y, person_x, person_y, infection_radius):
    in_radii = (zombie_x - person_x) ** 2 + (zombie_y - person_y) ** 2 <= infection_radius ** 2
    # calc = (person_x - zombie_x)^2 + (person_y - zombie_y)^2
    in_radius = True in in_radii
    return in_radius

def movement(speed, x_coord, y_coord, random_move):
    x = x_coord + speed * random_move[0]
    y = y_coord + speed * random_move[1]
    return x, y

def timenow():
    now = datetime.datetime.now()
    return now

def pop_add(n, map_size, pop='uninfected'):
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

def Zombie_sim(infection_chance=0.8, infection_radius=20, birth_rate=0.005, nat_death=0.001, zombie_lifespan=7, total_pop=400, days=30,
               zombie_speed=0.5, human_speed=0.7, map_size=400, zombies=1, immunity_chance=0.01, vaccine_day=90, vaccine_efficacy = 0.8, min_travel=-20.5, max_travel=20.5):
    start_time = timenow()
    df = pd.DataFrame({0: [], 1: [], 2: [], 3: []})
    df = df.append(pd.DataFrame(pop_add(total_pop, map_size)))

    df = df.append(pd.DataFrame(pop_add(zombies, map_size, 'Zombie')))

    df = df.rename(columns={0: 'x_coord', 1: 'y_coord', 2: 'population', 3: 'days_infected'})

    df['id'] = range(total_pop + zombies)

    df.index = df['id']

    df_hist = pd.DataFrame({0: [], 1: [], 2: [], 3: [], 4: []})

    df_hist = df_hist.rename(columns={0: 'x_coord', 1: 'y_coord', 2: 'population', 3: 'days_infected', 4: 'day'})

    for day in range(days):
        df['day'] = day
        #  print(f'{timenow()} Start of day {day}')
        df_hist = df_hist.append(df)

        if day >= vaccine_day:
            immunity_chance = vaccine_efficacy

        uninfected_list = list(df.query('population not in [3,4]').id.values)

        zombie_x, zombie_y = df[df['population'] == 3][['x_coord']].values, df[df['population'] == 3][
            ['y_coord']].values

        for nz in uninfected_list:
            #            print('nz is', nz)
            if random.random() < nat_death:
                #                print('nat death')
                df.iloc[nz, 2] = 4
            else:
                person_x = df['x_coord'][nz]
                person_y = df['y_coord'][nz]
                if proximity_test(zombie_x, zombie_y, person_x, person_y, infection_radius) == True:
                    df.iloc[nz, 2] = infect(df.iloc[nz, 2], infection_chance, immunity_chance)

        # Movement of non-dead people
        a = df.query("population not in [4,3]").iloc[:, 0]
        b = df.query("population not in [4,3]").iloc[:, 1]

        random_movement = [np.random.uniform(min_travel, max_travel, len(a)), np.random.uniform(min_travel, max_travel, len(a))]

        df.iloc[a.index, 0], df.iloc[a.index, 1] = movement(human_speed, a, b, random_movement)

        # Movement of zombies
        a = df.query("population == 3").iloc[:, 0]
        b = df.query("population == 3").iloc[:, 1]

        random_movement = [np.random.uniform(min_travel, max_travel, len(a)), np.random.uniform(min_travel, max_travel, len(a))]

        df.iloc[a.index, 0], df.iloc[a.index, 1] = movement(zombie_speed, a, b, random_movement)
        #    print(f'{timenow()} Movement done for day {day}')

        # determine any births
        remaining_humans = len(uninfected_list)
        birthlist = np.array([])
        for i in range(remaining_humans):
            n = random.random()
            birthlist = np.append(birthlist, n)

        new_borns = Counter(birthlist < birth_rate)[True]

        babies = pop_add(new_borns, map_size)

        baby_list = []

        d = df['id'].max()

        for p in babies:
            d = d + 1 # get next id for df_hist
            baby_dict = {}
            baby_dict['x_coord'] = p[0]
            baby_dict['y_coord'] = p[1]
            baby_dict['population'] = p[2]
            baby_dict['days_infected'] = p[3]
            baby_dict['id'] = d
            baby_dict['day'] = day
            baby_list.append(baby_dict)

        df = df.append(baby_list, ignore_index=True)

        infections = Counter(df.query('population == 3 and days_infected == 1')['population'])[3]

        ndeaths = Counter(df.query('population == 4')['population'])[4]

        #print(f'{timenow()} Day {day}: {infections} people were infected today, {new_borns} babies were born, {ndeaths} deaths occured naturally')

        # increment days infected for Zombies
        df.loc[df['population'] == 3, 'days_infected'] += 1

        # Determine if Zombies die
        mu, sigma = zombie_lifespan, 1  # mean and standard deviation for zombie lifespan population
        s = np.random.normal(mu, sigma, len(df.iloc[:,2] == 3))  # generate random normally disributed samples around the zombie_lifespan
        y = df.iloc[:, 3] > s   # Test if each zombie has been infected longer than lifespan gen
        update_indexes = y[y].index.values # indexes for zombies which have lived longer than lifespan gen
        update_values = np.repeat(4, len(update_indexes)) # create list of values to apply to dataframe
        df.loc[update_indexes, ["population"]] = update_values # Update zombies to dead where applicable

    # Update populations to a more readable format
    df_hist.loc[df_hist.population == 1, "population"] = "Population_1"
    df_hist.loc[df_hist.population == 2, "population"] = "Population_2"
    df_hist.loc[df_hist.population == 3, "population"] = "Zombie"
    df_hist.loc[df_hist.population == 4, "population"] = "Dead"
    df_hist.loc[df_hist.population == 5, "population"] = "Immune"

    end_time = timenow()
    delta = end_time - start_time
 #   print(f'Duration of run for {days} days was {delta}')
    return df_hist