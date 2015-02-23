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


Definitions
  functions as equations


Use this to re-generate the definitions in initializer.py.

>>> from eumi.joy import initializer
>>> from eumi.joy.definitions import generate_definitions
>>> generate_definitions()

Copy and paste the output into initializer.py.  It is a little crude but
it works.


'''
from textwrap import dedent
from .joy import joy
from .parser import text_to_expression
from .functions import FunctionWrapper, FUNCTIONS


DEFINITIONS = '''

# This is one of the most basic commands.
# It provides the rest of a sequence...

  rest == uncons popd


;
# This is ALSO one of the most basic commands.
# It provides the first item of a sequence...

  first == uncons pop


;

  second == rest first ;
  third == rest rest first ;

  sum == 0 swap [+] step ;
  product == 1 swap [*] step ;

  swons == swap cons ;
  swoncat == swap concat ;
  shunt == [swons] step ;
  reverse == [] swap shunt ;
  flatten == [] swap [concat] step ;

  unit == [] cons ;
  quoted == [unit] dip ;
  unquoted == [i] dip ;

  enstacken == stack [clear] dip ;
  disenstacken == [truth] [uncons] while pop ;

  pam == [i] map ;
  run == [] swap infra ;
  size == [1] map sum ;
  size == 0 swap [pop ++] step ;

  average == [sum 1.0 *] [size] cleave / ;

  gcd == [0 >] [dup rollup modulus] while pop ;

  least_fraction == dup [gcd] infra [/] concat map ;


  divisor == popop 2 * ;
  minusb == pop neg ;
  radical == swap dup * rollup * 4 * - sqrt ;
  root1 == + swap / ;
  root2 == - swap / ;

  quadratic ==
    [[[divisor] [minusb] [radical]] pam] ternary i
    [[[root1] [root2]] pam] ternary ;


  *fraction ==
    [uncons] dip uncons
    [swap] dip concat
    [*] infra [*] dip cons ;

  *fraction0 == concat [[swap] dip * [*] dip] infra ;


  down_to_zero == [0 >] [dup --] while ;
  range_to_zero == unit [down_to_zero] infra ;

  times == [-- dip] cons [swap] infra [0 >] swap while pop ;


''' # End of DEFINITIONS


class DefinitionWrapper(FunctionWrapper):
  '''
  Allow functions to have a nice repr().
  '''

  def __init__(self, name, body_text, doc=None):
    self.name = self.__name__ = name
    self.body = text_to_expression(body_text)
    self.__doc__ = doc or body_text

  def __call__(self, stack):
    return joy(self.body, stack)


  @classmethod
  def parse_definition(class_, definition, doc_char='#'):
    '''
    Given some text describing a Joy function definition parse it and
    return a DefinitionWrapper.
    '''
    lines = body_lines, doc_lines = [], []
    for line in definition.splitlines(True):
      docy = line.lstrip().startswith(doc_char)
      lines[docy].append(line.lstrip(doc_char))
    doc, defi = dedent(''.join(doc_lines)), ''.join(body_lines)
    name, proper, body_text = (n.strip() for n in defi.partition('=='))
    if not proper:
      raise ValueError('Definition %r failed' % (definition,))
    return DefinitionWrapper(name, body_text, doc)


def generate_definitions(defs=DEFINITIONS, funcs=FUNCTIONS):
  for definition in defs.split(';'):
    definition = definition.lstrip()
    if not definition or definition.isspace():
      continue
    try:
      f = DefinitionWrapper.parse_definition(definition)
    except KeyError, err:
##      print 'Error', err, 'in', definition
      continue
    d = definition.splitlines()
    if len(d) == 1:
      s = "'%s'" % d[0]
    else:
      d = '\n'.join('    '  + line for line in d)
      s = "'''\\\n%s'''" % d
    funcs[f.name] = f
    print "  '%s': DefinitionWrapper.parse_definition(%s)," % (f.name, s)
