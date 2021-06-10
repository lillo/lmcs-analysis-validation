from collections import defaultdict
import sys


class Graph():
    def __init__(self):
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append(to_node)
        self.weights[(from_node, to_node)] = weight

    def nodes(self):
        return list(self.edges.keys())

    def predecessors(self, node):
        return [u for u, l in self.edges.items() if node in l]


def transaction_cost(file):
    costs = {}
    with open(file) as f:
        for line in f.readlines():
            line = line.split(',')
            costs[int(line[0])] = float(line[2])
    return costs


def load_graph(file, costs):
    g = Graph()
    with open(file) as f:
        for line in f.readlines():
            line = line.split(" => ")
            from_node = int(line[0])
            dest_node = int(line[1])
            g.add_edge(from_node, dest_node, costs[dest_node])
    return g


def dfs(graph, n, visited, stack):
    visited.add(n)

    for successor in graph.edges[n]:
        if not successor in visited:
            dfs(graph, successor, visited, stack)

    stack.append(n)


def topological_sort(graph):
    visited = set()
    stack = []

    for n in graph.nodes():
        if not n in visited:
            dfs(graph, n, visited, stack)

    return stack[::-1]


def longest_path(graph):
    dist = defaultdict(lambda: 0)

    for node in topological_sort(graph):
        pred = graph.predecessors(node)
        if not(pred == []):
            dist[node] = max([dist[u] + graph.weights[u, node] for u in pred])

    max_dist = max(dist.values())
    inv_dist = {v: k for k, v in dist.items()}
    path = [inv_dist[max_dist]]
    stack = [inv_dist[max_dist]]

    while len(stack) > 0:
        node = stack.pop()
        pred = graph.predecessors(node)
        if pred != []:
            mpred = inv_dist[max(dist[u] for u in pred)]
            path.append(mpred)
            stack.insert(0, mpred)

    return (path[::-1], max_dist)


def main():
    if len(sys.argv) != 3:
        sys.stderr.write("Usage:\n python %s graph_file costs_file\n" % sys.argv[0])
        exit(-1)
    else:
        graph_file = sys.argv[1]
        costs_file = sys.argv[2]

        costs = transaction_cost(costs_file)
        graph = load_graph(graph_file, costs)
        print(longest_path(graph))


if __name__ == "__main__":
    main()