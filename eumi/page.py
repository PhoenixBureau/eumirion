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
from os.path import exists, join
from os import makedirs
from joy.utils.stack import strstack
from .html import posting, all_pages_pre, all_pages_post
from .page_actions import (
  get_page_data,
  linkerate,
  link_finder,
  match_dict,
  render_body,
  )
from .utilities.joy_wrapper import JOY


DEFAULT_TITLE = 'No Title'
DEFAULT_TEXT = 'You can use the editor below to write some text...'
DEFAULT_DATA = {
  'title': '',
  'text': '',
  }
FIELDS = tuple(sorted(DEFAULT_DATA))


class Page(object):

  def __init__(self, router, environ, page_data, head, body):
    '''
    router: the dict mapping paths to page handlers.
    page_data: the current instance data for this page.

    Fill in the head and body and return the page's (possibly new) page_data.
    '''
    if page_data is None:
      page_data = DEFAULT_DATA.copy()
    update_page_data(page_data, environ, router)
    self.link = linkerate(*environ['path'])
    self.title = page_data['title']
    self.text = page_data['text']
    self.router = router
    self.data = page_data
    self.environ = environ
    self.head = head
    self.body = body

  def __call__(self):
    all_pages_pre(self.head, self.body, self.title, self.link, DEFAULT_TITLE)
    render_body(self.body.div, self, DEFAULT_TEXT)
    if 'NO-EDIT' not in self.environ:
      all_pages_post(self.body, self.title, self.text, self.link, DEFAULT_TEXT)
    return self.data

  def update_files(self, base_dir):
    location = join(base_dir, self.link.lstrip('/'))
    if not exists(location):
      makedirs(location)
    write_file(join(location, 'title'), self.data['title'])
    write_file(join(location, 'text'), self.data['text'])
    try:
      expression = self.data['joy']
    except KeyError:
      return
    joy = strstack(expression)
    write_file(join(location, 'joy'), joy)


def write_file(fn, output):
  print 'writing', fn
  with open(fn, 'w') as f:
    f.write(output)


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
  expression = expression_of(command, router)
  stack = page_data.get('joy', ())
  result = JOY(expression, stack)
  print 'running', strstack(expression)
  print 'on', strstack(stack)
  print 'result', strstack(result)
  page_data['joy'] = result


def get_form_data(environ):
  environ['QUERY_STRING'] = ''
  return FieldStorage(
    fp=environ['wsgi.input'],
    environ=environ,
    keep_blank_values=True,
    )


def expression_of(command, router):
  kind, unit = kind_and_unit_from_command(command)
  command_data = get_page_data(router, kind, unit)
  if command_data is None:
    raise ValueError('No page for: %r' % (command,))
  try:
    return command_data['joy']
  except KeyError:
    raise ValueError('No available expression for: %r' % (command,))


def kind_and_unit_from_command(command):
  match = link_finder.match(command)
  if match is None:
    raise ValueError('The command arg is messed up: %r' % (command,))
  _, kind, unit = match_dict(match)
  return kind, unit
