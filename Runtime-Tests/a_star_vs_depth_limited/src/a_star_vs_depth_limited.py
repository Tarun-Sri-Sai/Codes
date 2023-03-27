import random
import sys
import time
import os


sys.setrecursionlimit(int(1e8))


INF = int(1e9)
ONE_HUNDREDTH_SEC = 0.01
ONE_FIFTH_SEC = 0.2

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
                return False

            if n == stop_node:
                while parents[n] != n:
                    self.a_star_path.append(n)
                    n = parents[n]
                self.a_star_path.append(start_node)
                self.a_star_path.reverse()
                return True

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
        return False

    def depth_limited_search(self, start_vertex, target_vertex, depth_limit):
        self.dls_path.append(start_vertex)
        if self.dls(start_vertex, target_vertex, depth_limit):
            return True
        else:
            return False

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

                while curr_vertex == vertex or curr_vertex in adjacency_list[vertex]:
                    curr_vertex = vertices[random.randint(0, n_vertices - 1)]

                adjacency_list[vertex][curr_vertex] = random.randint(1, 99)

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
    time.sleep(ONE_HUNDREDTH_SEC)
    for vertex in vertices: 
        print(f"{vertex}: ", end="")
        if adjacency_list[vertex]:
            i_max = len(adjacency_list[vertex]) - 1

            print("{", end="")
            for i, (neighbor, weight) in enumerate(adjacency_list[vertex].items()):
                print(f"{neighbor}: {weight:3d}", end="")
                if i == i_max:
                    print("}")
                else:
                    print(", ", end="")
                    
                sys.stdout.flush()
        else:
            print("{}")

    print()

    return adjacency_list


def get_adjacency_list_from_file(file_in):
    print("Enter number of vertices: ", end="")
    sys.stdout.flush()
    n_vertices = int(file_in.readline().strip())

    if n_vertices > 26:
        return

    vertices = [chr(i + 65) for i in range(n_vertices)]
    print(f"Vertices: {vertices}\n")

    adjacency_list = {}

    print("How do you want your graph:\n\t1. Randomly generated\n\t2. Custom input")
    print("\nEnter your Choice: ", end="")
    sys.stdout.flush()
    choice = int(file_in.readline().strip())

    if choice == 1:
        for vertex in vertices:
            adjacency_list[vertex] = {}

            for _ in range(random.randint(0, n_vertices - 1)):
                curr_vertex = vertices[random.randint(0, n_vertices - 1)]

                while curr_vertex == vertex or curr_vertex in adjacency_list[vertex]:
                    curr_vertex = vertices[random.randint(0, n_vertices - 1)]

                adjacency_list[vertex][curr_vertex] = random.randint(1, 99)

    else:
        print("\nEnter the adjacency list", end=" ")
        print("format: \"vertex_name,weight\" pairs separated by space, \"None\" for empty list):")

        for vertex in vertices:
            print(f"For {vertex}: ", end="")
            sys.stdout.flush()
            line = file_in.readline().strip()

            adjacency_list[vertex] = {}

            if line != "None":
                pairs = line.split()

                for pair in pairs:
                    comma_sep_fields = pair.split(sep=",")
                    adjacency_list[vertex][comma_sep_fields[0]] = int(comma_sep_fields[1])

    print("\nGraph:")
    time.sleep(ONE_HUNDREDTH_SEC)
    for vertex in vertices: 
        print(f"{vertex}: ", end="")
        if adjacency_list[vertex]:
            i_max = len(adjacency_list[vertex]) - 1

            print("{", end="")
            for i, (neighbor, weight) in enumerate(adjacency_list[vertex].items()):
                print(f"{neighbor}: {weight:3d}", end="")
                if i == i_max:
                    print("}")
                else:
                    print(", ", end="")
                    
                sys.stdout.flush()
        else:
            print("{}")

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
    return find_dist(adjacency_list, start, end) * 10


