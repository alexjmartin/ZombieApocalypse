# ZombieApocalypse
This repository houses the code for the modelling of a Zombie apocalypse over a number of days. It's split in to:
- The WebApp (App: https://zombie-simulator.herokuapp.com/) which allows anyone to run a one off simulation using the simulation module and review the results 
- The core simulation module (zombie_library)
- The zombie_simulation script which is used to run the simulation module multiple times and output the results of these runs to csv

## WebApp
The WebApp simulator can be access at https://zombie-simulator.herokuapp.com, though not guarentees are made for availability and the first run simulation for a session will likely take a few moments to complete. The parameters that can be provided to the simulator are:
|Parameter|Expected values|Purposed|
|---|---|---|
|Zombies |1-10 |The initial number of zombies which are seeded in a population|
|Infection chance  |0.1–1 |The probability that any encounter for a person within the infection radius will result in an infection, this is expressed as a value between 0 and 1, with the derived “immunity chance” being 1 – the infection chance|
|Infection radius  |5–100 |The distance over which a zombie may feasibly infect a person for that specific day |
|Zombie speed |0.1–1 |The ground that can be covered by a zombie in a day|
|Human speed |0.1–1 |The ground that can be covered by a human in a day|
|Total pop |100-10,000 |The total number of humans across the two distinct populations |
|Birth rate |0.0001–1 |The speed at which new humans are added to the populations|
|Natural death rate |0.0001–1 |The speed at which new humans die, unrelated to the zombie outbreak|
|Zombie lifespan |1-100 |The approximate lifespan of a zombie within the simulation. Ultimately the lifespan for each zombie is selected from a normal distribution with mean equal to the zombie lifespan and deviation equal to one|
|Map size |100-1000 |This is the square area that participants of the simulation will initial be introduced in, coupled with total pop this allows for varying of populations densities.|
|Immunity Chance |0.01–1 |The probability of an infection event resulting in immunity for the human |
|Vaccine efficacy |0.1-1 | The effectiveness of the vaccine once it is introduced, this value will update immunity chance on the vaccine day|
|Vaccine day |1-120 |The day in the simulation when the vaccine will be introduced (all people are assumed to be instantly vaccinated)|
|Days |1-120 |The number of days which the simulation will run for|


## zombie_library
The core function within the zombie library is that of the Zombie_Sim() function, which takes the parameters described in the WebApp section and runs a simulation for how a specific zombie outbreak would pan out. Within zombie_library there are several helper functions which build the population, simulate the movement of humans and zombies, whether they will become infected and whether humans will be immune. 



