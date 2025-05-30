#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import math
import random

Value = int | float

Increment = int | float

class Problem:
    def __init__(self, towns):
        self.n = len(towns)
        self.towns = towns

    def __str__(self):
        p = " ".join(list(map(str, self.towns)))
        d = " ".join(list(map(str, self.initPos)))
        return f"Problem with {self.n} towns\n List of towns:\t {p}\:\t"

    @classmethod
    def from_textio(cls, f):
        """
        Create a problem from a text I/O source `f`
        """
        print(f)
        n = int(f.readline())
        towns = []
        for i in range(n):
            line = list(map(int, f.readline().split()))
            # Each town is represented as a tuple: (index, x, y, height, rate)
            towns.append([i] + line)  # prepend the index to the village data
        towns[0] += [0,0]
        return cls(towns)



