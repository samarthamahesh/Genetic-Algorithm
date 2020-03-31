import json
import random

population = []

input_file = open('best.txt', 'r')
arr = input_file.read()
arr = json.loads(arr)
population.append(arr)
input_file.close()

for i in range(9):
    chromosome = population[0]
    ind = random.randint(1, 10)
    x = chromosome[ind]/100
    chromosome[ind] += random.uniform(-x, x)
    population.append(chromosome)

output_file = open('out.txt', 'w')
arr = json.dumps(population)
output_file.write(arr)
output_file.close()