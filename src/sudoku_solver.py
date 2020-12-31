import sys
import copy
       
class CSP:
    def __init__(self, variables, domains, arcs, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.arcs = arcs

def boxRange(x): return range((x//3)*3,(x//3)*3+3)

# returns true if constraint satisfied
def constraints(x,y):
    return x != y

# generates a list of arcs vij if either same row or column, or in same grid
def arcgen(x,y):
    return ['X'+str(i)+str(j) for i in range(0,9) for j in range(0,9) if 
        (i != x or y != j) and (i == x or j == y or (i in boxRange(x) and j in boxRange(y)))]

def select_unassigned_variable(csp):
    # most constrained variable
    return min(filter(lambda y: len(y[1]) > 1, csp.domains.items()), key=lambda x: len(x[1]))

def order_domain_values(csp, var, domain):
    # least constraining value
    def affected(val):
        num = 0
        neighbors = arcgen(int(var[1]), int(var[2]))
        for n in neighbors:
            if val in csp.domains[n]:
                num += 1
        return num
    domain.sort(key = lambda x: affected(x))
    return domain

def consistentAssignment(csp, var, value):
    # check if conflict with any neighbors with domainsize = 1
    neighbors = arcgen(int(var[1]), int(var[2]))
    for n in neighbors:
        if ((len(csp.domains[n]) == 1) and (value in csp.domains[n])):
            return False
    return True

def revise(csp, Xi, Xj):
    revised = False
    for x in csp.domains[Xi]:
        # csp.domains[Xj] returned a value?!
        if all(not csp.constraints(x, y) for y in csp.domains[Xj]):
            csp.domains[Xi].remove(x)
            revised = True
    return revised

def AC3(csp):
    queue = [(Xi, Xj) for Xi in csp.domains for Xj in csp.arcs[Xi]]
    while queue:
        Xi, Xj = queue.pop()
        if revise(csp, Xi, Xj):
            if (len(csp.domains[Xi]) == 0):
                return False
            for Xk in csp.arcs[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def backtrackingSearch(csp):
    # goal test
    if all(len(csp.domains[k]) == 1 for k in csp.domains):
        solution = [[0 for i in range(9)] for j in range(9)]
        i, j = 0, 0
        for line in solution:
            for entry in line:
                    solution[i][j] = csp.domains['X'+str(i)+str(j)][0]
                    j += 1
                    if j == 9:
                        i += 1
                        j = 0
        return solution
    if not any([len(csp.domains[k]) == 0 for k in csp.domains]):
        nextVar, varDomain = select_unassigned_variable(csp)
        for value in order_domain_values(csp, nextVar, varDomain):
            nextState = copy.deepcopy(csp)
            nextState.domains[nextVar] = [value]
            if consistentAssignment(nextState, nextVar, value):
                if AC3(nextState):                    
                    result = backtrackingSearch(nextState)
                    if result is not None:
                        return result
    return None

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        #TODO: Your code here
        # variables (Xij, value) generated from puzzle
        variables = [('X'+str(i)+str(j), X) for i, row in enumerate(self.puzzle) for j, X in enumerate(row)]    
        # key is variable, values are 0-9
        domains ={}

        for (key, X) in variables:
            if X == 0:
                domains[key] = [x for x in range(1,10)]
            else:
                domains[key] = [X]

        # domains = {key: ([x for x in range(1,10)] if X == 0 else [X]) for (key, X) in variables}
        # key is variable, value is a list of variables that form arc with key
        arcs = {}
        for (key, X) in variables:
            arcs[key] = arcgen(int(key[1]), int(key[2]))
        self.ans = backtrackingSearch(CSP(variables, domains, arcs, constraints))
        # don't print anything here. just return the answer
        # self.ans is a list of lists
        return self.ans

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY

def printSudoku(title, puzzle):
    print('-----------------------------------------')
    print('----------- '+title+' -----------')
    print('-----------------------------------------')
    print(' ','','','','1   2   3   4   5   6   7   8   9')
    print(' ','','','','-   -   -   -   -   -   -   -   -')
    print('a)',str(puzzle[0]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('b)',str(puzzle[1]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('c)',str(puzzle[2]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('d)',str(puzzle[3]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('e)',str(puzzle[4]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('f)',str(puzzle[5]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('g)',str(puzzle[6]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('h)',str(puzzle[7]).replace(',',' |').replace(']',' |').replace('[','| '))
    print('i)',str(puzzle[8]).replace(',',' |').replace(']',' |').replace('[','| '))
    print(' ','','','','-   -   -   -   -   -   -   -   -')

if __name__ == "__main__":
    puzzle = [[0 for i in range(9)] for j in range(9)]
    printSudoku('AC3 SUDOKU SOLVER',puzzle)
    print('-----------------------------------------')
    print('----------------- SETUP -----------------')
    print('-----------------------------------------')
    print('To solve a sudoku matrix you need to specify its input.txt file path.')
    userInput = input('Please, enter the path here:')
    try:
        file = open(userInput, 'r')
    except IOError:
        print ('\nYou need to enter a valid file path!\n')
        raise IOError('Input file not found!')
    
    rows = file.readlines()
    i, j = 0, 0
    for row in rows:
        for number in row:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    printSudoku('ENTERED MATRIX',puzzle)
    userInput = input('Want to solve it? (y/n)')
    if(userInput != '' or userInput != ' '):
        if(userInput == 'y'):
            sudoku = Sudoku(puzzle)
            ans = sudoku.solve()
            printSudoku('SOLVED RESULT', ans)
            with open('../data/output.txt', 'a') as f:
                for i in range(9):
                    for j in range(9):
                        f.write(str(ans[i][j]) + ' ')
                    f.write('\n')
            print('Result saved! (../data/output.txt)')
            print('Thanks for using the AC3 sudoku solver!')
            exit

    