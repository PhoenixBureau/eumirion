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
from random import randrange
from .html import posting
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

  all_pages_pre(head, body, title, self_link)
  render_body(head, body.div, text, router, self_link, DEFAULT_TEXT)
  all_pages_post(body, title, text, self_link)

  return page_data


def update_page_data(page_data, environ, router):
  form = get_form_data(environ)
  for field in FIELDS:
    value = form.getfirst(field)
    if value is not None:
      page_data[field] = value

  check_for_joy(page_data)

  if posting(environ) and 'command' in form:
    command = form.getfirst('command')
    run_command(page_data, command, router)


def check_for_joy(page_data):
  text = page_data['text']
  if text.startswith('#!joy'):
    first_line = text.splitlines(False)[0][5:]
    expression = page_data['joy'] = text_to_expression(first_line)


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


def all_pages_pre(head, body, title, self_link):
  head.title(title or self_link)
  body.h1.a(title or DEFAULT_TITLE, href=self_link)


def all_pages_post(body, title, text, self_link):
  body.hr
  with body.form(action=self_link, method='POST') as form:
    form.h4('Edit')
    labeled_field(form, 'Title:', 'text', 'title', title,
      size='44', placeholder=DEFAULT_TITLE)
    form.br
    labeled_textarea(form, 'Text:', 'text', text,
      cols='58', rows='15', placeholder='Write something...')
    form.br
    form.input(type_='hidden', name='fake_out_caching',
               value=str(randrange(2**32)))
    form.input(type_='submit', value='post')


def labeled_field(form, label, type_, name, value, **kw):
  form.label(label, for_=name)
  form.input(type_=type_, name=name, value=value, **kw)


def labeled_textarea(form, label, name, value, **kw):
  form.label(label, for_=name)
  form.br
  form.textarea(value, name=name, **kw)


##def path_link(home, kind, unit):
##  link = linkerate(kind, unit)
##  home.a(link, href=link)
##
##
##  body.hr
##  path_link(body, randrange(2**32), randrange(2**32))
##  body.br
