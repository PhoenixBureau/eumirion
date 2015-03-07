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
'''
Some HTML and HTTP support stuff.

The interface of the HTML generation class is pretty directly based on
https://pypi.python.org/pypi/html but it uses ElementTree to render the
HTML output.
'''
from random import randrange
from xml.etree.ElementTree import Element, SubElement, tostringlist


def posting(environ):
  return environ['REQUEST_METHOD'] == 'POST'


def start(start_response, message, mime_type):
  start_response(message, [('Content-type', mime_type)])


def err500(start_response, message):
  start(start_response, '500 Internal Server Error', 'text/plain')
  return [str(message)]


def ok200(start_response, response):
  start(start_response, '200 OK', 'text/html')
  return response


class HTML(object):

  def __init__(self, element=None):
    if element is None:
      element = Element('html')
    assert isinstance(element, Element), repr(element)
    self.root = self.element = element

  def __getattr__(self, tag):
    e = HTML(SubElement(self.element, tag))
    e.root = self.root
    return e

  def __iadd__(self, other):
    return self._append(self.element, other)

  def _append(self, to, other):
    if isinstance(other, basestring):
      if len(to):
        last = to[-1]
        if last.tail is None:
            last.tail = other
        else:
            last.tail += other
      elif to.text is None:
        to.text = other
      else:
        to.text += other
    elif isinstance(other, Element):
      to.append(other)
    elif isinstance(other, HTML):
      if other.root is self.root:
        raise ValueError('What are you doing? No recursive HTML.')
      to.append(other.element)
    else:
      raise ValueError('Must only add strings or Elements not %r'
                       % (other,))
    return self

  def __call__(self, *content, **kw):
    for it in content:
      self._append(self.element, it)
    self.element.attrib.update((k.rstrip('_'), v) for k, v in kw.iteritems())
    return self

  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, exc_tb):
    pass

  def __repr__(self):
    return '<HTML:%r 0x%x>' % (self.element, id(self))

  def _stringify(self, encoding='us-ascii'):
    return tostringlist(self.element, method='html', encoding=encoding)

  def __str__(self):
    return ''.join(self._stringify())

  def __unicode__(self):
    return u''.join(self._stringify('UTF-8'))

  def __iter__(self):
    return iter(self._stringify())


def all_pages_pre(head, body, title, self_link, default):
  head.title(title or self_link)
  with body.h1 as h1:
    h1.a('O', href='/00000000/00000000')
    h1(' ')
    h1.a(title or default, href=self_link)


def all_pages_post(body, title, text, self_link, default):
  body.hr
  with body.form(action=self_link, method='POST') as form:
    form.h4('Edit')
    labeled_field(form, 'Title:', 'text', 'title', title,
      size='44', placeholder=default)
    form.br
    labeled_textarea(form, 'Text:', 'text', text,
      cols='58', rows='15', placeholder='Write something...')
    form.br
    fake_out_caching(form)
    form.input(type_='submit', value='post')


def fake_out_caching(form):
  form.input(type_='hidden', name='fake_out_caching', value=str(randrange(2**32)))


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
