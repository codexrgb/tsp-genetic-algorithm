import json
import os
import random
import imageio
import matplotlib.pyplot as plt
from utils import distance

# Load cities
def load_cities(path):
    with open(path, "r") as f:
        data = json.load(f)
    return {int(k): tuple(v) for k, v in data.items()}

# Genetic Algorithm functions
def total_distance(route, cities):
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i+1) % len(route)]])
    return dist

def create_population(size, num_cities):
    pop = []
    base = list(range(num_cities))
    for _ in range(size):
        route = base[:]
        random.shuffle(route)
        pop.append(route)
    return pop

def selection(population, cities):
    chosen = random.sample(population, 3)
    chosen.sort(key=lambda r: total_distance(r, cities))
    return chosen[0]

def crossover(p1, p2):
    a, b = sorted(random.sample(range(len(p1)), 2))
    child = [None] * len(p1)
    child[a:b] = p1[a:b]

    pos = 0
    for gene in p2:
        if gene not in child:
            while child[pos] is not None:
                pos += 1
            child[pos] = gene
    return child

def mutate(route):
    if random.random() < 0.02:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]
    return route

# Draw frame
def draw_route(route, cities, filename):
    xs = [cities[i][0] for i in route] + [cities[route[0]][0]]
    ys = [cities[i][1] for i in route] + [cities[route[0]][1]]

    plt.figure(figsize=(6, 5))
    plt.plot(xs, ys, marker="o")
    for idx in route:
        plt.text(cities[idx][0], cities[idx][1], str(idx))

    plt.title("TSP Route Evolution")
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

# Main animation generator
def generate_animation(cities_path="data/sample_cities.json", output="output/tsp_route.gif"):
    cities = load_cities(cities_path)
    population = create_population(100, len(cities))
    frames = []

    for gen in range(300):
        new_pop = []
        for _ in range(100):
            p1 = selection(population, cities)
            p2 = selection(population, cities)
            child = crossover(p1, p2)
            mutate(child)
            new_pop.append(child)
        population = new_pop

        # Get best candidate
        best = min(population, key=lambda r: total_distance(r, cities))

        # Save frame
        frame_path = f"output/frame_{gen}.png"
        draw_route(best, cities, frame_path)
        frames.append(frame_path)

        if gen % 50 == 0:
            print(f"Generated frame: {gen}")

    # Create GIF
    images = [imageio.imread(f) for f in frames]
    imageio.mimsave(output, images, duration=0.12)

    print(f"\nGIF saved to: {output}")

if __name__ == "__main__":
    generate_animation()
