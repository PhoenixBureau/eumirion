# -*- coding: utf-8 -*-
#
#    Copyright © 2015 Simon Forman
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
from sys import argv
from traceback import print_exc
from .joy import joy, run
from .initializer import FUNCTIONS, FunctionWrapper
from .stack import strstack
from . import tracer


def TRACE(stack):
  '''
  Toggle print-out of execution trace.
  '''
  tracer.TRACE = not tracer.TRACE
  return stack


FUNCTIONS['TRACE'] = FunctionWrapper(TRACE)


def repl(stack=()):
  '''
  Read-Evaluate-Print Loop

  Accept input and run it on the stack, loop.
  '''
  try:
    while True:

      print
      print '->', strstack(stack)
      print

      try:
        text = raw_input('joy? ')
      except (EOFError, KeyboardInterrupt):
        break

      if tracer.TRACE: joy.reset()

      try:
        stack = run(text, stack)
      except:
        print_exc()

      if tracer.TRACE: joy.show_trace()

  except:
    print_exc()
  print
  return stack


stack = repl()
