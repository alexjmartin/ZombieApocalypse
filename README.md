# ZombieApocalypse
This repository houses the code for the modelling of a Zombie apocalypse over a number of days. It's split in to:
- The WebApp (App: https://zombie-simulator.herokuapp.com/) which allows anyone to run a one off simulation using the simulation module and review the results 
- The core simulation module (zombie_library)
- The zombie_simulator script which is used to run the simulation module multiple times and output the results of these runs to csv

## WebApp
The WebApp simulator can be access at https://zombie-simulator.herokuapp.com, though not guarentees are made for availability and the first run simulation for a session will likely take a few moments to complete. The parameters that can be provided to the simulator are:
|Zombie speed |()– |The ground that can be covered by a zombie in a day|
|---|---|---|
- Human speed – The ground that can be covered by a human in a day
- Zombies – The initial number of zombies which are seeded in a population
- Total pop – The total number of humans across the two distinct populations 
- Birth rate – The speed at which new humans are added to the populations
- Natural death rate – The speed at which new humans die, unrelated to the zombie outbreak
- Zombie lifespan – The approximate lifespan of a zombie within the simulation. Ultimately the lifespan for each zombie is selected from a normal distribution with mean equal to the zombie lifespan and deviation equal to one.
- Map size – This is the square area that participants of the simulation will initial be introduced in, coupled with total pop this allows for varying of populations densities. 


## zombie_library
The core function within the zombie library is that of the Zombie_Sim() function, which takes the parameters described in the WebApp section and runs a simulation for how a specific zombie outbreak would pan out. Within zombie_library there are several helper functions which build the population, simulate the movement of humans and zombies, whether they will become infected and whether humans will be immune. 

## zombie_simulator




