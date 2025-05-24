from api.problem import Problem
from api.solution import Solution
import random
import math
import sys


if __name__ == '__main__':
    # For testing only
    if len(sys.argv)==2:
        with open(sys.argv[1], 'r') as f:
            prob = Problem.from_textio(f)
    else:
        raise ValueError("Usage: python3 main.py <problem_file>")
    # print(prob)
    # Constructive-search test
    sol = Solution.empty_solution(prob)
    c_rule = sol.construction_neighbourhood()
    moves = list(c_rule.moves(sol))
    lb = sol.lower_bound()
    while len(moves):
        v = random.choice(moves)
        lbi = v.lower_bound_increment(sol)        
        v.apply(sol)
        assert lbi >= 0
        assert math.isclose(sol.lower_bound(), lb + lbi)
        moves = list(c_rule.moves(sol))
        lb = sol.lower_bound()
    print("Random construction")
    print(sol.objective_value())
    print(sol.lower_bound())

    # Local-search test
    l_rule = sol.local_neighbourhood()
    moves = list(l_rule.moves(sol))
    obj = sol.objective_value()
    for _ in range(100):
        v = random.choice(moves)
        obji = v.objective_value_increment(sol)
        v.apply(sol)
        print(v,obj,obji,sol.objective_value())
        assert math.isclose(sol.objective_value(), obj + obji)
        moves = list(l_rule.moves(sol))
        obj = sol.objective_value()
        
    print("After random walk")
    print(sol.objective_value())
    print(sol.lower_bound())
