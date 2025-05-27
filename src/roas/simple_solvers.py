#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>, Alexandre Jesus <me@adbjesus.com>
#
# SPDX-License-Identifier: Apache-2.0

import random, operator, time, math
import logging

logger = logging.getLogger("iterations")

def Search(solution): #Heuristics and pruning, best first search
    constr_rule = solution.construction_neighbourhood()
    moves = constr_rule.moves(solution)
    best_solution = solution.copy()
    best_value = best_solution.objective_value()
    for move in moves:
        temp_solution = solution.copy()
        move.apply(temp_solution)
        temp_value = temp_solution.objective_value() + 0 #replace 0 with a heuristics function
        if temp_value > best_value:
            best_solution, best_value = temp_solution, temp_value
    if best_value == solution.objective_value():
        return best_solution
    else:
        return Search(best_solution)