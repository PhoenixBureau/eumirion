#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#    Copyright © 2015 Simon Forman
#
#    This file is part of Eumirion.
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
#    along with Eumirion.  If not, see <http://www.gnu.org/licenses/>.
#
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

