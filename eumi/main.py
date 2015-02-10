#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2015 Simon Forman
#
#    This file is part of Eumirion.
#
#    Eumirion is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Eumirion is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Eumirion.  If not, see <http://www.gnu.org/licenses/>.
#
from traceback import format_exc
from wsgiref.simple_server import make_server
from .html import HTML, ok200, err500


class EumiServer(object):

  def __init__(self, pather, page_renderer):
    self.pather = pather
    self.router = {}
    self.page_renderer = page_renderer
    self.modified = False

  def handle_request(self, environ, start_response):
    environ['path'] = path = self.pather(environ)
    handler = self.router.get(path, self.default_handler)
    response = handler(environ)
    return ok200(start_response, response)

  def default_handler(self, environ):
    path = environ['path']
    self.router[path] = handler = PageHandler(self, environ)
    return handler(environ)

  def render(self, environ, page_data, head, body):
    return self.page_renderer(self.router, environ, page_data, head, body)

  def __call__(self, environ, start_response):
    try:
      return self.handle_request(environ, start_response)
    except MalformedURL, err:
      message = MalformedURL.__doc__ % err.args
      return err500(start_response, message)
    except:
      return err500(start_response, format_exc())


class PageHandler(object):

  def __init__(self, server, environ, data=None):
    self.server = server
    self.data = data
    self.post(environ)

  def __call__(self, environ):
    if environ['REQUEST_METHOD'] == 'POST':
      self.post(environ)
      self.server.modified = True
    return self.response

  def post(self, environ):
    doc = HTML()
    self.data = self.server.render(environ, self.data, doc.head, doc.body)
    self.response = str(doc)


class MalformedURL(Exception):
  '''This URL is no good: %r
It must be xxxxxxxx/xxxxxxxx
where the x's stand for any of
"0123456789abcdefABCDEF".'''


def pather(environ):
  '''
  Extract and return the path (location or coordinates) from a given
  request environ.  Raises MalformedURL if the URL is no good.
  '''
  path = environ['PATH_INFO'].strip('/')
  if len(path) != 17:  # nnnnnnnn/nnnnnnnn
    raise MalformedURL(path)

  head, slash, tail = path.partition('/')
  if not slash:
    raise MalformedURL(path)

  try:
    head = int(head, 16)
    tail = int(tail, 16)
  except (TypeError, ValueError):
    raise MalformedURL(path)

  return head, tail


def run(app, host='', port=8000):
  httpd = make_server(host, port, app)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass


def main(page):
  HOST, PORT = '', 8000
  print "Serving on port http://localhost:8000/ ..."
  app = EumiServer(pather, page)
  run(app=app, host=HOST, port=PORT)
