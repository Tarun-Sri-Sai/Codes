import random
import sys
import time


sys.setrecursionlimit(int(1e8))


INF = int(1e9)


class Graph:
    def __init__(self, adjacency_list, heuristics):
        self.adjacency_list = adjacency_list
        self.heuristics = heuristics
        self.dls_path = []
        self.a_star_path = []
        self.a_star_count = 0
        self.dls_count = 0

    def get_neighbors(self, v):
        return self.adjacency_list[v]

    def get_heuristic(self, n):
        return self.heuristics[n]

    def a_star_algorithm(self, start_node, stop_node):
        open_list = set([start_node])
        closed_list = set([])
        g = {}
        g[start_node] = 0
        parents = {}
        parents[start_node] = start_node
        while len(open_list) > 0:
            n = None
            for v in open_list:
                if n == None or g[v] + self.get_heuristic(v) < g[n] + self.get_heuristic(n):
                    n = v

            if n == None:
                print("Path not found using A-star search!")
                return

            if n == stop_node:
                while parents[n] != n:
                    self.a_star_path.append(n)
                    n = parents[n]
                self.a_star_path.append(start_node)
                self.a_star_path.reverse()
                print(
                    f"Path found using A-star search!\t\t{self.a_star_path}")
                return

            for m, weight in self.get_neighbors(n).items():
                self.a_star_count += 1
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n
                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            open_list.remove(n)
            closed_list.add(n)
        print("Path not found using A-star search!")

    def depth_limited_search(self, start_vertex, target_vertex, depth_limit):
        self.dls_path.append(start_vertex)
        if self.dls(start_vertex, target_vertex, depth_limit):
            print(f"Path found using Depth Limited search!\t{self.dls_path}")
        else:
            print("Path not found using Depth Limited search!")

    def dls(self, current_vertex, target_vertex, depth_limit):
        if current_vertex == target_vertex:
            return True

        if depth_limit == 0:
            return False

        for neighbor, _ in self.get_neighbors(current_vertex).items():
            self.dls_count += 1
            self.dls_path.append(neighbor)
            if self.dls(neighbor, target_vertex, depth_limit - 1):
                return True

            self.dls_path.pop()

        return False


def get_adjacency_list():
    n_vertices = int(input("Enter number of vertices: "))
    if n_vertices > 26:
        return

    vertices = [chr(i + 65) for i in range(n_vertices)]
    print(f"Vertices: {vertices}\n")

    adjacency_list = {}

    print("How do you want your graph:\n\t1. Randomly generated\n\t2. Custom input")
    choice = int(input("\nEnter your Choice: "))

    if choice == 1:
        for vertex in vertices:
            adjacency_list[vertex] = {}

            for _ in range(random.randint(0, n_vertices - 1)):
                curr_vertex = vertices[random.randint(0, n_vertices - 1)]

                while curr_vertex == vertex:
                    curr_vertex = vertices[random.randint(0, n_vertices - 1)]

                adjacency_list[vertex][curr_vertex] = random.randint(1, 100)

    else:
        print("\nEnter the adjacency list", end=" ")
        print("format: \"vertex_name,weight\" pairs separated by space, \"None\" for empty list):")

        for vertex in vertices:
            line = input(f"For {vertex}: ")

            adjacency_list[vertex] = {}

            if line != "None":
                pairs = line.split()

                for pair in pairs:
                    comma_sep_fields = pair.split(sep=",")
                    adjacency_list[vertex][comma_sep_fields[0]] = int(comma_sep_fields[1])

    print("\nGraph:")
    for vertex in vertices: 
        print(f"{vertex}:", f"{adjacency_list[vertex]}" if adjacency_list[vertex] else "None")

    print()

    return adjacency_list


def find_dist(adjacency_list, start, end):
    queue = [start]
    visited = set(start)
    dist = 0
    
    while queue:
        size = len(queue)

        for _ in range(size):
            node = queue.pop(0)
            if node == end:
                return dist
            
            for neighbor in adjacency_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        dist += 1

    return INF


def find_heuristic(adjacency_list, start, end):
    return find_dist(adjacency_list, start, end)


def get_heuristics(adjacency_list, end_vertex):
    print("\nHow do you want your heuristics:\n\t1. Calculated\n\t2. Custom input")
    choice = int(input("\nEnter your Choice: "))

    vertices = [key for key in adjacency_list]

    heuristics = {}

    if choice == 1:
        for vertex in vertices:
            if vertex == end_vertex:
                heuristics[vertex] = INF
            else:    
                heuristics[vertex] = find_heuristic(adjacency_list, vertex, end_vertex)

    else:
        for vertex in vertices:
            heuristics[vertex] = int(input(f"Enter heuristic for {vertex}: "))

    print("\nHeuristics:\t", end="")
    for i, vertex in enumerate(vertices):
        print(f"({vertex}: {heuristics[vertex]})", 
            ", " if (i + 1) % 6 != 0 and i < len(vertices) - 1 else "\n\t\t", sep="", end="")
        
    return heuristics


def main():
    adjacency_list = get_adjacency_list()

    start = input("Enter starting node: ")
    end = input("Enter destination node: ")
    depth = int(input("Enter depth for depth limited search: "))

    heuristics = get_heuristics(adjacency_list, end)

    graph = Graph(adjacency_list, heuristics)

    print()

    start_time = time.perf_counter() * 1e6
    graph.a_star_algorithm(start, end)
    end_time_a_star = time.perf_counter() * 1e6 - start_time

    start_time = time.perf_counter() * 1e6
    graph.depth_limited_search(start, end, depth)
    end_time_dls = time.perf_counter() * 1e6 - start_time

    print("\n", "=" * 30, " Algorithm Analysis ", "=" * 30, sep="")

    print(f"\nA-star search took\t\t\t\t{end_time_a_star:.2f} microseconds")
    print(f"Depth Limited search took\t\t\t{end_time_dls:.2f} microseconds")

    print("\n", "=" * 80, sep="")

    diff = end_time_dls - end_time_a_star
    if diff < 0:
        print(
            f"Depth Limited search was faster by\t\t{-diff:.2f} microseconds")
    elif diff > 0:
        print(f"A-star search was faster by\t\t\t{diff:.2f} microseconds")
    else:
        print("Both searches finished at the same time")

    print("=" * 80)

    print(f"\nA-star search visits\t\t\t\t{graph.a_star_count}")
    print(f"Depth Limited search visits\t\t\t{graph.dls_count}")

    print("\n", "=" * 80, sep="")

    diff = graph.a_star_count - graph.dls_count
    if diff < 0:
        print(f"A-star search beats Depth Limited search by\t{-diff} visits")
    else:
        print(f"Depth Limited search beats A-star search by\t{diff} visits")

    print("=" * 80)

    a_star_cost = sum(graph.adjacency_list[graph.a_star_path[i]][graph.a_star_path[i + 1]]
                      for i in range(len(graph.a_star_path) - 1))
    dls_cost = sum(graph.adjacency_list[graph.dls_path[i]][graph.dls_path[i + 1]]
                   for i in range(len(graph.dls_path) - 1))

    print(f"\nA-star search found a path that costs\t\t{a_star_cost}")
    print(f"Depth Limited search found a path that costs\t{dls_cost}")

    print("\n", "=" * 80, sep="")

    diff = a_star_cost - dls_cost
    if diff < 0:
        print(f"A-star search found a path cheaper by\t\t{-diff}")
    elif diff > 0:
        print(f"Depth Limited search found a path cheaper by\t{diff}")
    else:
        print(f"Both searches found the same path")

    print("=" * 80)


if __name__ == "__main__":
    main()
