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
  update_page_data(page_data, environ)

  location = environ['path']
  self_link = linkerate(*location)

  title = page_data['title'].title()
  text = page_data['text']
  head.title(title or self_link)
  body.h1.a(title or DEFAULT_TITLE, href=self_link)
  render_text(body.div, text or DEFAULT_TEXT, router)
  body.hr

  with body.form(action=self_link, method='POST') as form:
    form.h4('Edit')
    labeled_field(form, 'Title:', 'text', 'title', title,
                  size='44', placeholder=DEFAULT_TITLE)
    form.br
    labeled_textarea(form, 'Text:', 'text', text,
                     cols='88', rows='5', placeholder='Write something...')
    form.br
    form.input(type_='hidden', name='fake_out_caching', value=str(randrange(2**32)))
    form.input(type_='submit', value='post')

  return page_data


def update_page_data(page_data, environ):
  form = get_form_data(environ)
  for field in FIELDS:
    value = form.getfirst(field)
    if value is not None:
      page_data[field] = value


def get_form_data(environ):
  environ['QUERY_STRING'] = ''
  return FieldStorage(
    fp=environ['wsgi.input'],
    environ=environ,
    keep_blank_values=True,
    )


link_finder = RegularExpression('/([0-9a-f]{8})' * 2, flags=IGNORECASE)


def render_text(home, text, router):
  for paragraph in text.splitlines(False):
    linkenate(home.p, render_link, paragraph, link_finder, router)


def linkenate(p, render_link, text, regex, router):
  '''
  Given some text and a paragraph element, convert links in the text to
  actual hyperlinks, looking up titles if any, and render into the
  paragraph element.
  '''
  begin = 0
  for match in regex.finditer(text):
    p(text[begin:match.start()])
    begin = match.end()
    render_link(p, match, router)
  p(text[begin:])


def render_link(p, match, router):
  piece = match.groups()
  link = '/%s/%s' % piece
  coordinates = tuple(int(n, 16) for n in piece)
  try:
    page_handler = router[coordinates]
  except KeyError:
    link_text = link
  else:
    link_text = page_handler.data['title'] or link
  if link_text == link:
    link_text = 'jump to ' + link_text
  p.a(link_text, href=link)


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


def linkerate(head, tail):
  return '/%s/%s' % (hexify(head), hexify(tail))


def path_link(home, head, tail):
  link = linkerate(head, tail)
  home.a(link, href=link)


##  body.hr
##  path_link(body, randrange(2**32), randrange(2**32))
##  body.br
