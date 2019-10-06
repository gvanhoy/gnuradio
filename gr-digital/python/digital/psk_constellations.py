#!/usr/bin/env python
#
# Copyright 2013 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

from __future__ import absolute_import
from __future__ import unicode_literals
import numpy as np

'''
Note on the naming scheme. Each constellation is named using a prefix
for the type of constellation, the order of the constellation, and a
distinguishing feature, which comes in three modes:

- No extra feature: the basic Gray-coded constellation map; others
  will be derived from this type.
- A single number: an indexed number to uniquely identify different
  constellation maps.
- 0xN_x0_x1..._xM: A permutation of the base constellation, explained
  below.

For rectangular constellations (BPSK, QPSK, QAM), we can define a
hyperspace and look for all symmetries. This is also known as the
automorphism group of the hypercube, aka the hyperoctahedral
group. What this means is that we can easily define all possible
rotations in terms of the first base symbols by creating the symbols:

  f(x) = k XOR pi(x)

The x is the bit string for the symbol we are altering. Then k is a
bit string of n bits where n is the number of bits per symbol in the
constellation (e.g., 2 for QPSK or 6 for QAM64). The pi is a
permutation function specified as pi_0, pi_1..., pi_n-1. This permutes
the bits from the base constellation symbol to a new code, which is
then xor'd by k.

The value of k is from 0 to 2^n-1 and pi is a list of all bit
positions.

The total number of Gray coded modulations is (2^n)*(n!).

We create aliases for all possible naming schemes for the
constellations. So if a hyperoctahedral group is defined, we also set
this function equal to a function name using a unique ID number, and
we always select one rotation as our basic rotation that the other
rotations are based off of.
'''

def psk_constellation(const_points, symbols, k, pi):
    const_points, symbols = constellation_map_generator(const_points, symbols, k, pi)
    return digital.constellation_psk(constellation_points, symbols, len(const_points)).base() 

def const_bpsk(k, pi):
    constellation_points = np.exp(2j * np.pi * np.linspace(0, 1, 2) / 2.0)
    symbols = [0, 1]
    return psk_constellation(constellation_points, symbols, k, pi)

def const_qpsk(k, pi):
    constellation_points = np.exp(2j * np.pi * np.linspace(0, 3, 4) / 4.0)
    symbols = [0, 1, 2, 3]
    return psk_constellation(constellation_points, symbols, k, pi)

def const_8psk(k, pi):
    constellation_points = np.exp(2j * np.pi * np.linspace(0, 7, 8) / 8.0)
    symbols = [0, 1, 3, 2, 6, 7, 5]
    return psk_constellation(constellation_points, symbols, k, pi)

if __name__ == "__main__":
    from gnuradio import digital
    from constellation_map_generator import constellation_map_generator

    print(const_bpsk(0, [0]))
    print(const_bpsk(0, [1]))