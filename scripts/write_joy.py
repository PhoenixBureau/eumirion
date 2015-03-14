from os.path import join
from os import makedirs
from eumi.page_actions import hexify
from eumi.joy.initializer import FUNCTIONS


base_dir = '/home/sforman/Desktop/eumirion/server'
base_unit = '00001000'
joy_dir = join(base_dir, '01010101')

u = int(base_unit, 16)
F = sorted(FUNCTIONS)
U = xrange(u, u + len(F))
for i, function_name in zip(U, F):
  function_wrapper = FUNCTIONS[function_name]
  d = join(joy_dir, hexify(i))
  makedirs(d)
  print d, function_name
  with open(join(d, 'title'), 'w') as title:
    title.write(function_name)
  with open(join(d, 'text'), 'w') as text:
    text.write(function_wrapper.__doc__)
  with open(join(d, 'joy'), 'w') as joy:
    joy.write(function_name)

