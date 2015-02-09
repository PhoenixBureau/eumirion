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
from html import HTML


class Fun(dict):

  def __init__(self, page, *a, **b):
    self.page = page
    dict.__init__(self, *a, **b)

  def default_handler(self, environ):
    path = environ['path']
    handler = self[path] = PageHandler(environ, self.make_page)
    return handler(environ)

  def make_page(self, environ, page_data, head, body):
    return self.page(self, environ, page_data, head, body)


class PageHandler(object):

  def __init__(self, environ, make_page, data=None):
    self.data = data
    self.make_page = make_page
    self.post(environ, make_page)

  def __call__(self, environ):
    if environ['REQUEST_METHOD'] == 'POST':
      self.post(environ, self.make_page)
    return self.response

  def post(self, environ, make_page):
    doc = HTML()
    self.data = make_page(environ, self.data, doc.head, doc.body)
    self.response = str(doc)


class MalformedURL(Exception): pass


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
