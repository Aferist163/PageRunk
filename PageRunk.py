import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

#Dodawanie węzłów
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

#Dodajemy_krawędzie
edges = [
    ('A', 'B'), ('A', 'C'), ('B', 'D'), ('C', 'A'), ('D', 'E'),
    ('E', 'F'), ('F', 'C'), ('G', 'E'), ('H', 'G'), ('I', 'H'),
    ('J', 'I'), ('J', 'A'), ('H', 'B'), ('F', 'J'), ('F', 'A')
]

#Obliczamy_PageRank =======================================

#Budowa_grafu
graph = {node: [] for node in nodes}
for src, dst in edges:
    graph[src].append(dst)

incoming_links = {node: [] for node in nodes}
for src, dsts in graph.items():
    for dst in dsts:
        incoming_links[dst].append(src)

damping_factor = 0.85
num_iterations = 20
N = len(nodes)

pagerank = {node: 1 / N for node in nodes}

#Iteracje PageRank
for _ in range(num_iterations):
    new_pagerank = {}
    for node in nodes:
        rank_sum = 0
        for incoming in incoming_links[node]:
            rank_sum += pagerank[incoming] / len(graph[incoming])
        new_pagerank[node] = (1 - damping_factor) / N + damping_factor * rank_sum
    pagerank = new_pagerank


#wyniki
print('PageRank wartość po', num_iterations, "iteracjach:")
for node, rank in sorted(pagerank.items(), key=lambda item: item[1], reverse=True):
    print(f"{node}: {rank:.4f}")

#==================================================================================

#Budowa_grafu
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
pagerank = nx.pagerank(G, alpha=0.85)

# Node_Size, Node_Color
node_sizes = [pagerank[node] * 50000 for node in G.nodes()]
cmap = mcolors.LinearSegmentedColormap.from_list("custom_cmap", ["green", "yellow"])
pr_values = list(pagerank.values())
norm = mcolors.Normalize(vmin=min(pr_values), vmax=max(pr_values))
node_colors = [cmap(norm(pagerank[node])) for node in G.nodes()]

fig, (ax, ax2) = plt.subplots(1, 2, figsize=(18, 9))

#Draw_Graf
pos = nx.spring_layout(G, seed=46)
nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_colors, node_size=node_sizes, font_size=18, arrowsize=20)
label_pos = {node: (x, y + 0.08) for node, (x, y) in pos.items()}
labels = {node: f"{pagerank[node]:.2f}" for node in G.nodes()}
nx.draw_networkx_labels(G, label_pos, labels=labels, font_color='black', font_size=18, font_weight='bold', ax=ax)

#Data_Histogram
nodes_sorted = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
node_labels = [node for node, _ in nodes_sorted]
pagerank_values = [pr_value for _, pr_value in nodes_sorted]
node_colors_hist = [cmap(norm(pagerank[node])) for node in node_labels]

#Draw_Histogram
bars = ax2.barh(node_labels, pagerank_values, color=node_colors_hist)
for bar, pr_value in zip(bars, pagerank_values):
    ax2.text(pr_value - 0.025, bar.get_y() + bar.get_height() / 2,
             f"{pr_value:.4f}", va='center', ha='left', fontsize=18,  color='black')

plt.tight_layout()
plt.show()
