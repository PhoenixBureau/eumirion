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
from cgi import FieldStorage
from .html import posting, all_pages_pre, all_pages_post
from .joy.joy import joy
from .joy.parser import text_to_expression
from .joy.stack import iter_stack, stack_to_string
from .page_actions import (
  linkerate,
  render_body,
  link_finder,
  match_dict,
  get_page_data,
  )


DEFAULT_TITLE = 'No Title'
DEFAULT_TEXT = 'You can use the editor below to write some text...'
DEFAULT_DATA = {
  'title': '',
  'text': '',
  }
FIELDS = tuple(sorted(DEFAULT_DATA))


def page(router, environ, page_data, head, body):
  '''
  router: the dict mapping paths to page handlers.
  environ: the WSGI environ.
  page_data: the current instance data for this page.
  head: the head HTML element.
  body: the body HTML element.

  Fill in the head and body and return the page's (possibly new) page_data.
  '''
  if page_data is None:
    page_data = DEFAULT_DATA.copy()
  update_page_data(page_data, environ, router)

  self_link = linkerate(*environ['path'])
  title = page_data['title']
  text = page_data['text']

  all_pages_pre(head, body, title, self_link, DEFAULT_TEXT)
  render_body(head, body.div, text, router, self_link, DEFAULT_TEXT)
  all_pages_post(body, title, text, self_link, DEFAULT_TEXT)

  return page_data


def update_page_data(page_data, environ, router):
  form = get_form_data(environ)
  for field in FIELDS:
    value = form.getfirst(field)
    if value is not None:
      page_data[field] = value

  if posting(environ) and 'command' in form:
    command = form.getfirst('command')
    run_command(page_data, command, router)


def run_command(page_data, command, router):
  match = link_finder.match(command)
  if match is None:
    raise ValueError('The command arg is messed up: %r' % (command,))
  _, kind, unit = match_dict(match)
  command_data = get_page_data(router, kind, unit)
  if command_data is None:
    raise ValueError('No page for: %r' % (command,))
  try:
    expression = command_data['joy']
  except KeyError:
    raise ValueError('No available expression for: %r' % (command,))
  stack = page_data.get('stack', ())
  page_data['stack'] = joy(expression, stack)


def get_form_data(environ):
  environ['QUERY_STRING'] = ''
  return FieldStorage(
    fp=environ['wsgi.input'],
    environ=environ,
    keep_blank_values=True,
    )
