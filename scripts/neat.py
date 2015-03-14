from pprint import pformat
from eumi.utilities.server import dependency_graph, extract_server_data


server = # 
server.debug = True
data = extract_server_data(server)
dep_graph = dependency_graph(data)

print pformat(data)
print '-' * 80
print pformat(dep_graph)
