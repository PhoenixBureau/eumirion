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


def make_app(pather, router, default_handler):
  @report_problems
  def app(environ, start_response):
    path = environ['path'] = pather(environ)
    handler = router.get(path, default_handler)
    response = handler(environ)
    return ok200(start_response, response)
  return app


def pather(environ):
  return tuple(environ['PATH_INFO'].strip('/').split('/'))


router = {('',): lambda environ: 'root'}


def default_handler(environ):
  message = 'No resource at ' + str(environ['path'])
  document = HTML()
  document.head.title(message)
  document.body(message)
  return document


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
    except:
      return err500(start_response, format_exc())
  return inner


def run(app, host='', port=8000):
  httpd = make_server(host, port, app)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass


if __name__ == '__main__':
  print "Serving on port http://localhost:8000/ ..."
  run(make_app(pather, router, default_handler))
