import json
import random
from client_moodle import *

ARRAY_SIZE = 11
POPULATION_SIZE = 10

# Function for returning mutated genes
def mutated_genes(x):
    y = x/10
    return x+random.uniform(-y, y)

# Function for mating between parents to produce offspring
def mate(parent1, parent2):
    child_chromosome = np.empty(ARRAY_SIZE)
    point = random.randint(1, 9)
    for i in range(point):
        child_chromosome[i] = parent1[i]
    for i in range(point+1, 11):
        child_chromosome[i] = parent2[i]
    mut_point = random.randint(1, 10)
    child_chromosome[mut_point] = mutated_genes(child_chromosome[mut_point])
    return Individual(list(child_chromosome))

# Class for an individual
class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = get_errors('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', chromosome)

if __name__ == "__main__":
    # Initial population
    population = []

    # Read initial individual from given overfit weights array
    input_file = open('out.txt', 'r')
    arr = input_file.read()
    arr = json.loads(arr)
    for i in range(len(arr)):
        population.append(Individual(arr[i]))

    rounds = 0

    while True:
        # Sort population based on fitness function
        population.sort(key=lambda x: x.fitness[0] + x.fitness[1])

        # Print population errors
        print("ROUND: ", rounds)
        for i in range(POPULATION_SIZE):
            print(population[i].fitness)
        print()

        # After required number of generations, break the algo
        if rounds >= 10:
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
        s = (20*POPULATION_SIZE)//100
        for i in range(s):
            new_generation.append(population[i])

        # Rest 90% comes from mating between the parents with rare mutations with low probability
        s *= 3
        for i in range(s):
            for j in range(i+1, s):
                if i == j:
                    continue
                new_generation.append(mate(population[i].chromosome, population[j].chromosome))

        population = new_generation
        rounds += 1

    # Submit the best individual from latest generation
    err = submit('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', population[0].chromosome)
    print(err)