def get_heuristics(adjacency_list, end_vertex):
    print("\nHow do you want your heuristics:\n\t1. Calculated\n\t2. Custom input")
    choice = int(input("\nEnter your Choice: "))

    vertices = [key for key in adjacency_list]

    heuristics = {}

    if choice == 1:
        for vertex in vertices:
            if vertex == end_vertex:
                heuristics[vertex] = 0
            else:    
                heuristics[vertex] = find_heuristic(adjacency_list, vertex, end_vertex)

    else:
        for vertex in vertices:
            heuristics[vertex] = int(input(f"Enter heuristic for {vertex}: "))

    print("\nHeuristics:\t", end="")
    time.sleep(ONE_FIFTH_SEC)
    for i, vertex in enumerate(vertices):
        print(f"({vertex}: ", f"{heuristics[vertex]:3d})" if heuristics[vertex] < INF else "INF)", sep="", end="")
        if (i + 1) % 7 != 0 and i < len(vertices) - 1:
            print(", ", end="")
        else:
            print("\n\t\t", end="")
        sys.stdout.flush()
        time.sleep(ONE_FIFTH_SEC)
        
    return heuristics


def get_heuristics_from_file(adjacency_list, end_vertex, file_in):
    print("\nHow do you want your heuristics:\n\t1. Calculated\n\t2. Custom input")
    print("\nEnter your Choice: ", end="")
    sys.stdout.flush()
    choice = int(file_in.readline().strip())

    vertices = [key for key in adjacency_list]

    heuristics = {}

    if choice == 1:
        for vertex in vertices:
            if vertex == end_vertex:
                heuristics[vertex] = 0
            else:    
                heuristics[vertex] = find_heuristic(adjacency_list, vertex, end_vertex)

    else:
        for vertex in vertices:
            print(f"Enter heuristic for {vertex}: ", end="")
            sys.stdout.flush()
            heuristics[vertex] = int(file_in.readline().strip())

    print("\nHeuristics:\t", end="")
    time.sleep(ONE_FIFTH_SEC)
    for i, vertex in enumerate(vertices):
        print(f"({vertex}: ", f"{heuristics[vertex]:3d})" if heuristics[vertex] < INF else "INF)", sep="", end="")
        if (i + 1) % 7 != 0 and i < len(vertices) - 1:
            print(", ", end="")
        else:
            print("\n\t\t", end="")
        sys.stdout.flush()
        time.sleep(ONE_FIFTH_SEC)
        
    return heuristics


