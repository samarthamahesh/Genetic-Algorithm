import json
import random
from client_moodle import *

ARRAY_SIZE = 11
POPULATION_SIZE = 10

# Function for returning mutated genes
def mutated_genes():
    return random.uniform(-10, 10)

# Function for mating between parents to produce offspring
def mate(parent1, parent2):
    child_chromosome = np.empty(ARRAY_SIZE)
    for i in range(ARRAY_SIZE):
        probability = random.random()
        if probability < 0.45:
            child_chromosome[i] = parent1[i]
        elif probability < 0.90:
            child_chromosome[i] = parent2[i]
        else:
            child_chromosome[i] = mutated_genes()
    return Individual(list(child_chromosome))

# Class for an individual
class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = get_errors('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', chromosome)

if __name__ == "__main__":
    # Initial population
    population = []

    # Read an individual from given overfit weights array
    input_file = open('overfit.txt', 'r')
    arr = input_file.read()
    arr = json.loads(arr)
    population.append(Individual(arr))

    # Create initial population
    for i in range(POPULATION_SIZE-1):
        population.append(Individual(list(np.random.uniform(-10, 10, ARRAY_SIZE))))

    rounds = 0

    while true:
        # Sort population based on validation error
        population.sort(key=lambda x: x.fitness[1])

        # Print population errors
        print("ROUND: ", rounds)
        for i in range(POPULATION_SIZE):
            print(population[i].fitness)
        print()

        # After required number of generations, break the algo
        if rounds >= 14:
            for i in range(POPULATION_SIZE):
                print(population[i].chromosome)
            break

        # New generation
        new_generation = []

        # Top 10% of population having minimum validation error go directly to next generation
        s = (10*POPULATION_SIZE)//100
        for i in range(s):
            new_generation.append(population[i])

        # Rest 90% comes from mating between the parents with rare mutations with low probability
        s = POPULATION_SIZE - s
        for i in range(s):
            par1 = random.randint(0, POPULATION_SIZE//2)
            par2 = random.randint(0, POPULATION_SIZE//2)
            new_generation.append(mate(population[par1].chromosome, population[par2].chromosome))

        population = new_generation
        rounds += 1

    # Submit the best individual from latest generation
    err = submit('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', population[0].chromosome)
    print(err)