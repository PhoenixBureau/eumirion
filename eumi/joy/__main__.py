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
