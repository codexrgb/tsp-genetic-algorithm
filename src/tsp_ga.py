import random
import json
import argparse
import os
from utils import distance, total_distance, save_route_plot

def create_population(size, num_cities):
    population = []
    base_route = list(range(num_cities))

    for _ in range(size):
        route = base_route[:]
        random.shuffle(route)
        population.append(route)

    return population

def selection(population, cities, k=3):
    candidates = random.sample(population, k)
    candidates.sort(key=lambda route: total_distance(route, cities))
    return candidates[0]

def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)

    # Copy a slice
    child[start:end] = parent1[start:end]

    # Fill remaining from parent2
    ptr = 0
    for gene in parent2:
        if gene not in child:
            while child[ptr] is not None:
                ptr += 1
            child[ptr] = gene

    return child

def mutate(route, mutation_rate=0.02):
    for i in range(len(route)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(route) - 1)
            route[i], route[j] = route[j], route[i]
    return route

def load_cities(path):
    with open(path, "r") as f:
        data = json.load(f)
    return {int(k): tuple(v) for k, v in data.items()}

def save_results(route, dist, cities, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    # Save best route data
    with open(os.path.join(output_dir, "best_route.txt"), "w") as f:
        f.write(f"Total Distance: {dist}\n")
        f.write("Route: " + ",".join(map(str, route)))

    # Save plot
    save_route_plot(route, cities, os.path.join(output_dir, "route_plot.png"))

    print(f"\n▶ Results saved in folder: {output_dir}")

def genetic_algorithm(cities, population_size=150, generations=800, mutation_rate=0.02, k=5):
    population = create_population(population_size, len(cities))

    best_route = None
    best_distance = float("inf")

    for gen in range(generations):
        new_population = []

        for _ in range(population_size):
            parent1 = selection(population, cities, k)
            parent2 = selection(population, cities, k)
            child = crossover(parent1, parent2)
            child = mutate(child, mutation_rate)
            new_population.append(child)

        population = new_population

        for route in population:
            dist = total_distance(route, cities)
            if dist < best_distance:
                best_route = route
                best_distance = dist

        if gen % 50 == 0:
            print(f"Generation {gen} → Best Distance: {best_distance:.2f}")

    return best_route, best_distance

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cities", type=str, default="data/sample_cities.json")
    parser.add_argument("--pop", type=int, default=150)
    parser.add_argument("--gen", type=int, default=800)
    parser.add_argument("--mut", type=float, default=0.02)
    parser.add_argument("--k", type=int, default=5)

    args = parser.parse_args()

    cities = load_cities(args.cities)
    print(f"Loaded {len(cities)} cities.")

    route, best_dist = genetic_algorithm(
        cities,
        population_size=args.pop,
        generations=args.gen,
        mutation_rate=args.mut,
        k=args.k
    )

    print("\nFinal Best Route:", route)
    print("Final Distance:", best_dist)

    save_results(route, best_dist, cities)
