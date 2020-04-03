import json
import random
from client_moodle import *

ARRAY_SIZE = 11
POPULATION_SIZE = 30
RANGES = [[-10, 10], [-10, 10], [-0.06, 0.06], [-0.06, 0.06], [-5*1e-08, 5*1e-08], [-5*1e-08, 5*1e-08], [-1e-13, 1e-13], [-1e-13, 1e-13], [-1e-14, 1e-14], [-1e-14, 1e-14], [-1e-14, 1e-14]]

trace_file = open('trace.txt', 'a')

# Function for performing mutation
def mutation(chromosome):
    Mutation_position = random.randint(0,10)
    trace_file.write("Mutation point -> " + str(Mutation_position) + "\n")
    
    lo,hi = RANGES[Mutation_position][0],RANGES[Mutation_position][1]
    mut_change = random.uniform(lo,hi)
    chromosome[Mutation_position] = mut_change
    trace_file.write("Offspring vector after mutation -> " + str(chromosome) + "\n")
    
# Function for mating between parents to produce offspring
def mate(parent1, parent2):
    child_chromosome = np.empty(ARRAY_SIZE)
    point = random.randint(1, 9)
    trace_file.write("Cross over point -> " + str(point) + "\n")

    for i in range(point):
        child_chromosome[i] = parent1[i]
    for i in range(point, ARRAY_SIZE):
        child_chromosome[i] = parent2[i]
    child_chromosome = list(child_chromosome)
    trace_file.write("Offspring vector -> " + str(child_chromosome) + "\n")
    
    mutation(child_chromosome)
    return Individual(child_chromosome)

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

    trace_file.write("Population Size : 30\n")
    trace_file.write("\nInitial Population : \n")
    for i in range(POPULATION_SIZE):
        trace_file.write(str(i+1) + ". Vector -> " + str(population[i].chromosome) + " Errors -> " + str(population[i].fitness) + " Fitness score -> " + str(population[i].fitness[0]+population[i].fitness[1]) + "\n")

    rounds = 1

    while True:
        # After required number of generations, break the algo
        if rounds > 10:
            break

        # Sort population based on fitness function
        population.sort(key=lambda x: x.fitness[0] + x.fitness[1])

        # Print population errors
        print("ROUND: ", rounds, len(population))
        for i in range(POPULATION_SIZE):
            print(population[i].fitness)
            print(population[i].chromosome)
        print()

        trace_file.write("\nRound Number : " + str(rounds) + "\n")
        trace_file.write("\nPopulation : \n")
        for i in range(POPULATION_SIZE):
            trace_file.write(str(i+1) + ". Vector -> " + str(population[i].chromosome) + " Errors -> " + str(population[i].fitness) + " Fitness score -> " + str(population[i].fitness[0]+population[i].fitness[1]) + "\n")

        # New generation
        new_generation = []

        # Top 10% of population having minimum validation error go directly to next generation
        trace_file.write("\nTop 10% Individuals directly enter next generation\n")
        s = int(POPULATION_SIZE/10)
        for i in range(s):
            new_generation.append(population[i])
            trace_file.write("Vector -> " + str(population[i].chromosome) + " Errors -> " + str(population[i].fitness) + " Fitness -> " + str(population[i].fitness[0] + population[i].fitness[1]) + "\n")

        # Rest 90% comes from mating between the parents with rare mutations with low probability
        trace_file.write("\nRest 90% Inviduals come from crossing\n")
        s *= 9
        i = 0
        while i < s:
            par1 = random.randint(0, POPULATION_SIZE//10)
            par2 = random.randint(0, POPULATION_SIZE//10)

            if par1 == par2:
                continue
            
            trace_file.write("\nOffspring " + str(i+1) + "\n")
            trace_file.write("Parent 1 (" + str(par1+1) + ") -> " + str(population[par1].chromosome) + " Errors -> " + str(population[par1].fitness) + " Fitness -> " + str(population[par1].fitness[0] + population[par1].fitness[1]) + "\n")
            trace_file.write("Parent 2 (" + str(par2+1) + ") -> " + str(population[par2].chromosome) + " Errors -> " + str(population[par2].fitness) + " Fitness -> " + str(population[par2].fitness[0] + population[par2].fitness[1]) + "\n")
            new_generation.append(mate(population[par1].chromosome, population[par2].chromosome))

            i += 1

        population = new_generation
        trace_file.write("\nNew generation : \n")
        for i in range(POPULATION_SIZE):
            trace_file.write(str(i+1) + ". Vector -> " + str(population[i].chromosome) + " Errors -> " + str(population[i].fitness) + " Fitness score -> " + str(population[i].fitness[0]+population[i].fitness[1]) + "\n")

        rounds += 1

    # Submit the best individual from latest generation
    err = submit('VXD6PTcfgsKccNf66cip6D3O44SsqI11uaORwBaR9HtS4nyDEY', population[0].chromosome)
    print(err)