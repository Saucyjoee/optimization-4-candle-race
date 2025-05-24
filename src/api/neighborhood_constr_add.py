#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0


from api.base import Neighbourhood, Move


# ------------------------------- Neighbourhood ------------------------------

class AddNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        #dd = [(job,self.problem.due_dates[job]) for job in solution.not_scheduled]
        for town in solution.not_scheduled:
            yield AddMove(self, town)



# ----------------------------------- Move -----------------------------------

class AddMove(Move):
    def __init__(self, neighbourhood, town):
        self.neighbourhood = neighbourhood
        # i and j are cities
        self.town = town

    def __str__(self):
        return "%d" % self.town

    def apply(self, solution):
        #assert solution.tour[-1] == self.i
        prob = solution.problem
        # Update lower bound
        solution.lb += 0
        # Tighter, but *not* better!
        # solution.lb += prob.dist[self.j][solution.tour[0]] - prob.dist[self.i][solution.tour[0]]
        # Update solution
        solution.sequence.append(self.town)
        solution.not_scheduled.remove(self.town)

    def lower_bound_increment(self, solution):
        return 0