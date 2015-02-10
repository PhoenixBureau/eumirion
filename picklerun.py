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
from sys import argv as ARGV, stderr
from os.path import exists, realpath
from pickle import dump, load
from wsgiref.simple_server import make_server
from eumi.argparser import make_argparser
from eumi.main import EumiServer, pather, run
from eumi.page import page


class CannotFindPickle(ValueError):
  pass


def real(fn):
  realfn = realpath(fn)
  if not exists(realfn):
    raise CannotFindPickle(realfn)
  return realfn


def read_pickle(fn):
  with open(real(fn), 'r') as pickle_file:
    server = load(pickle_file)
  return server


def save_pickle(fn, server):
  with open(realpath(fn), 'w') as pickle_file:
    dump(server, pickle_file)
    pickle_file.flush()


def main(argv=None):
  if argv is None:
    argv = ARGV
    if argv[0] == 'picklerun.py':
      del argv[0]

  cli_args = make_argparser().parse_args(argv)

  print "eumi serving at http://%s:%i/00000000/00000000" % (
    cli_args.host or 'localhost',
    cli_args.port,
    )

  if cli_args.pickle is None:
    print 'Running without saving pickles.'
    server = EumiServer(pather, page)
    run(server, cli_args.host, cli_args.port)
    return

  try:
    server = read_pickle(cli_args.pickle)
  except CannotFindPickle:
    print >> stderr, 'Using new pickle file ', cli_args.pickle
    server = EumiServer(pather, page)
    save_pickle(cli_args.pickle, server)

  httpd = make_server(cli_args.host, cli_args.port, server)
  quit_loop = False
  while not quit_loop:
    try:
      httpd.handle_request()
    except KeyboardInterrupt:
      quit_loop = True
    else:
      save_pickle(cli_args.pickle, server)


if __name__ == '__main__':
  main()
