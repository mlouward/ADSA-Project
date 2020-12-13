import numpy as np
from itertools import permutations
from ortools.constraint_solver import pywrapcp, routing_enums_pb2


INF = float('inf')

def floyd_warshall(graph):
    '''
    The graph is undirected and weighted (symmetric adjacency matrix)
    '''
    v = len(graph)
    # path reconstruction matrix
    p = np.zeros((v, v))
    for i in range(v):
        for j in range(v):
            p[i, j] = graph[i, j]

    for k in range(v):
        for j in range(v):
            for i in range(j):
                p[i, j] = min(p[i, j], p[i, k] + p[k, j])
                p[j, i] = p[i, j]

    return p

def load_graph(path, for_crewmates=True):
    edges = []
    with open(path, 'r') as f:
        for line in f:
            # Stop at empty line for crewmate map
            if not line.strip():
                if for_crewmates:
                    break
                else:
                    continue
            edges.append(list(map(int, line.strip().split())))

    # find max index of vertices in the graph = nb of vertices
    nb_vertices = np.max([[i[0] for i in edges] + [i[1] for i in edges]])

    # Initialize all values to INF
    matrix = [[INF for _ in range(nb_vertices)] for _ in range(nb_vertices)]
    # Set diagonal as 0
    for i in range(nb_vertices):
        matrix[i][i] = 0

    # Set weights in matrix
    for edge in edges:
        matrix[edge[0] - 1][edge[1] - 1] = edge[2]
        matrix[edge[1] - 1][edge[0] - 1] = edge[2]
    return np.array(matrix)

def create_data_model(graph):
    """Stores the data for the problem."""
    data = {}
    data['distance_matrix'] = floyd_warshall(graph)
    data['num_vehicles'] = 1
    data['depot'] = 0
    return data

def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return data['distance_matrix'][from_node][to_node]

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index) + 1)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(manager.IndexToNode(index) + 1)
    plan_output += 'Route distance: {}miles\n'.format(route_distance)
    print(plan_output)

if __name__ == "__main__":
    graph = load_graph(f"graph_all.txt")
    data = create_data_model(graph)
    manager = pywrapcp.RoutingIndexManager(
        len(data['distance_matrix']), data['num_vehicles'],
        data['depot'])
    routing = pywrapcp.RoutingModel(manager)
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        print_solution(manager, routing, solution)