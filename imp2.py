# Written by Nickoli Londura and Chase Denecke
# CS325 at Oregon State University
# Winter 2019

import sys
import math
import itertools

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

        unsortedCostMatrix = list()
        for x in stringMatrix:
            unsortedCostMatrix.append([y for y in x.split(",")])

        sortedCostMatrix = [[0 for i in range(128)] for j in range(128)]
        
        # Construct the sorted cost matrix by inserting the cost of a particular swap into the ordered
        # table at the indexes given by the ASCII values of the characters whose swap cost we are interested in
        for i in range(1, len(unsortedCostMatrix)):
            for j in range(1, len(unsortedCostMatrix[0])):
                sortedCostRow = ord(unsortedCostMatrix[i][0]) # Use the ASCII value of the character to index the sorted cost table.
                sortedCostColumn = ord(unsortedCostMatrix[0][j])
                sortedCostMatrix[sortedCostRow][sortedCostColumn] = int(unsortedCostMatrix[i][j])
                sortedCostMatrix[sortedCostColumn][sortedCostRow] = int(unsortedCostMatrix[i][j])
        
        self.costMatrix = sortedCostMatrix
    
    # Reads the input file passed in as a command line argument and puts the contents into two lists
    def readInputFile(self, inputFileName = "imp2input.txt"):
        with open(inputFileName, "r") as inputFile:
            for count, line in enumerate(inputFile):
                self.inputMatrix.append([x.strip() for x in line.split(',')])

    def cost(self, char1, char2):
        return self.costMatrix[ord(char1)][ord(char2)]
    
    def minPath(self, i, j):
        if i == 0 and j == 0:
            return
        elif j == 0:
            return "up"
        elif i == 0:
            return "left"
        left = self.alignmentMatrix[i][j-1]
        up = self.alignmentMatrix[i-1][j]
        up_left = self.alignmentMatrix[i-1][j-1]
        if up_left <= left and up_left <= up:
            return "up-left"
        elif up <= left and up <= up_left:
            return "up"
        elif left <= up and left <= up_left:
            return "left"
        

        # if left <= up and left <= up_left:
        #     return "left"
        # elif up <= left and up <= up_left:
        #     return "up"
        # elif up_left <= left and up_left <= up:
        #     return "up-left"

    # Letters of pairOfStrings[0] are rows, letters of pairOfStrings[1] are columns
    def outputAlignments(self):
        outFile = open("imp2output.txt", "w")
        for pairOfStrings in self.inputMatrix:
            pairOfStrings[0] = "-" + pairOfStrings[0]
            pairOfStrings[1] = "-" + pairOfStrings[1]
            self.alignmentMatrix = [[0 for i in range(len(pairOfStrings[1]))] for j in range(len(pairOfStrings[0]))]
            # Fill the first column with cost values
            self.alignmentMatrix[0][0] = 0
            for i in range(1, len(pairOfStrings[0])):
                self.alignmentMatrix[i][0] = self.cost(pairOfStrings[0][i], '-') + self.alignmentMatrix[i-1][0]
            # Fill the first row with cost values
            for i in range(1, len(pairOfStrings[1])):
                self.alignmentMatrix[0][i] = self.cost(pairOfStrings[1][i], '-') + self.alignmentMatrix[0][i-1]
            # Fill the rest of the alignment matrix with cost values
            for i in range(1, len(pairOfStrings[0])):
                for j in range(1, len(pairOfStrings[1])):
                    self.alignmentMatrix[i][j] = min(self.alignmentMatrix[i-1][j] + self.cost(pairOfStrings[0][i], '-'), 
                                                     self.alignmentMatrix[i][j-1] + self.cost(pairOfStrings[1][j], '-'), 
                                                     self.alignmentMatrix[i-1][j-1] + self.cost(pairOfStrings[0][i], pairOfStrings[1][j])) 
                    # self.alignmentMatrix[i][j] = pairOfStrings[0][i] + " " + pairOfStrings[1][j]

            # Read backwards through the matrix to compute the optimal alignment
            tempString1 = tempString2 = ""
            string1Iterator = len(pairOfStrings[0]) - 1
            string2Iterator = len(pairOfStrings[1]) - 1
            backwardsAlignmentString1 = backwardsAlignmentString2 = ""
            while string1Iterator != 0 or string2Iterator != 0:
                minPathString = self.minPath(string1Iterator, string2Iterator)
                if minPathString== "left":
                    tempString1 += "-"
                    tempString2 += pairOfStrings[1][string2Iterator]
                    string2Iterator -= 1
                elif minPathString == "up":
                    tempString1 += pairOfStrings[0][string1Iterator]
                    tempString2 += "-"
                    string1Iterator -= 1
                elif minPathString == "up-left":
                    tempString1 += pairOfStrings[0][string1Iterator]
                    tempString2 += pairOfStrings[1][string2Iterator]
                    string1Iterator -= 1
                    string2Iterator -= 1
            tempString1 = tempString1[::-1]
            tempString2 = tempString2[::-1]
            totalCost = self.alignmentMatrix[len(pairOfStrings[0]) - 1][len(pairOfStrings[1]) - 1] # Total cost will be the final number in the bottom right corner of the matrix
            outputLine = tempString1 + "," + tempString2 + ":" + str(totalCost) + "\r\n"
            outFile.write(outputLine)
            
# readCostFile()

comparer = StringComparer()
comparer.outputAlignments()
# call member functions of StringComparer class to execute the rest of the script