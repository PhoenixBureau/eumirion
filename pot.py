from pprint import pformat
from StringIO import StringIO
from wsgiref.simple_server import make_server
from eumi.utilities.loader import load
from eumi.joy import initializer
from eumi.server import EumiServer, PageHandler, pather
from eumi.page import Page


server = EumiServer(pather, Page)
for path, data in load():
 # print path, pformat(data)
  env = {
    'wsgi.input': StringIO(),
    'REQUEST_METHOD': 'POST',
    'path': path,
    }
  server.router[path] = pageh = PageHandler(server, data)
 # print '-' * 80

print server
httpd = make_server('', 8000, server)
httpd.serve_forever()
