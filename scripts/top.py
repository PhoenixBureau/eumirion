# Script to convert pickle to files...
from pprint import pformat
from eumi.main import read_pickle
from eumi.utilities.server import extract_server_data, out_to_files


pickle_name = 'server.pyckle'
server = read_pickle(pickle_name)
data = extract_server_data(server)
out_to_files(data, './server')
