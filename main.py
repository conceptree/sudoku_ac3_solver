import sys 
import time
from CSP import csp
from AC3 import AC3
import re

# metodo para compilar a matriz 
def buildList(inputPath):
    tempList = []
    with open(inputPath, "r") as inputFile:
        for line in inputFile:
            tempList.append(line)
    inputFile.close()
    return tempList

# itera e imprime as matrizes
def printMatrix(grid):
    stringMatrix = str(grid) 
    n = 9
    lines = [stringMatrix[i:i+n] for i in range(0, len(stringMatrix), n)]
    for line in lines:
        print(' '.join(line))
        
def main():
    inputPath = "./data/input.txt"
    outputPath ="./data/output.txt"
    ac3 = AC3()
    lineList = buildList(inputPath)
    index = 0
    outputFile = open(outputPath, "w")
    
    print ("------------------------------------------------")
    print ("-------- WELCOME TO AC3 SUDOKU RESOLVER --------")
    print ("------------------------------------------------")

    for grid in lineList:
        prev = time.time()
        sudoku = csp(grid=grid)
        solved = ac3.applyAC3(sudoku)
        if ac3.isComplete(sudoku) and solved:
            print ("--------------- Initial problem ---------------")
            printMatrix(grid)
            outputFile.write("Initial problem: " + str(grid) + "\n")
            print ("------------------ Solution -------------------")
            printMatrix(ac3.write(sudoku.values))
            outputFile.write("Solution: " + str(ac3.write(sudoku.values)) + "\n")
            print ("------------------ Results -------------------")
            print ("Solved in: ", time.time()-prev, " seconds \n")
            outputFile.write("Solved in: " + str(time.time()-prev) + " seconds \n")
            index = index + 1

    outputFile.close()

if __name__ == "__main__":
    main()

    