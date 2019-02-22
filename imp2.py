# Written by Nickoli Londura and Chase Denecke
# CS325 at Oregon State University
# Winter 2019

import sys
import math

# python3 imp2.py imp2cost.txt imp2input.txt
# Default cost file name is imp2cost.txt, but can be overwritten by passing in an argument
# Default cost file name is imp2input.txt, but can be overwritten by passing an argument
class StringComparer:
    def __init__(self):
        self.costMatrix = list()
        self.inputMatrix = list()
        # There's probably some better more Python-ish way to implement this group of if statements
        if len(sys.argv) == 1:
            self.readCostFile()
            self.readInputFile()
        elif len(sys.argv) == 2:
            self.readCostFile(sys.argv[1])
            self.readInputFile()
        elif len(sys.argv) == 3:
            self.readCostFile(sys.argv[1])
            self.readInputFile(sys.argv[2])
        # print(self.costMatrix)
    def readCostFile(self, costFileName = "imp2cost.txt"):
        # Read in file line by line
        # Store each character in a temporary 128x128 list
        # Sort contents alphabetically so that new entries can be found
        # Use modulus of ascii value of character as its index for sorted 2d list
        # This means we need a 128x128 list for all possible ascii values
        # This table will allow us to get constant time access to all translation weights
        
        with open(costFileName, "r") as costFile:
            stringMatrix = costFile.readlines()

        stringMatrix = [x.strip() for x in stringMatrix] 
        print(stringMatrix)

        unsortedCostMatrix = list()
        for x in stringMatrix:
            unsortedCostMatrix.append([y for y in x.split(",")])
        print(unsortedCostMatrix)

        sortedCostMatrix = [[0 for i in range(128)] for j in range(128)]
        
        # Construct the sorted cost matrix by inserting the cost of a particular swap into the ordered
        # table at the indexes given by the ASCII values of the characters whose swap cost we are interested in
        for i in range(1, len(unsortedCostMatrix)):
            for j in range(1, len(unsortedCostMatrix[0])):
                sortedCostRow = ord(unsortedCostMatrix[i][0]) # Use the ASCII value of the character to index the sorted cost table.
                sortedCostColumn = ord(unsortedCostMatrix[0][j])
                sortedCostMatrix[sortedCostRow][sortedCostColumn] = unsortedCostMatrix[i][j]
                sortedCostMatrix[sortedCostColumn][sortedCostRow] = unsortedCostMatrix[i][j]
        
        self.costMatrix = sortedCostMatrix
    
    # Reads the input file passed in as a command line argument and puts the contents into two lists
    def readInputFile(self, inputFileName = "imp2input.txt"):
        with open(inputFileName, "r") as inputFile:
            for count, line in enumerate(inputFile):
                self.inputMatrix.append([x.strip() for x in line.split(',')])
        print(self.inputMatrix)

    def cost(char1, char2):
        # Use Dijkstra's algorithm to compute shortest path through from one node to another 

    # Letters of pairOfStrings[0] are rows, letters of pairOfStrings[1] are columns
    def outputAlignments(self):
        alignmentMatrix = [[0 for i in range(len(pairOfStrings[0]))] for j in range(len(pairOfStrings[1]))]
        for pairOfStrings in self.inputMatrix:
            # Fill the first column with cost values
            for i, x in enumerate(pairOfStrings[0]):
                alignmentMatrix[i][0] = cost(x, '-')
            # Fill the first row with cost values
            for i, x in enumerate(pairOfStrings[1]):
                alignmentMatrix[0][i] = cost(x, '-')
            # Fill the rest of the alignment matrix with cost values
            for i in range(1, len(pairOfStrings[0])):
                for j in range(1, len(pairOfStrings[1]))
                    alignmentMatrix[i][j] = min(alignmentMatrix[i-1][j] + cost(pairOfStrings[0][i], '-'), alignmentMatrix[i][j-1] + cost(pairOfStrings[1][j], '-'), alignmentMatrix[i-1][j-1] + cost(pairOfStrings[0][i], pairOfStrings[1][j]))
            # Read backwards through the matrix to compute the optimal alignment
            tempString1= tempString2 = ""

            

            totalCost = alignmentMatrix[len(pairOfStrings[0]) - 1][len(pairOfStrings[1]) - 1] # Total cost will be the final number in the bottom right corner of the matrix
            
# readCostFile()

comparer = StringComparer()
comparer.outputAlignments()
# call member functions of StringComparer class to execute the rest of the script