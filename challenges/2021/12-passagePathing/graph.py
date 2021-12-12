import networkx as nx
import matplotlib.pyplot as plt

edges = []
nodes = []
with open("input.txt") as f:
    for line in f.read().strip().splitlines():
        f, t = line.split("-")
        edges.append((f,t))
        for x in [f, t]:
            if x not in nodes:
                nodes.append(x)

graph = nx.Graph()
graph.add_edges_from(edges)
pos = nx.kamada_kawai_layout(graph)
nx.draw_networkx_nodes(graph, pos, nodelist=nodes)
nx.draw_networkx_labels(graph, pos)
nx.draw_networkx_edges(graph, pos, edgelist=graph.edges())
plt.show()