import json
import random
from client_moodle import *

ARRAY_SIZE = 11
POPULATION_SIZE = 10

print(ARRAY_SIZE)

def mutated_genes():
    return random.uniform(-10, 10)

def mate(parent1, parent2):
    child_chromosome = np.empty(ARRAY_SIZE)
    for i in range(ARRAY_SIZE):
        num = random.random()
        if num < 0.45:
            child_chromosome[i] = parent1[i]
        elif num < 0.90:
            child_chromosome[i] = parent2[i]
        else:
            child_chromosome[i] = mutated_genes()
    return Individual(list(child_chromosome))

class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = get_errors('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', chromosome)

if __name__ == "__main__":
    population = []

    input_file = open('overfit.txt', 'r')
    arr = input_file.read()
    arr = json.loads(arr)

    population.append(Individual(arr))

    for i in range(POPULATION_SIZE):
        population.append(Individual(list(np.random.uniform(-10, 10, ARRAY_SIZE))))

    found = False
    rounds = 0

    while found == False:
        population.sort(key=lambda x: x.fitness)

        print("ROUND: ", rounds)
        for i in range(POPULATION_SIZE):
            print(population[i].fitness)
        print()

        if rounds >= 14:
            for i in range(POPULATION_SIZE):
                print(population[i].chromosome)
            break

        new_generation = []

        s = (10*POPULATION_SIZE)//100
        for i in range(s):
            new_generation.append(population[i])

        s = POPULATION_SIZE - s
        for i in range(s):
            par1 = random.randint(0, POPULATION_SIZE//2)
            par2 = random.randint(0, POPULATION_SIZE//2)
            new_generation.append(mate(population[par1].chromosome, population[par2].chromosome))

        population = new_generation
        rounds += 1

    err = submit('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', population[0].chromosome)

    print(err)