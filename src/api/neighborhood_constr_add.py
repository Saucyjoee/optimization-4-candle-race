


from api.base import Neighbourhood, Move


# ------------------------------- Neighbourhood ------------------------------

class AddNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        for town in solution.not_scheduled:
            yield AddMove(self, town)



# ----------------------------------- Move -----------------------------------

class AddMove(Move):
    def __init__(self, neighbourhood, town):
        self.neighbourhood = neighbourhood
        self.town = town

    def __str__(self):
        return "%d" % self.town

    def apply(self, solution):
        prob = solution.problem

        if self.town in solution.not_scheduled and not self.town in solution.sequence:
            pos = prob.towns[solution.sequence[-1]][1:3]
            solution.sequence.append(self.town)
            solution.not_scheduled.remove(self.town)

            DT = abs(pos[0] - prob.towns[solution.sequence[-1]][1:3][0]) + abs(pos[1] - prob.towns[solution.sequence[-1]][1:3][1])
            solution.time += DT
            solution.value = max(0, prob.towns[solution.sequence[-1]][3] - (DT*prob.towns[solution.sequence[-1]][4]))

    def lower_bound_increment(self, solution):
        return solution.objective_value()