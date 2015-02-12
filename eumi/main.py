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
from os.path import exists, realpath
from pickle import dump, load
from traceback import format_exc
from wsgiref.simple_server import make_server
from .argparser import make_argparser
from .html import HTML, ok200, err500, posting
from .page import page
from .joy import initializer


class EumiServer(object):

  def __init__(self, pather, page_renderer):
    self.pather = pather
    self.router = {}
    self.page_renderer = page_renderer
    self.modified = False
    self.debug = False

  def handle_request(self, environ, start_response):
    environ['path'] = path = self.pather(environ['PATH_INFO'])
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
    if self.debug:
      return self.handle_request(environ, start_response)
    try:
      return self.handle_request(environ, start_response)
    except MalformedURL, err:
      message = MalformedURL.__doc__ % (environ['PATH_INFO'], err.args[0])
      return err500(start_response, message)
    except:
      return err500(start_response, format_exc())


class PageHandler(object):

  def __init__(self, server, environ, data=None):
    self.server = server
    self.data = data
    self.post(environ)

  def __call__(self, environ):
    if posting(environ):
      self.post(environ)
      self.server.modified = True
    return self.response

  def post(self, environ):
    doc = HTML()
    self.data = self.server.render(environ, self.data, doc.head, doc.body)
    self.response = str(doc)


class MalformedURL(Exception):
  '''This URL is no good: %r
Reason: %s
It must be /nnnnnnnn/nnnnnnnn
where the n's stand for any of
"0123456789abcdefABCDEF".'''


def pather(path_info):
  '''
  Extract and return the path (location or coordinates) from a given
  request PATH_INFO.  Raises MalformedURL if the URL is no good.
  The expected pattern is '/nnnnnnnn/nnnnnnnn' where the n's are
  hexidecimal digits.
  '''
  path = path_info.strip('/')
  n = len(path)
  if n < 17:
    raise MalformedURL('Too short (%i), not just right (17)!' % n)
  elif n > 17:
    raise MalformedURL('Too long (%i), not just right (17)!' % n)

  kind, slash, unit = path.partition('/')
  if not slash:
    raise MalformedURL('There should be a slash in it.')

  try:
    kind = int(kind, 16)
    unit = int(unit, 16)
  except (TypeError, ValueError):
    raise MalformedURL('The chars can only be one of'
                       ' abcdef or ABCDEF or 0123456789.')
  return kind, unit


def main(argv=None):
  if argv is None:
    import sys
    argv = sys.argv[1:]
  args = make_argparser().parse_args(argv)

#  initialize()  # Joy.

  pickle_name = realpath(args.pickle)
  if exists(pickle_name):
    print 'Loading server from pickle file:', pickle_name
    server = read_pickle(pickle_name)
  else:
    print 'Loading new blank server.'
    server = EumiServer(pather, page)

  if not hasattr(server, 'debug'):
    server.debug = False

  if args.crazy_town:
    print 'Running without saving pickles.'
    _print_serving(args.host, args.port)
    run(server, args.host, args.port)
    return

  if not exists(pickle_name):
    print 'Using new pickle file:', pickle_name
    save_pickle(pickle_name, server)

  httpd = make_server(args.host, args.port, server)
  _print_serving(args.host, args.port)
  quit_loop = False
  while not quit_loop:
    try:
      httpd.handle_request()
    except KeyboardInterrupt:
      quit_loop = True
    else:
      modified, server.modified = server.modified, False
      if modified:
        save_pickle(pickle_name, server)


def run(app, host='', port=8000):
  httpd = make_server(host, port, app)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass


def read_pickle(fn):
  with open(fn, 'r') as pickle_file:
    server = load(pickle_file)
  return server


def save_pickle(fn, server):
  with open(fn, 'w') as pickle_file:
    dump(server, pickle_file)
    pickle_file.flush()


def _print_serving(host, port):
  print (
    'eumi at http://%s:%i/00000000/00000000'
    % (host or 'localhost', port)
    )
