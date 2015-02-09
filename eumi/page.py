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


FIELDS = 'title', 'text'
DEFAULT_TITLE = 'no title'
DEFAULT_TEXT = 'Write something...'


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
    page_data = {'text': DEFAULT_TEXT}

  form = get_form_data(environ)
  for field in FIELDS:
    value = form.getfirst(field)
    if value is not None:
      page_data[field] = value

  location = environ['path']
  self_link = linkerate(*location)
  message = 'Current location: ' + self_link

  title = page_data.get('title', DEFAULT_TITLE).title()
  text = page_data['text']
  head.title(title)
  body.h1.a(title, href=self_link)
  body.div(text)

##  body.hr
##  path_link(body, randrange(2**32), randrange(2**32))
##  body.br
  body.hr

  with body.form(action=self_link, method='POST') as form:
    labeled_field(form, 'Title:', 'text', 'title', title, size='44')
    form.br
    labeled_textarea(form, 'Text:', 'text', text, '88', '5')
    form.br
    form.input(
      type_='hidden',
      name='fake_out_caching',
      value=str(randrange(2**32)),
      )
    form.input(type_='submit', value='post')

  return page_data


def get_form_data(environ):
  environ['QUERY_STRING'] = ''
  return FieldStorage(
    fp=environ['wsgi.input'],
    environ=environ,
    keep_blank_values=True,
    )


def labeled_field(form, label, type_, name, value, **kw):
  form.label(label, for_=name)
  form.input(type_=type_, name=name, value=value, **kw)


def labeled_textarea(form, label, name, value, cols, rows, **kw):
  form.label(label, for_=name)
  form.br
  form.textarea(value, name=name, cols=cols, rows=rows, **kw)


def hexify(i):
  s = hex(i)[2:]
  return '0' * (8 - len(s)) + s


def linkerate(head, tail):
  return '/%08s/%s' % (hexify(head), hexify(tail))


def path_link(home, head, tail):
  link = linkerate(head, tail)
  home.a(link, href=link)