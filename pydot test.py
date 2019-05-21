import pydot as pd
graph = pd.Dot(graph_type="graph")
for i in range(3):
    edge = pd.Edge("king", "lord%d" % i)
    graph.add_edge(edge)

for i in range(5):
  edge = pd.Edge("root",str(i))
  graph.add_edge(edge)

graph.write_png('example1_graph.png')
