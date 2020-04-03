import json
import random
from client_moodle import *

ARRAY_SIZE = 11
POPULATION_SIZE = 30
RANGES = [[-10, 10], [-10, 10], [-0.06, -0.06], [-0.06, 0.06], [-5*1e-08, 5*1e-08], [-5*1e-08, 5*1e-08], [-1e-14, 1e-14], [-1e-14, 1e-14], [-1e-14, 1e-14], [-1e-13, 1e-13], [-1e-13, 1e-13]]

# Function for performing mutation
def mutation(chromosome):
    # for i in range(ARRAY_SIZE):
    Mutation_position = random.randint(0,10)
    # prob = random.random()
    #     if prob < 0.1:
    lo,hi = RANGES[Mutation_position][0],RANGES[Mutation_position][1]
    mut_change = random.uniform(lo,hi)
    chromosome[Mutation_position] = mut_change
    
    # g = random.uniform(-1,1)
    # return x + g

# Function for mating between parents to produce offspring
def mate(parent1, parent2):
    child_chromosome = np.empty(ARRAY_SIZE)
    point = random.randint(1, 9)
    for i in range(point):
        child_chromosome[i] = parent1[i]
    for i in range(point, ARRAY_SIZE):
        child_chromosome[i] = parent2[i]
    # for i in range(ARRAY_SIZE):
    #     prob = random.random()
    #     if prob < 0.5:
    #         child_chromosome[i] = parent1[i]
    #     else:
    #         child_chromosome[i] = parent2[i]
    mutation(child_chromosome)
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
        for j in range(ARRAY_SIZE):
            tmp = random.uniform(RANGES[j][0], RANGES[j][1])
            arr.append(tmp)
        population.append(Individual(arr))

    # f = open('out.txt', 'r')
    # arr = f.read()
    # li = json.loads(arr)
    # for i in range(len(li)):
    #     population.append(Individual(li[i]))

    rounds = 0

    f1 = open('result.txt', 'a')

    while True:
        # Sort population based on fitness function
        population.sort(key=lambda x: x.fitness[0] + x.fitness[1])

        # Print population errors
        print("ROUND: ", rounds, len(population))
        for i in range(POPULATION_SIZE):
            print(population[i].fitness)
            print(population[i].chromosome)
            f1.write(str(population[i].fitness)+"\n")
            f1.write(str(population[i].chromosome)+"\n")
        print()

        # After required number of generations, break the algo
        if rounds >= 20:
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