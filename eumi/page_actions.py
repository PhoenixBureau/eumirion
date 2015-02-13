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
from copy import copy
from itertools import groupby
from operator import itemgetter
from re import compile as RegularExpression, IGNORECASE
from .html import fake_out_caching
from .joy.stack import iter_stack, stack_to_string
from .joy.parser import text_to_expression
from .joy.library import concat


def render_body(head, content, page, default=''):
  text = page.text
  router = page.router
  self_link = page.link
  if not text:
    if default:
      content.p(default, class_='default-text')
    return
  for paragraph in text.splitlines(False):
    p = content.p
    for action, kind, unit in scan_text(paragraph):
      renderer = RENDERERS.get(action, unknown)
      renderer(head, p, page, kind, unit, action)


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


def render_stack(head, home, page, kind, unit, action):
  data = get_page_data(page.router, kind, unit)
  if not data or 'stack' not in data:
    return
  ol = home.ol
  for item in iter_stack(data['stack']):
    ol.li(stack_to_string(item))
#    render_body(head, home, data['text'], router, self_link)


def render_stackinto(head, home, page, kind, unit, action):
  data = get_page_data(page.router, kind, unit)
  if not data or 'stack' not in data:
    return
  for item in iter_stack(data['stack']):
    text = item if isinstance(item, str) else stack_to_string(item)
    render_text_deluxe(head, home, page, text)


def render_text(head, home, page, kind, unit, action):
  if unit is None:
    home(kind)
    return
  data = get_page_data(page.router, kind, unit)
  if not data:
    return
  render_text_deluxe(head, home, page, data['text'])


def render_text_deluxe(head, home, page, text):
  page = copy(page)
  page.text = text
  render_body(head, home, page)


def render_link(_, home, page, kind, unit, action=None):
  link, link_text = get_link_text(kind, unit, page.router)
  if link_text is link:
    link_text = 'jump to ' + link_text
  home.a(link_text, href=link)


def render_door(_, home, page, kind, unit, action=None):
  link, link_text = get_link_text(kind, unit, page.router)
  link_text = '[' + link_text + ']'
  home.a(link_text, href=link, class_='door-link')


def add_css(head, _, page, kind, unit, action=None):
  data = get_page_data(page.router, kind, unit)
  if data:
    css = data['text']
    head.style(css)


def add_joy(_, __, page, kind, unit, action=None):
  data = get_page_data(page.router, kind, unit)
  if not data:
    return
  joy, semicolon, doc = data['text'].partition(';')
  expression = text_to_expression(joy)
  if 'joy' in data:
    stack = (expression, (data['joy'], ()))
    result = concat(stack)[0]
  else:
    result = expression
  data['joy'] = result
  print 'Adding joy %s to "%s"' % (result, data['title'])


def index_filter(kind, unit, router):
  if kind == '00000000':
    return router
  kind = int(kind, 16)
  return (key for key in router if key[0] == kind)


def render_index(head, home, page, kind, unit, action,
                 keyfunc=itemgetter(0), filter_=index_filter):
  keys = filter_(kind, unit, page.router)
  data = sorted(keys, key=keyfunc)
  with home.ol as ol:
    for kind, units in groupby(data, keyfunc):
      kind = hexify(kind)
      with ol.li as kind_li:
        render_link(head, kind_li, page, kind, 8 * '0')
        with kind_li.ol as kind_ol:
          for _, unit in sorted(units):
            if unit:
              unit = hexify(unit)
              render_link(head, kind_ol.li, page, kind, unit)


def render_command(head, home, page, kind, unit, action):
  link, link_text = get_link_text(kind, unit, page.router)
  with home.form(
    action=page.link,
    method='POST',
    class_='command',
    ) as form:
    fake_out_caching(form)
    form.input(type_='hidden', name='command', value=l(kind, unit))
    form.input(type_='submit', value=link_text)


RENDERERS = {
  'text': render_text,
  'link': render_link,
  'door': render_door,
  'css': add_css,
  'joy': add_joy,
  'index': render_index,
  'command': render_command,
  'stack': render_stack,
  'stackinto': render_stackinto,
  }


def get_link_text(kind, unit, router):
  link = l(kind, unit)
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


def hexify(i):
  s = hex(i)[2:]
  return '0' * (8 - len(s)) + s


def linkerate(kind, unit):
  return l(hexify(kind), hexify(unit))


l = lambda kind, unit:'/%s/%s' % (kind, unit)
