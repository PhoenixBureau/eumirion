# -*- coding: utf-8 -*-
#
#    Copyright © 2014, 2015 Simon Forman
#
#    This file is part of Eumirion
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
#    along with Eumirion.  If not see <http://www.gnu.org/licenses/>.
#
'''

§ Functions

  stack → stack
  note() decorator
  define several functions
  wrap functions from Python operator module


We can catagorize functions into those that rearrange things on the stack
but don't otherwise process them, those that perform some process on
them, and those that call back into the joy() function to execute one or
more quoted programs themselves.  And, of course, there are commands that
do more than one or all three.

Commands that execute quoted programs are called "Combinators" and
they are the key to Joy's expressiveness and power.  The joy()
function by itself wouldn't accomplish much but with the availability of
several combinators it becomes a powerhouse.

Commands that just rearrange things on the stack can be written in python
as simple tuple unpacking and repacking.

Definitions, functions defined by equations, refactoring and how
important it is..
'''
from __future__ import print_function
from sys import stderr


FUNCTIONS = {}


class FunctionWrapper(object):
  '''
  Allow functions to have a nice repr().
  '''

  def __init__(self, f):
    self.f = f
    self.name = f.__name__.rstrip('_')
    self.__doc__ = f.__doc__ or str(f)

  def __call__(self, stack):
    return self.f(stack)

  def __repr__(self):
    return self.name


class BinaryBuiltinWrapper(FunctionWrapper):

  def __call__(self, stack):
    (a, (b, stack)) = stack
    result = self.f(b, a)
    return result, stack


ALIASES = (
  ('add', ['+']),
  ('mul', ['*']),
  ('truediv', ['/']),
  ('mod', ['%', 'rem', 'remainder', 'modulus']),
  ('eq', ['=']),
  ('ge', ['>=']),
  ('gt', ['>']),
  ('le', ['<=']),
  ('lshift', ['<<']),
  ('lt', ['<']),
  ('ne', ['<>', '!=']),
  ('rshift', ['>>']),
  ('sub', ['-']),
  ('xor', ['^']),
  ('succ', ['++']),
  ('pred', ['--']),
  ('rolldown', ['roll<']),
  ('rollup', ['roll>']),
  ('id', ['•']),
#  ('', ['']),
  )


def convert(token):
  '''Look up symbols in the functions dict.'''
  try:
    return FUNCTIONS[token]
  except KeyError:
    raise KeyError('unknown word: %r' % (token,))


def is_function(term):
  '''
  Return a Boolean value indicating whether or not a term is a function.
  '''
  return isinstance(term, FunctionWrapper)