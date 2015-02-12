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
from library import *
from combinators import *
from functions import FUNCTIONS, FunctionWrapper
from definitions import DefinitionWrapper


FUNCTIONS.update({

  # Functions.
  'clear': FunctionWrapper(clear),
  'concat': FunctionWrapper(concat),
  'cons': FunctionWrapper(cons),
  'dup': FunctionWrapper(dup),
  'dupd': FunctionWrapper(dupd),
  'id': FunctionWrapper(id_),
  'pop': FunctionWrapper(pop),
  'popd': FunctionWrapper(popd),
  'popop': FunctionWrapper(popop),
  'pred': FunctionWrapper(pred),
  'reverse': FunctionWrapper(reverse),
  'rolldown': FunctionWrapper(rolldown),
  'rollup': FunctionWrapper(rollup),
  'stack': FunctionWrapper(stack_),
  'succ': FunctionWrapper(succ),
  'swap': FunctionWrapper(swap),
  'uncons': FunctionWrapper(uncons),
  'unstack': FunctionWrapper(unstack),
  'zip': FunctionWrapper(zip_),

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
