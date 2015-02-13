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
from pickle import dump, load
from wsgiref.simple_server import make_server
from .argparser import make_argparser
from .page import page
from .server import EumiServer, pather
from .joy import initializer  # FIXME these aren't the same as the ones in the pickle...


def main(argv=None):
  args = get_args(argv)
  pickle_name, server = get_server(args)
  if args.crazy_town:
    print 'Running without saving pickles.'
    run(server, args.host, args.port)
  else:
    if not exists(pickle_name):
      print 'Using new pickle file:', pickle_name
      save_pickle(pickle_name, server)
    go(args, pickle_name, server)


def get_args(argv=None):
  if argv is None:
    import sys
    argv = sys.argv[1:]
  return make_argparser().parse_args(argv)


def get_server(args):
  pickle_name = realpath(args.pickle)
  if exists(pickle_name):
    print 'Loading server from pickle file:', pickle_name
    server = read_pickle(pickle_name)
  else:
    print 'Loading new blank server.'
    server = EumiServer(pather, page)
  if not hasattr(server, 'debug'):
    server.debug = False
  return pickle_name, server


def go(args, pickle_name, server):
  httpd = make_server(args.host, args.port, server)
  _print_serving(args.host, args.port)
  while True:
    try:
      httpd.handle_request()
    except KeyboardInterrupt:
      break
    modified, server.modified = server.modified, False
    if modified:
      save_pickle(pickle_name, server)


def run(app, host='', port=8000):
  httpd = make_server(host, port, app)
  _print_serving(host, port)
  try:
    httpd.serve_forever()
  except KeyboardInterrupt:
    pass


def read_pickle(fn):
  with open(fn, 'r') as pickle_file:
    server = load(pickle_file)
  return server


def save_pickle(fn, server):
  tfn = fn + '.temp'
  success = False
  try:
    with open(tfn, 'w') as pickle_file:
      dump(server, pickle_file)
    success = True
  finally:
    if success:
      move(tfn, fn)


def move(from_, to):
  try:
    remove(to)
  except OSError:
    pass
  rename(from_, to)
  remove(from_)


def _print_serving(host, port):
  print (
    'eumi at http://%s:%i/00000000/00000000'
    % (host or 'localhost', port)
    )
