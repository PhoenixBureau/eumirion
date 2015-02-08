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
from random import randrange
from .html import HTML


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


def hexify(i):
  s = hex(i)[2:]
  return '0' * (8 - len(s)) + s


def linkerate(head, tail):
  return '/%08s/%s' % (hexify(head), hexify(tail))


def path_link(home, head, tail):
  link = linkerate(head, tail)
  home.a(link, href=link)


class PageHandler(object):

  def __init__(self, environ, site_wide):
    document = HTML()
    site_wide(environ, document.head, document.body)
    self.response = str(document)

  def __call__(self, environ):
    return self.response


class Fun(dict):

  def default_handler(self, environ):
    path = environ['path']
    handler = self[path] = PageHandler(environ, self.site_wide)
    return handler(environ)

  def site_wide(self, environ, head, body):
    path = environ['path']
    message = 'Current location: ' + linkerate(*path)
    head.title(message)
    body.h1(message)
    with body.ol as ol:
      for known_path in sorted(self):
        path_link(ol.li, *known_path)
    path_link(body, randrange(2**32), randrange(2**32))
