#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>, Alexandre Jesus <me@adbjesus.com>
#
# SPDX-License-Identifier: Apache-2.0

import random, operator, time, math
import logging

logger = logging.getLogger("iterations")

timer = 0
maxtimer = 10000
def Search(solution): #Heuristics and pruning, depth first search
    global timer
    if solution.sequence == [0]:
        timer = 0
    constr_rule = solution.construction_neighbourhood()
    moves = list(constr_rule.moves(solution))
    if moves == []:
        return solution
    
    best_solution = solution.copy()
    first_value = solution.objective_value()
    best_value = best_solution.objective_value()

    moves = Heuristic_sort(moves, solution)
    for move in moves:
        if timer > maxtimer:
            continue
        temp_solution = solution.copy()
        move.apply(temp_solution)

        if temp_solution.objective_value() == first_value:
            continue

        temp_solution = Search(temp_solution)

        temp_value = temp_solution.objective_value()
        if temp_value > best_value:
            best_solution, best_value = temp_solution, temp_value
    timer += 1
    return best_solution

def Heuristic_sort(moves, solution):
    return moves


def Best_first(solution):
    global timer
    timer = 0
    solutions = [solution]
    Best_value = solution.objective_value()
    Best_solution = solution
    while solutions != [] and timer < maxtimer:
        if Best_value < solutions[-1].objective_value():
            Best_solution = solutions[-1]
            Best_value = solutions[-1].objective_value()
        sol = solutions[-1]
        solutions.pop()
        constr_rule = sol.construction_neighbourhood()
        moves = list(constr_rule.moves(sol))
        for move in moves:
            temp_sol = sol.copy()
            move.apply(temp_sol)
            i = binary_search([x.objective_value() for x in solutions], temp_sol.objective_value(), 0, len(solutions) - 1)
            solutions.insert(i, temp_sol)
    return Best_solution
        

def binary_search(arr, val, start, end):
    if start == end:
        if arr[start] > val:
            return start
        else:
            return start+1
        
    if start > end:
        return start

    mid = int((start+end)/2)
    if arr[mid] < val:
        return binary_search(arr, val, mid+1, end)
    elif arr[mid] > val:
        return binary_search(arr, val, start, mid-1)
    else:
        return mid
