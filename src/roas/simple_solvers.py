#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>, Alexandre Jesus <me@adbjesus.com>
#
# SPDX-License-Identifier: Apache-2.0

import random, operator, time, math
import logging

logger = logging.getLogger("iterations")

def greedy_construction(solution):
    constr_rule = solution.construction_neighbourhood()
    move_iter = iter(constr_rule.moves(solution))
    move = next(move_iter, None)
    while move is not None:
        best_move, best_incr = move, move.lower_bound_increment(solution)
        for move in move_iter:
            incr = move.lower_bound_increment(solution)
            if incr < best_incr:
                best_move, best_incr = move, incr
                if incr == 0:
                    break
        best_move.apply(solution)
        move_iter = iter(constr_rule.moves(solution))
        move = next(move_iter, None)
    return solution

def greedy_construction_random_tie_breaking(solution):
    constr_rule = solution.construction_neighbourhood()
    move_iter = iter(constr_rule.moves(solution))
    move = next(move_iter, None)
    while move is not None:
        best_move, best_incr = [move], move.lower_bound_increment(solution)
        for move in move_iter:
            incr = move.lower_bound_increment(solution)
            if incr == best_incr or type(incr) == float and math.isclose(best_incr, incr):
                best_move.append(move)
            elif incr < best_incr:
                best_move, best_incr = [move], incr
        random.choice(best_move).apply(solution)
        move_iter = iter(constr_rule.moves(solution))
        move = next(move_iter, None)
    return solution

def first_improvement(solution):
    # modifies solution in place and returns a reference to it
    sol_value = solution.objective_value()  
    local_nbhood = solution.local_neighbourhood()
    move_iter = iter(local_nbhood.random_moves_without_replacement(solution))
    move = next(move_iter, None)
    while move is not None:
        increment = move.objective_value_increment(solution)
        if increment < 0:
            move.apply(solution)
            move_iter = iter(local_nbhood.random_moves_without_replacement(solution))
            sol_value += increment
            logger.info(f"new sol found: {sol_value}")
        move = next(move_iter, None)
    return solution

def best_improvement(solution):
    # modifies solution in place and returns a reference to it
    local_nbhood = solution.local_neighbourhood()
    move_iter = iter(local_nbhood.moves(solution))
    move = next(move_iter, None)
    while move is not None:
        best_move, best_incr = move, move.objective_value_increment(solution)
        for move in move_iter:
            incr = move.objective_value_increment(solution)
            if incr < best_incr:
                best_move, best_incr = move, incr
        if best_incr < 0:
            best_move.apply(solution)
            move_iter = iter(local_nbhood.moves(solution))
            logger.info(f"new sol found: {best_incr}")
        move = next(move_iter, None)
    return solution
