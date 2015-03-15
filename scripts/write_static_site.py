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
from os import makedirs
from os.path import join
from StringIO import StringIO
from eumi.main import load_server
from eumi.page_actions import linkerate


base_dir = '../server'
out_dir = './static'
env = {
  'REQUEST_METHOD': 'POST',
  'wsgi.input': StringIO(),
  }
server = load_server(base_dir)
server.base_dir = None  # Don't modify files in base_dir.
for (kind, unit), page_handler in server.router.iteritems():
  loc = join(out_dir, linkerate(kind, unit).lstrip('/'))
  makedirs(loc)
  fn = join(loc, 'index.html')
  e = env.copy()
  e['path'] = kind, unit
  with open(fn, 'w') as index_html:
    index_html.write(page_handler(e))
  print 'wrote', fn
