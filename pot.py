from wsgiref.simple_server import make_server
from eumi.utilities.loader import load
from eumi.joy import initializer
from eumi.server import EumiServer, PageHandler, pather
from eumi.page import Page


base_dir = '/home/sforman/Desktop/eumirion/server'


server = EumiServer(pather, Page)
for path, data in load(base_dir):
  server.router[path] = pageh = PageHandler(server, data)


httpd = make_server('', 8000, server)
httpd.serve_forever()
