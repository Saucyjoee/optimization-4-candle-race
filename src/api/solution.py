#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import random
import matplotlib.pyplot as plt  

from api.neighborhood_constr_add import AddNeighbourhood


class Solution:
    def __init__(self, problem, sequence, not_scheduled, value=0, time=0):
        self.problem = problem
        self.sequence = sequence
        self.not_scheduled = not_scheduled
        self.value = value
        self.time = 0
        self.lb = 0

    

        self.c_nbhood = None
        self.l_nbhood = None

    def __str__(self):
        return " ".join(map(str, self.sequence))

    def copy(self):
        return self.__class__(self.problem,
            self.sequence.copy(),
            self.not_scheduled.copy(),
            self.value,
            self.time)

    @classmethod
    def empty_solution(cls, problem):
        return cls(problem, [0], set(range(1,problem.n)))

    @classmethod
    def random_solution(cls, problem):
        c = (list(range(1,problem.n)))
        random.shuffle(c)
        time = 0
        pos = problem.initPos
        value = 0
        for town in c:
            DT = (pos[0] - problem.towns[town][0]) + (pos[1] - problem.towns[town][1])
            time += DT
            pos = problem[town][:3]
            value += max(0, problem[town][2] - (DT*problem[town][3]))

        return cls(problem, [0].append(c), set(), value, time)

    def problem_instance(self):
        return self.problem

    def is_feasible(self):
        return True

    def objective_value(self):
        
        prev_town = self.sequence[0]
        self.time = 0
        self.value = 0
        for town in self.sequence:
            DT = abs(self.problem.towns[prev_town][1] - self.problem.towns[town][1]) + abs(self.problem.towns[prev_town][2] - self.problem.towns[town][2])
            self.time += DT
            self.value += max(0, self.problem.towns[town][3] - (self.time*self.problem.towns[town][4]))
            prev_town = town
        return self.value

    def lower_bound(self):
        return self.lb

    def construction_neighbourhood(self):
        if self.c_nbhood is None:
            self.c_nbhood = AddNeighbourhood(self.problem)
        return self.c_nbhood
    

