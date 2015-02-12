# -*- coding: utf-8 -*-
#
#    Copyright © 2014, 2015 Simon Forman
#
#    This file is part of joy.py
#
#    joy.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    joy.py is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with joy.py.  If not see <http://www.gnu.org/licenses/>.
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

  # Definitions.
  'rest': DefinitionWrapper('''\
    # This is one of the most basic commands.
    # It provides the rest of a sequence...
    
      rest == uncons popd
    
    '''),
  'first': DefinitionWrapper('''\
    # This is ALSO one of the most basic commands.
    # It provides the first item of a sequence...
    
      first == uncons pop
    
    '''),
  'second': DefinitionWrapper('second == rest first '),
  'third': DefinitionWrapper('third == rest rest first '),
  'swons': DefinitionWrapper('swons == swap cons '),
  'swoncat': DefinitionWrapper('swoncat == swap concat '),
  'shunt': DefinitionWrapper('shunt == [swons] step '),
  'reverse': DefinitionWrapper('reverse == [] swap shunt '),
  'flatten': DefinitionWrapper('flatten == [] swap [concat] step '),
  'unit': DefinitionWrapper('unit == [] cons '),
  'quoted': DefinitionWrapper('quoted == [unit] dip '),
  'unquoted': DefinitionWrapper('unquoted == [i] dip '),
  'enstacken': DefinitionWrapper('enstacken == stack [clear] dip '),
  'pam': DefinitionWrapper('pam == [i] map '),
  'run': DefinitionWrapper('run == [] swap infra '),





  })
