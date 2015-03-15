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
from os import remove, rename
from os.path import exists, realpath
from wsgiref.simple_server import make_server
from .argparser import make_argparser
from .page import Page
from .server import EumiServer, pather, PageHandler
from .joy import initializer
from .utilities.loader import load


def main(argv=None):
  args = get_args(argv)
  server = get_server(args)
  run(server, args.host, args.port)


def get_args(argv=None):
  if argv is None:
    import sys
    argv = sys.argv[1:]
  return make_argparser().parse_args(argv)


def get_server(args):
  base_dir = realpath(args.base_dir)
  print 'Loading server from:', base_dir
  server = load_server(base_dir)
  return server


def load_server(base_dir):
  server = EumiServer(pather, Page, base_dir)
  for path, data in load(base_dir):
    server.router[path] = PageHandler(server, data)
  return server


def run(app, host='', port=8000):
  httpd = make_server(host, port, app)
  _print_serving(host, port)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass


def _print_serving(host, port):
  print (
    'eumi at http://%s:%i/00000000/00000000'
    % (host or 'localhost', port)
    )
