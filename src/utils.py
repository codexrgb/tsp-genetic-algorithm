import math
import matplotlib.pyplot as plt

def distance(point1, point2):
    return math.hypot(point1[0] - point2[0], point1[1] - point2[1])

def total_distance(route, cities):
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i+1) % len(route)]])
    return dist

def save_route_plot(route, cities, filename):
    xs = [cities[i][0] for i in route] + [cities[route[0]][0]]
    ys = [cities[i][1] for i in route] + [cities[route[0]][1]]

    plt.figure(figsize=(8,6))
    plt.plot(xs, ys, marker='o')

    # Add city labels
    for idx in route:
        plt.text(cities[idx][0], cities[idx][1], str(idx))

    plt.title("TSP Best Route")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