def main():
    print("How do you want your input:\n\t1. Stdin\n\t2. File path")
    choice = int(input("\nEnter your choice: "))
    if choice == 1:
        adjacency_list = get_adjacency_list()

        start = input("Enter starting node: ")
        end = input("Enter destination node: ")
        depth = int(input("Enter depth for depth limited search: "))

        heuristics = get_heuristics(adjacency_list, end)
    
    else:
        print("\n", os.getcwd(), sep="")
        with open(input("\nEnter file path: "), "r") as file_in:
            adjacency_list = get_adjacency_list_from_file(file_in)

            print("Enter starting node: ", end="")
            sys.stdout.flush()
            start = file_in.readline().strip()
            print("Enter destination node: ", end="")
            sys.stdout.flush()
            end = file_in.readline().strip()
            print("Enter depth for depth limited search: ", end="")
            sys.stdout.flush()
            depth = int(file_in.readline().strip())

            heuristics = get_heuristics_from_file(adjacency_list, end, file_in)

    graph = Graph(adjacency_list, heuristics)

    print()

    start_time = time.perf_counter() * 1e6
    a_star_success = graph.a_star_algorithm(start, end)
    end_time_a_star = time.perf_counter() * 1e6 - start_time

    if a_star_success:
        i_max = len(graph.a_star_path) - 1

        print("Path found using A-star search!\t\t", end="")
        sys.stdout.flush()
        for i, vertex in enumerate(graph.a_star_path):
            print(vertex, sep="", end="")
            if i == i_max:
                print("\n")
            else:
                print(" -> ", end="")
            sys.stdout.flush()
            time.sleep(ONE_FIFTH_SEC)
    else:
        print("Path not found using A-star search!")

    start_time = time.perf_counter() * 1e6
    dls_success = graph.depth_limited_search(start, end, depth)
    end_time_dls = time.perf_counter() * 1e6 - start_time

    if dls_success:
        i_max = len(graph.dls_path) - 1

        print("Path found using Depth Limited search!\t", end="")
        sys.stdout.flush()
        for i, vertex in enumerate(graph.dls_path):
            print(vertex, sep="", end="")
            if i == i_max:
                print("\n")
            else:
                print(" -> ", end="")
            sys.stdout.flush()
            time.sleep(ONE_FIFTH_SEC)
    else:
        print("Path not found using Depth Limited search!")

    print("\n", "=" * 30, " Algorithm Analysis ", "=" * 30, sep="")
    time.sleep(ONE_FIFTH_SEC)

    print(f"\nA-star search took\t\t\t\t{end_time_a_star:3.2f} microseconds")
    time.sleep(ONE_FIFTH_SEC)
    print(f"Depth Limited search took\t\t\t{end_time_dls:3.2f} microseconds")
    time.sleep(ONE_FIFTH_SEC)

    print("\n", "=" * 80, sep="")
    time.sleep(ONE_FIFTH_SEC)

    diff = end_time_dls - end_time_a_star
    if diff < 0:
        print(
            f"Depth Limited search was faster by\t\t{-diff:3.2f} microseconds")
        time.sleep(ONE_FIFTH_SEC)
    elif diff > 0:
        print(f"A-star search was faster by\t\t\t{diff:3.2f} microseconds")
        time.sleep(ONE_FIFTH_SEC)
    else:
        print("Both searches finished at the same time")
        time.sleep(ONE_FIFTH_SEC)

    print("=" * 80)
    time.sleep(ONE_FIFTH_SEC)

    print(f"\nA-star search visits\t\t\t\t{graph.a_star_count}")
    time.sleep(ONE_FIFTH_SEC)
    print(f"Depth Limited search visits\t\t\t{graph.dls_count}")
    time.sleep(ONE_FIFTH_SEC)

    print("\n", "=" * 80, sep="")
    time.sleep(ONE_FIFTH_SEC)

    diff = graph.a_star_count - graph.dls_count
    if diff < 0:
        print(f"A-star search beats Depth Limited search by\t{-diff} visits")
        time.sleep(ONE_FIFTH_SEC)
    else:
        print(f"Depth Limited search beats A-star search by\t{diff} visits")
        time.sleep(ONE_FIFTH_SEC)

    print("=" * 80)
    time.sleep(ONE_FIFTH_SEC)

    a_star_cost = sum(graph.adjacency_list[graph.a_star_path[i]][graph.a_star_path[i + 1]]
                      for i in range(len(graph.a_star_path) - 1))
    dls_cost = sum(graph.adjacency_list[graph.dls_path[i]][graph.dls_path[i + 1]]
                   for i in range(len(graph.dls_path) - 1))

    print(f"\nA-star search found a path that costs\t\t{a_star_cost}")
    time.sleep(ONE_FIFTH_SEC)
    print(f"Depth Limited search found a path that costs\t{dls_cost}")
    time.sleep(ONE_HUNDREDTH_SEC)

    print("\n", "=" * 80, sep="")
    time.sleep(ONE_FIFTH_SEC)

    diff = a_star_cost - dls_cost
    if diff < 0:
        print(f"A-star search found a path cheaper by\t\t{-diff}")
        time.sleep(ONE_FIFTH_SEC)
    elif diff > 0:
        print(f"Depth Limited search found a path cheaper by\t{diff}")
        time.sleep(ONE_FIFTH_SEC)
    else:
        print(f"Both searches found the same path")
        time.sleep(ONE_FIFTH_SEC)

    print("=" * 80)
    time.sleep(ONE_FIFTH_SEC)


if __name__ == "__main__":
    main()
