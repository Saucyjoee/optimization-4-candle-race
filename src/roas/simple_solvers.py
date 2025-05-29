#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>, Alexandre Jesus <me@adbjesus.com>
#
# SPDX-License-Identifier: Apache-2.0

import random, operator, time, math
import logging

logger = logging.getLogger("iterations")

maxtimer = 60
def Search(solution): #Heuristics and pruning, depth first search
    global start
    if solution.sequence == [0]:
        start = time.time()
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
        if time.time() - start >= maxtimer:
            break
    return best_solution

def Heuristic_sort(moves, solution):
    return moves

time_spent = 0
def Best_first(solution):
    global time_spent
    start = time.time()

    solutions = [solution]
    Best_value = solution.objective_value()
    Best_solution = solution

    subSolutions = set()
    subValues = dict()
    hits = 0
    while solutions != [] and time.time() - start < maxtimer:
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

            if temp_sol.objective_value() == sol.objective_value():
                continue
            
            spent_start = time.time_ns()
            shouldPrune  = False
            past = temp_sol.copy()
            for i in range(len(temp_sol.sequence)-1):
                subSol = (past.sequence[0], frozenset(past.sequence), past.sequence[-1])
                subSolutions.add(subSol)
                past.time = -1
                if subValues.get(subSol, -1) >= past.objective_value():
                    shouldPrune  = True
                    break
                subValues[subSol] = past.objective_value()
                past.sequence = past.sequence[1:]
            if shouldPrune :
                hits += 1
                continue
            time_spent += time.time_ns() - spent_start
            i = binary_search([x.objective_value() for x in solutions], temp_sol.objective_value(), 0, len(solutions) - 1)
            solutions.insert(i, temp_sol)
    print(hits)
    print(time_spent)
    print(time.time() - start)
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
