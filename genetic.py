import numpy as np
import copy
from car import Car
from nn import NeuralNetwork

def calculate_fitness(car):
    return car.time_alive * car.speed

def mutate_matrix(matrix, mutation_rate=0.1, mutation_scale=0.2):
    mask = np.random.rand(*matrix.shape) < mutation_rate
    noise = np.random.normal(0, mutation_scale, size=matrix.shape)
    matrix[mask] += noise[mask]

def crossover(parent_a_nn, parent_b_nn, mutation_rate=0.1):
    child_nn = NeuralNetwork(input_size=7, hidden_size=6, output_size=1)

    mask_w1 = np.random.rand(*parent_a_nn.w1.shape) < 0.5
    child_nn.w1 = np.where(mask_w1, parent_a_nn.w1, parent_b_nn.w1)

    mask_b1 = np.random.rand(*parent_a_nn.b1.shape) < 0.5
    child_nn.b1 = np.where(mask_b1, parent_a_nn.b1, parent_b_nn.b1)

    mask_w2 = np.random.rand(*parent_a_nn.w2.shape) < 0.5
    child_nn.w2 = np.where(mask_w2, parent_a_nn.w2, parent_b_nn.w2)

    mask_b2 = np.random.rand(*parent_a_nn.b2.shape) < 0.5
    child_nn.b2 = np.where(mask_b2, parent_a_nn.b2, parent_b_nn.b2)

    mutate_matrix(child_nn.w1, mutation_rate)
    mutate_matrix(child_nn.b1, mutation_rate)
    mutate_matrix(child_nn.w2, mutation_rate)
    mutate_matrix(child_nn.b2, mutation_rate)

    return child_nn

def next_generation(old_population, pop_size=50, mutation_rate=0.1, start_pos=(110, 300), start_angle=0):
    sorted_cars = sorted(old_population, key=lambda c: c.total_fitness if c.total_fitness > 0 else calculate_fitness(c), reverse=True)
    new_population = []

    # Elitism (10%)
    num_elites = max(1, int(pop_size * 0.1))
    for i in range(num_elites):
        elite_car = Car(start_pos[0], start_pos[1], start_angle)
        elite_car.brain = copy.deepcopy(sorted_cars[i].brain)
        new_population.append(elite_car)

    # Breeding Pool (30%)
    mating_pool = sorted_cars[:max(2, int(pop_size * 0.3))]

    # Crossover & Mutation
    while len(new_population) < pop_size:
        p_a = np.random.choice(mating_pool)
        p_b = np.random.choice(mating_pool)
        child_car = Car(start_pos[0], start_pos[1], start_angle)
        child_car.brain = crossover(p_a.brain, p_b.brain, mutation_rate)
        new_population.append(child_car)

    return new_population