from joy.library import initialize
from joy.joy import joy


dictionary = initialize()


def JOY(expression, stack):
  global dictionary
  stack, _, D = joy(stack, expression, dictionary)
  dictionary = D
  return stack
