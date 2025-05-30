import roas.simple_solvers as solvers
from api.problem import Problem
from api.solution import Solution
import sys
import matplotlib.pyplot as plt  


if __name__ == '__main__':
    if len(sys.argv)==2:
        with open(sys.argv[1], 'r') as f:
            prob = Problem.from_textio(f)
    if (prob):
        sol2 = solvers.Best_first(Solution.empty_solution(prob))
        print("Heuristics search with pruning: {:.2f}".format(sol2.objective_value()))
        print(sol2)
        print(Solution(prob, [0,1,3,2,4],[]).objective_value())
        temp = sys.argv[1]
        out_f = temp.split('.')
        out_f[-1] = ".out"
        out_f =''.join(out_f)
        print(out_f)
        with open(out_f,"w") as out:
            out.write(sol2.__str__())





