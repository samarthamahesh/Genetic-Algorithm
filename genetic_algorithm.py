import json
import random
from client_moodle import *

ARRAY_SIZE = 11
POPULATION_SIZE = 200
RANGES = [[9.9, 10], [-5.2, -5.1], [-6.45, -6.4], [0.064, 0.065], [0.03, 0.04], [9.73e-05, 9.74e-05], [-6.1e-05, -6e-05], [-1.28e-07, -1.27e-07], [3.4e-08, 3.5e-08], [3.6e-11, 3.7e-11], [-6.7e-12, -6.8e-12]]

# Function for returning mutated genes
def mutated_genes(x):
    return random.uniform(-10, 10)

# Function for mating between parents to produce offspring
def mate(parent1, parent2):
    child_chromosome = np.empty(ARRAY_SIZE)
    for i in range(ARRAY_SIZE):
        prob = random.random()
        if prob < 0.45:
            child_chromosome[i] = parent1[i]
        elif prob < 0.9:
            child_chromosome[i] = parent2[i]
        else:
            child_chromosome[i] = mutated_genes(i)
    return Individual(list(child_chromosome))

# Class for an individual
class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = get_errors('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', chromosome)

if __name__ == "__main__":
    # Initial population
    population = []

    # Create initial individual
    for i in range(POPULATION_SIZE):
        arr = []
        for j in range(11):
            tmp = random.uniform(RANGES[j][0], RANGES[j][1])
            arr.append(tmp)
        population.append(Individual(arr))

    # f = open('out.txt', 'r')
    # arr = f.read()
    # li = json.loads(arr)
    # for i in range(len(li)):
    #     population.append(Individual(li[i]))

    rounds = 0

    while True:
        # Sort population based on fitness function
        population.sort(key=lambda x: x.fitness[0] + x.fitness[1])

        # Print population errors
        print("ROUND: ", rounds, len(population))
        for i in range(POPULATION_SIZE):
            print(population[i].fitness)
        print()

        # After required number of generations, break the algo
        if rounds >= 5:
            temp = []
            for i in range(POPULATION_SIZE):
                print(population[i].chromosome)
                temp.append(population[i].chromosome)
            output_file = open('out.txt', 'w')
            arr = json.dumps(temp)
            output_file.write(arr)
            output_file.close()
            break

        # New generation
        new_generation = []

        # Top 10% of population having minimum validation error go directly to next generation
        s = int(POPULATION_SIZE/10)
        for i in range(s):
            new_generation.append(population[i])

        # Rest 90% comes from mating between the parents with rare mutations with low probability
        s *= 9
        for i in range(s):
            par1 = random.randint(0, POPULATION_SIZE//20)
            par2 = random.randint(0, POPULATION_SIZE//20)

            new_generation.append(mate(population[par1].chromosome, population[par2].chromosome))

        population = new_generation
        rounds += 1

    # Submit the best individual from latest generation
    err = submit('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', population[0].chromosome)
    print(err)