#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>, Alexandre Jesus <me@adbjesus.com>
#
# SPDX-License-Identifier: Apache-2.0

import random, operator, time, math
import logging

logger = logging.getLogger("iterations")

def Search(solution): #Heuristics and pruning, depth first search
    constr_rule = solution.construction_neighbourhood()
    moves = list(constr_rule.moves(solution))
    if moves == []:
        return solution
    
    best_solution = solution.copy()
    first_value = solution.objective_value()
    best_value = best_solution.objective_value()

    moves = Heuristic_sort(moves, solution)
    for move in moves:
        temp_solution = solution.copy()
        move.apply(temp_solution)

        if temp_solution.objective_value() == first_value:
            continue

        temp_solution = Search(temp_solution)

        temp_value = temp_solution.objective_value()
        if temp_value > best_value:
            best_solution, best_value = temp_solution, temp_value
    return best_solution

def Heuristic_sort(moves, solution):
    return moves