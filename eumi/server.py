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
from .html import HTML, ok200, err500, posting


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
    self.router[path] = handler = PageHandler(self)
    return handler(environ)

  def render(self, environ, page_data, head, body):
    page_renderer = self.page_renderer(self.router, environ, page_data, head, body)
    if posting(environ):
      page_renderer.update_files('./server')
    return page_renderer()

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

  def __init__(self, server, data=None):
    self.server = server
    self.data = data
    self.response = None

  def __call__(self, environ):
    if posting(environ) or not self.response:
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
