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


def page(router, environ, page_data, head, body):
  '''
  router: the dict mapping paths to page handlers.
  environ: the WSGI environ.
  page_data: the current instance data for this page.
  head: the head HTML element.
  body: the body HTML element.

  Fill in the head and body and return the page's (possibly new) page_data.
  '''
  known_paths = sorted(router)
  location = environ['path']
  self_link = linkerate(*location)
  message = 'Current location: ' + self_link

  head.title(message)
  body.h1(message)

  with body.ol as ol:
    for known_path in known_paths:
      path_link(ol.li, *known_path)

  body.hr
  path_link(body, randrange(2**32), randrange(2**32))
  body.br
  body.hr

  with body.form(action=self_link, method='POST') as form:
    form.input(type_='hidden', name='hmm', value=str(randrange(2**32)))
    form.input(type_='submit', value='reload')

  return page_data


def hexify(i):
  s = hex(i)[2:]
  return '0' * (8 - len(s)) + s


def linkerate(head, tail):
  return '/%08s/%s' % (hexify(head), hexify(tail))


def path_link(home, head, tail):
  link = linkerate(head, tail)
  home.a(link, href=link)
