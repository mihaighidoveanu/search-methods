import random
import abc
import numpy as np
import itertools

class AbstractGenetic(abc.ABC):
    def __init__(self, size, steps, mutatation_proba):
        self.steps = steps
        self.mutatation_proba = mutatation_proba
        self.size = size
        self._best = None

    @abc.abstractmethod
    def _gen_populaion():
        pass
    
    @abc.abstractmethod
    def sample():
        pass

    @abc.abstractmethod
    def crossover(x, y):
        """ Should return a iterable of children"""
        pass

    @abc.abstractmethod
    def mutate(child):
        pass

    @abc.abstractmethod
    def fitness(x):
        pass

    def solve(self):
        step = 0
        while step < self.steps:
            print('###################### Step ', step)
            new_population = []
            for i in range(len(self.population)):
                x = self.sample(self.population)
                y = self.sample(self.population, reuse_scores = True)
                # print('X' , x)
                # print('Y' , y)
                for child in self.crossover(x,y):
                    # print('Child ', child)
                    # print('Probability of mutation ', random.random())
                    if random.random() < self.mutatation_proba :
                        child = self.mutate(child)
                        # print('Mutated ', child)
                    new_population.append(child)
            self.population = new_population.copy() 
            print('Population ', self.population)
            # get the state with the best fitness
            self.population.sort(key = self.fitness, reverse = False)
            best = self.population[0]
            self._best = best
            print('##################### Best ', self._best)
            step += 1
        return best

class NQueens(AbstractGenetic):
    def __init__(self, n_queens, **kwargs):
        if n_queens >= 10:
            raise ValueError("Can't play N-Queens with more than 10 queens")
        super().__init__(**kwargs)
        self.population = self._gen_populaion(n_queens)
        self.n_queens = n_queens
        self._matrix_repr = None
        self._scores = None

    def _gen_populaion(self, n_queens):
        population = np.random.randint(1, n_queens, size = (self.size, n_queens))
        population = [ [str(queen) for queen in state] for state in population ]
        population = [ ''.join(state) for state in population]
        return population

    def sample(self, population, reuse_scores = False):
        if not reuse_scores :
            self._scores = [ self.fitness(individual) for individual in population]
        # print('Scores ', scores)
        scores = np.asarray(self._scores)
        probas = scores / sum(self._scores)
        # print('Probas ', probas)
        individual = np.random.choice(population, p = probas)
        return individual

    def crossover(self, x, y):
        if len(x) != len(y):
            raise ValueError('Individual states should have same length')
        assert(len(x) == len(y))
        idx = random.randint(0, len(x) - 1)
        child = x[:idx] + y[idx:]
        return [child]

    def mutate(self, x):
        queen_idx = random.randint(0, len(x) - 1)
        new_move = random.randint(1, self.n_queens)
        new_move = str(new_move)
        new_x = x[:queen_idx] + new_move + x[queen_idx + 1 :]
        return new_x

    def fitness(self, state):
        n = len(state)
        count = 0
        for row1 in state:
            row1 = int(row1) - 1
            col1 = int(state[row1])
            for row2 in range(row1, n):
                row2 = int(row2) - 1
                col2 = int(state[row2])
                q1 = (row1, col1)
                q2 = (row2, col2)
                if not self._attacking(q1, q2):
                    count += 1
        print('Score ', count)
        print(self._state_str(state))
        return count

    def _attacking(self, q1, q2):
        row1, col1 = q1
        row2, col2 = q2
        attacks_row = [row1 - 1, row1, row1 + 1] 
        attacks_col = [col1 - 1, col1, col1 + 1] 
        for row, col in itertools.product(attacks_row, attacks_col):
            if row == row2 and col == col2:
                return True

    def _state_str(self, state):
        matrix = np.zeros( (self.n_queens, self.n_queens))
        if state is not None:
            for row, col in enumerate(state):
                col = int(col) - 1
                matrix[row][col] = 1
        return matrix

    def __str__(self):
        if not self._matrix_repr:
            self._matrix_repr = self._state_str(self._best)
        return str(self._matrix_repr)


if __name__ == '__main__':
    problem = NQueens(n_queens = 4, size = 10, steps = 1000, mutatation_proba = 0.5)
    best = problem.solve()
    print(problem)
