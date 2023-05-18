# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI( AI ):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        ########################################################################
        #							YOUR CODE BEGINS						   #
        ########################################################################
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.startX = startX
        self.startY = startY
        
        
        self.tileCount = 0
        self.lastX = 0
        self.lastY = 0
        self.unmarkedNeighbors = set()
        self.marked = set()
        self.unmarked ={(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                        (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                        (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
                        (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
                        (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)
                        }
        
        
        

        ########################################################################
        #							YOUR CODE ENDS							   #
        ########################################################################

    

    def getAction(self, number: int) -> "Action Object":

        ########################################################################
        #							YOUR CODE BEGINS						   #
        ########################################################################
        
        if self.tileCount == 0:
            x = self.startX
            y = self.startY
            
            self.mark(x, y)
            self.tileCount += 1
            return Action(AI.Action.UNCOVER, x, y)
        
        
        
        elif self.tileCount == 1:
            self.fillUnmarkedNeighbors(self.startX, self.startY)
            x, y = self.unmarkedNeighbors.pop()
            
            
            self.mark(x, y)
            self.tileCount += 1     
            return Action(AI.Action.UNCOVER, x, y)
        
        else:
            if self.tileCount == 24:
                return Action(AI.Action.LEAVE)
            
            if number == 0:
                self.fillUnmarkedNeighbors(self.lastX, self.lastY)
            else:
                pass
                # ?
            
            
            # maybe check if there is unmarked neighbors
            if self.unmarkedNeighbors:
                
                x, y = self.unmarkedNeighbors.pop()
            else:
                x, y = list(self.unmarked)[0] # get random from unmarked
                        
            self.mark(x, y)
            self.tileCount += 1     
            return Action(AI.Action.UNCOVER, x, y)



    def fillUnmarkedNeighbors(self, x, y):
        # Will append VALID tiles around a tile with a '0' label
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                newX = x + dx
                newY = y + dy
                if self.isValidCoor(newX, newY) \
                and (newX, newY) not in self.unmarkedNeighbors \
                and (newX, newY) not in self.marked:
                    self.unmarkedNeighbors.add((newX, newY))
    
    def isValidCoor(self, x, y):
        if x < 0 or x >= self.rowDimension:
            return False
        if y < 0 or y >= self.colDimension:
            return False
        return True


    def mark(self, x, y):
        self.lastX = x
        self.lastY = y
        self.unmarked.discard((x, y))
        self.marked.add((x, y))
        

        ########################################################################
        #							YOUR CODE ENDS							   #
        ###################### #################################################
