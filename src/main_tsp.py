#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import roas.simple_solvers as solvers
from api.problem import Problem
from api.solution import Solution
import sys
import matplotlib.pyplot as plt  

from log_config import setup_logging
setup_logging()
import logging
logger = logging.getLogger("Main")

if __name__ == '__main__':
    if len(sys.argv)==2:
        with open(sys.argv[1], 'r') as f:
            prob = Problem.from_textio(f)
        #prob = tsp.Problem.from_textio(sys.stdin)
    else:
        #prob = Problem.from_textio("data/sample.txt")
        pass
    if (prob):
        sol2 = solvers.Search(Solution.empty_solution(prob))
        print("Heuristics search with pruning: {:.2f}".format(sol2.objective_value()))
        print(sol2)
        print(Solution(prob, [0,1,3,2,4],[]).objective_value())




