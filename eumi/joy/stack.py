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


§ Stack


When talking about Joy we use the terms "stack", "list", "sequence" and
"aggregate" to mean the same thing: a simple datatype that permits
certain operations such as iterating and pushing and popping values from
(at least) one end.

We use the venerable two-tuple recursive form of sequences where the
empty tuple () is the empty stack and (head, rest) gives the recursive
form of a stack with one or more items on it.

  ()
  (1, ())
  (1, (2, ()))
  (1, (2, (3, ())))
  ...

And so on.


We have two very simple functions to build up a stack from a Python
iterable and also to iterate through a stack and yield its items
one-by-one in order, and two functions to generate string representations
of stacks:

  list_to_stack()

  iter_stack()

  stack_to_string()

  strstack()



A word about the stack data structure.

Python has very nice "tuple packing and unpacking" in its syntax which
means we can directly "unpack" the expected arguments to a Joy function.

For example:

  def dup(stack):
    head, tail = stack
    return head, (head, tail)

We replace the argument "stack" by the expected structure of the stack,
in this case "(head, tail)", and Python takes care of de-structuring the
incoming argument and assigning values to the names.  Note that Python
syntax doesn't require parentheses around tuples used in expressions
where they would be redundant.
'''


def list_to_stack(el, stack=()):
  '''Convert a list (or other sequence) to a stack.'''
  for item in reversed(el):
    stack = item, stack
  return stack


def iter_stack(stack):
  '''Iterate through the items on the stack.'''
  while stack:
    item, stack = stack
    yield item


def stack_to_string(expression):
  '''
  Return a "pretty print" string for a stack.

  Ideally the output of this should result in the same expression if
  passed through tokenize() and parse(), but not yet.
  '''
  if not isinstance(expression, tuple):
    return repr(expression)
  return '[%s]' % strstack(expression)


def strstack(stack):
  if not isinstance(stack, tuple):
    return repr(stack)
  if not stack: # shortcut
    return ''
  return ' '.join(map(stack_to_string, iter_stack(stack)))