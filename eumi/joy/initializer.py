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


Initialize functions.


'''
from .library import *
from .combinators import *
from .functions import (
  ALIASES,
  FUNCTIONS,
  FunctionWrapper,
  BinaryBuiltinWrapper,
  )
from .definitions import DefinitionWrapper
from .morewords import d


import operator


FUNCTIONS['add'] = BinaryBuiltinWrapper(operator.add)
FUNCTIONS['and'] = BinaryBuiltinWrapper(operator.and_)
FUNCTIONS['div'] = BinaryBuiltinWrapper(operator.div)
FUNCTIONS['eq'] = BinaryBuiltinWrapper(operator.eq)
FUNCTIONS['floordiv'] = BinaryBuiltinWrapper(operator.floordiv)
FUNCTIONS['ge'] = BinaryBuiltinWrapper(operator.ge)
FUNCTIONS['gt'] = BinaryBuiltinWrapper(operator.gt)
FUNCTIONS['le'] = BinaryBuiltinWrapper(operator.le)
FUNCTIONS['lshift'] = BinaryBuiltinWrapper(operator.lshift)
FUNCTIONS['lt'] = BinaryBuiltinWrapper(operator.lt)
FUNCTIONS['mod'] = BinaryBuiltinWrapper(operator.mod)
FUNCTIONS['mul'] = BinaryBuiltinWrapper(operator.mul)
FUNCTIONS['ne'] = BinaryBuiltinWrapper(operator.ne)
FUNCTIONS['or'] = BinaryBuiltinWrapper(operator.or_)
FUNCTIONS['pow'] = BinaryBuiltinWrapper(operator.pow)
FUNCTIONS['rshift'] = BinaryBuiltinWrapper(operator.rshift)
FUNCTIONS['sub'] = BinaryBuiltinWrapper(operator.sub)
FUNCTIONS['truediv'] = BinaryBuiltinWrapper(operator.truediv)
FUNCTIONS['xor'] = BinaryBuiltinWrapper(operator.xor)


FUNCTIONS.update({

  # Functions.
  'clear': FunctionWrapper(clear),
  'concat': FunctionWrapper(concat),
  'cons': FunctionWrapper(cons),
  'dup': FunctionWrapper(dup),
  'dupd': FunctionWrapper(dupd),
  'id': FunctionWrapper(id_),
  'min': FunctionWrapper(min_),
  'pop': FunctionWrapper(pop),
  'popd': FunctionWrapper(popd),
  'popop': FunctionWrapper(popop),
  'pred': FunctionWrapper(pred),
  'remove': FunctionWrapper(remove),
  'reverse': FunctionWrapper(reverse),
  'rolldown': FunctionWrapper(rolldown),
  'rollup': FunctionWrapper(rollup),
  'stack': FunctionWrapper(stack_),
  'succ': FunctionWrapper(succ),
  'sum': FunctionWrapper(sum_),
  'swap': FunctionWrapper(swap),
  'uncons': FunctionWrapper(uncons),
  'unstack': FunctionWrapper(unstack),
  'zip': FunctionWrapper(zip_),

  'd': FunctionWrapper(d),

  # Combinators.
  'app1': FunctionWrapper(app1),
  'app2': FunctionWrapper(app2),
  'app3': FunctionWrapper(app3),
  'b': FunctionWrapper(b),
  'binary': FunctionWrapper(binary),
  'cleave': FunctionWrapper(cleave),
  'dip': FunctionWrapper(dip),
  'dipd': FunctionWrapper(dipd),
  'dipdd': FunctionWrapper(dipdd),
  'i': FunctionWrapper(i),
  'ifte': FunctionWrapper(ifte),
  'infra': FunctionWrapper(infra),
  'map': FunctionWrapper(map_),
  'nullary': FunctionWrapper(nullary),
  'step': FunctionWrapper(step),
  'ternary': FunctionWrapper(ternary),
  'unary': FunctionWrapper(unary),
  'while': FunctionWrapper(while_),
  'x': FunctionWrapper(x),
  })


for op, aliases in ALIASES:
  if op in FUNCTIONS:
    op = FUNCTIONS[op]
    for alias in aliases:
      FUNCTIONS[alias] = op


# Definitions.
# (Note that these are not in alphabetical order, as some depend on
# others that must be defined before them.)

FUNCTIONS.update({
  'rest': DefinitionWrapper.parse_definition('''\
    # This is one of the most basic commands.
    # It provides the rest of a sequence...
    
      rest == uncons popd
    
    '''),
  })

FUNCTIONS.update({
  'first': DefinitionWrapper.parse_definition('''\
    # This is ALSO one of the most basic commands.
    # It provides the first item of a sequence...
    
      first == uncons pop
    
    '''),
  })

FUNCTIONS.update({
  'second': DefinitionWrapper.parse_definition('second == rest first '),
  })

FUNCTIONS.update({
  'third': DefinitionWrapper.parse_definition('third == rest rest first '),
  })

FUNCTIONS.update({
  'swons': DefinitionWrapper.parse_definition('swons == swap cons '),
  })

FUNCTIONS.update({
  'swoncat': DefinitionWrapper.parse_definition('swoncat == swap concat '),
  })

FUNCTIONS.update({
  'shunt': DefinitionWrapper.parse_definition('shunt == [swons] step '),
  })

FUNCTIONS.update({
  'reverse': DefinitionWrapper.parse_definition('reverse == [] swap shunt '),
  })

FUNCTIONS.update({
  'flatten': DefinitionWrapper.parse_definition('flatten == [] swap [concat] step '),
  })

FUNCTIONS.update({
  'unit': DefinitionWrapper.parse_definition('unit == [] cons '),
  })

FUNCTIONS.update({
  'quoted': DefinitionWrapper.parse_definition('quoted == [unit] dip '),
  })

FUNCTIONS.update({
  'unquoted': DefinitionWrapper.parse_definition('unquoted == [i] dip '),
  })

FUNCTIONS.update({
  'enstacken': DefinitionWrapper.parse_definition('enstacken == stack [clear] dip '),
  })

FUNCTIONS.update({
  'pam': DefinitionWrapper.parse_definition('pam == [i] map '),
  })

FUNCTIONS.update({
  'run': DefinitionWrapper.parse_definition('run == [] swap infra '),
  })
