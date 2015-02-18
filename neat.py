from pprint import pformat
from eumi.main import read_pickle
from eumi.utilities import build_dependency_graph, print_server


pickle_name = 'server.pyckle'
server = read_pickle(pickle_name)
server.debug = True
data = print_server(server)
dep_graph = build_dependency_graph(data)

print pformat(data)
print '-' * 80
print pformat(dep_graph)
