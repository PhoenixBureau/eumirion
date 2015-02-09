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
from .html import HTML
from .page import page


def make_app(pather, router, default_handler):
  @report_problems
  def app(environ, start_response):
    path = environ['path'] = pather(environ)
    handler = router.get(path, default_handler)
    response = handler(environ)
    return ok200(start_response, response)
  return app


class Router(dict):

  def __init__(self, page, *a, **b):
    self.page = page
    dict.__init__(self, *a, **b)

  def default_handler(self, environ):
    path = environ['path']
    handler = self[path] = PageHandler(environ, self)
    return handler(environ)


class PageHandler(object):

  def __init__(self, environ, router, data=None):
    self.data = data
    self.router = router
    self.post(environ)

  def __call__(self, environ):
    if environ['REQUEST_METHOD'] == 'POST':
      self.post(environ)
    return self.response

  def post(self, environ):
    doc = HTML()
    self.data = self.router.page(
      self.router,
      environ,
      self.data,
      doc.head,
      doc.body,
      )
    self.response = str(doc)


class MalformedURL(Exception):
  '''This URL is no good: %r
It must be xxxxxxxx/xxxxxxxx
where the x's stand for any of
"0123456789abcdefABCDEF".'''


def pather(environ):
  path = environ['PATH_INFO'].strip('/')
  if len(path) != 17:  # nnnnnnnn/nnnnnnnn
    raise MalformedURL(path)
  head, slash, tail = path.partition('/')
  if not slash:
    raise MalformedURL(path)
  try:
    head = int(head, 16)
    tail = int(tail, 16)
  except:
    raise MalformedURL(path)
  return head, tail


def start(start_response, message, mime_type):
  start_response(message, [('Content-type', mime_type)])


def err500(start_response, message):
  start(start_response, '500 Internal Server Error', 'text/plain')
  return [str(message)]


def ok200(start_response, response):
  start(start_response, '200 OK', 'text/html')
  return response


def report_problems(f):
  def inner(environ, start_response):
    try:
      return f(environ, start_response)
    except MalformedURL, err:
      message = MalformedURL.__doc__ % err.args
      return err500(start_response, message)
    except:
      return err500(start_response, format_exc())
  return inner


def run(app, host='', port=8000):
  httpd = make_server(host, port, app)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass


def main():
  HOST, PORT = '', 8000
  print "Serving on port http://localhost:8000/ ..."
  router = Router(page=page)
  app = make_app(pather, router, router.default_handler)
  run(app=app, host=HOST, port=PORT)
