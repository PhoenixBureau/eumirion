from pprint import pformat
from eumi.main import read_pickle
from eumi.utilities.server import dependency_graph, extract_server_data


pickle_name = 'server.pyckle'
server = read_pickle(pickle_name)
server.debug = True
data = extract_server_data(server)
dep_graph = dependency_graph(data)

print pformat(data)
print '-' * 80
print pformat(dep_graph)
