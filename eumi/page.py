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
from re import compile as RegularExpression, IGNORECASE
from operator import itemgetter
from itertools import groupby
from .html import posting
from .joy import joy, text_to_expression


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

  location = environ['path']
  self_link = linkerate(*location)
  title = page_data['title']
  text = page_data['text']

  all_pages_pre(head, body, title, self_link)
  render_body(head, body, text, router, self_link)
  all_pages_post(body, title, text, self_link)

  return page_data


def update_page_data(page_data, environ, router):
  form = get_form_data(environ)
  print form
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
    page_data['joy'] = text_to_expression(first_line)
    print page_data['joy']


def run_command(page_data, command, router):
  match = link_finder.match(command)
  if match is None:
    raise ValueError('The command arg is messed up: %r' % (command,))
  action, kind, unit = match_dict(match, 'joy')
  command_data = get_page_data(router, kind, unit)
  try:
    expression = command_data[action]
  except KeyError:
    raise ValueError('No available expression for: %r' % (command,))

  stack = page_data.get('stack', ())
  result = joy(stack, expression)
  page_data['stack'] = result
  print 'stack', page_data['stack']


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
    labeled_field(
      form,
      'Title:',
      'text',
      'title',
      title,
      size='44',
      placeholder=DEFAULT_TITLE,
      )
    form.br
    labeled_textarea(
      form,
      'Text:',
      'text',
      text,
      cols='88',
      rows='5',
      placeholder='Write something...',
      )
    form.br
    form.input(
      type_='hidden',
      name='fake_out_caching',
      value=str(randrange(2**32)),
      )
    form.input(type_='submit', value='post')


def render_body(head, body, text, router, self_link):
  content = body.div
  if not text:
     content.p(DEFAULT_TEXT, class_='default-text')
     return
  for paragraph in text.splitlines(False):
    p = content.p
    for action, kind, unit in scan_text(paragraph):
      renderer = RENDERERS.get(action, unknown)
      renderer(head, p, kind, unit, router, action, self_link)


link_finder = RegularExpression(
  '((?P<action>[a-z]{1,32}):)?'
  '/(?P<kind>[0-9a-f]{8})'
  '/(?P<unit>[0-9a-f]{8})',
  flags=IGNORECASE,
  )


def scan_text(text, regex=link_finder):
  begin = 0
  for match in regex.finditer(text):
    yield 'text', text[begin:match.start()], None
    begin = match.end()
    yield match_dict(match)
  yield 'text', text[begin:], None


def match_dict(match, default='link'):
  d = match.groupdict(default)
  return d['action'], d['kind'], d['unit']


def unknown(head, home, kind, unit, router, action, self_link=None):
  home('unknown action "%s:"' % (action,))
  render_link(head, home, kind, unit, router)


def render_text(head, home, kind, unit, router, action, self_link=None):
  if unit is None:
    home(kind)
    return
  data = get_page_data(router, kind, unit)
  if not data:
    return
  render_body(head, home, data['text'], router)


def render_link(_, home, kind, unit, router, action=None, self_link=None):
  link, link_text = get_link_text(kind, unit, router)
  if link_text is link:
    link_text = 'jump to ' + link_text
  home.a(link_text, href=link)


def render_door(_, home, kind, unit, router, action=None, self_link=None):
  link, link_text = get_link_text(kind, unit, router)
  link_text = '[' + link_text + ']'
  home.a(link_text, href=link, class_='door-link')


def add_css(head, _, kind, unit, router, action=None, self_link=None):
  data = get_page_data(router, kind, unit)
  if data:
    css = data['text']
    head.style(css)


keyfunc = itemgetter(0)


def render_index(head, home, kind, unit, router, action, self_link=None):
  if kind == '00000000':
    keys = router
  else:
    kind = int(kind, 16)
    keys = (key for key in router if key[0] == kind)
  data = sorted(keys, key=keyfunc)
  ol = home.ol
  for kind, units in groupby(data, keyfunc):
    kind = hexify(kind)
    kind_li = ol.li
    render_link(head, kind_li, kind, 8 * '0', router)
    kind_ol = kind_li.ol
    for _, unit in sorted(units):
      if unit:
        unit = hexify(unit)
        render_link(head, kind_ol.li, kind, unit, router)


def render_command(head, home, kind, unit, router, action, self_link):
  link, link_text = get_link_text(kind, unit, router)
  with home.form(
    action=self_link,
    method='POST',
    class_='command',
    ) as form:
    form.input(type_='hidden', name='command', value=_l(kind, unit))
    form.input(type_='submit', value=link_text)


RENDERERS = {
  'text': render_text,
  'link': render_link,
  'door': render_door,
  'css': add_css,
  'index': render_index,
  'command': render_command,
  }


def get_link_text(kind, unit, router):
  link = _l(kind, unit)
  data = get_page_data(router, kind, unit)
  link_text = (data['title'] or link) if data else link
  return link, link_text


def get_page_data(router, kind, unit):
  coordinates = int(kind, 16), int(unit, 16)
  try:
    page_handler = router[coordinates]
  except KeyError:
    return
  return page_handler.data


def labeled_field(form, label, type_, name, value, **kw):
  form.label(label, for_=name)
  form.input(type_=type_, name=name, value=value, **kw)


def labeled_textarea(form, label, name, value, **kw):
  form.label(label, for_=name)
  form.br
  form.textarea(value, name=name, **kw)


def hexify(i):
  s = hex(i)[2:]
  return '0' * (8 - len(s)) + s


def linkerate(kind, unit):
  return _l(hexify(kind), hexify(unit))


_l = lambda kind, unit:'/%s/%s' % (kind, unit)


##def path_link(home, kind, unit):
##  link = linkerate(kind, unit)
##  home.a(link, href=link)
##
##
##  body.hr
##  path_link(body, randrange(2**32), randrange(2**32))
##  body.br
