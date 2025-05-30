#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>, Alexandre Jesus <me@adbjesus.com>
#
# SPDX-License-Identifier: Apache-2.0

import random, operator, time, math, heapq
import logging

logger = logging.getLogger("iterations")

maxtimer = 50
def Search(solution): #pruning, depth first search
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
def Best_first(solution): #pruning, Best first search
    global time_spent
    start = time.time()

    prob = solution.problem

    solutions = []
    Best_value = solution.objective_value()
    Best_solution = solution
    uid = 0
    heapq.heappush(solutions, (-Best_value, uid, solution))


    subValues = dict()
    while solutions != [] and time.time() - start < maxtimer:
        neg_score, _, sol = heapq.heappop(solutions)
        score = -neg_score
        if Best_value < score:
            Best_solution = sol
            Best_value = score
        constr_rule = sol.construction_neighbourhood()
        moves = list(constr_rule.moves(sol))
        
        cache = dict()
        
        #Towns on path pruning, with caching for improved performance
        if not (sol.sequence[-1] in cache.keys()):
            prunable = set()
            for move in moves:
                temp1 = sol.copy()
                move.apply(temp1)
                if temp1.objective_value() <= score:
                    continue
                for move2 in moves:
                    if move is move2:
                        continue
                    if between(
                            prob.towns[sol.sequence[-1]],
                            prob.towns[move2.town],    # B
                            prob.towns[move.town]     # C
                        ):
                        prunable.add(move)  # mark the C‐move for removal
            
            cache[sol.sequence[-1]] = set(moves) - prunable
        moves = cache[sol.sequence[-1]]
        
        
        for move in moves:
            temp_sol = sol.copy()
            move.apply(temp_sol)

            temp_val = temp_sol.objective_value()
            best_val = Best_solution.objective_value()

            #simple pruning
            if temp_val == score or temp_sol.upper_bound() < best_val:
                continue
            
            
            spent_start = time.time_ns()
            shouldPrune  = False
            past = temp_sol.copy()
            for i in range(len(temp_sol.sequence)-1):
                subSol = (past.sequence[0], frozenset(past.sequence), past.sequence[-1])
                past.time = -1
                if subValues.get(subSol, -1) >= past.objective_value():
                    shouldPrune  = True
                    break
                subValues[subSol] = past.objective_value()
                past.sequence = past.sequence[1:]
            if shouldPrune :
                continue
            time_spent += time.time_ns() - spent_start
            uid += 1
            heapq.heappush(solutions, (-temp_sol.objective_value(), uid ,temp_sol))
    print(time.time() - start)
    return Best_solution
        


def between(town1,town2,town3):
    return ((min(town1[1], town3[1]) < town2[1] and town2[1] < max(town1[1], town3[1])) and
             (min(town1[2], town3[2]) < town2[2] and town2[2] < max(town1[2], town3[2])))