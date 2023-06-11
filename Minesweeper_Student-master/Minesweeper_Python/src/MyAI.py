from AI import AI
from Action import Action
import copy



class MyAI( AI ):
        def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
            self.x, self.y = startX, startY
            self.totalMines = totalMines
            self.rowDimension = rowDimension
            self.colDimension = colDimension
            
            # This list store the border tiles
            self.borderTiles = []
            
            #Stores only unmarked border tiles
            self.unmarkedBorderTiles = []
            
            # Stores only the marked border tiles
            self.markedBorderTiles = []
            
            
            # Stores tiles to perform action on immedietly
            self.checkNow = []
            
            # Once checkNow is empty, then check this list
            self.checkAfter = []
            
            # Stores bomb tiles to flag
            self.bombs = []
            
            # Store safe tiles to uncover
            self.safes = []
            
            # Used for retrieving last safe tiles after all mines are flagged
            self.endTiles = []
            
            # 2-d array that stores the entire board, ' ' for empty tiles, -1 for mines, and 0-9 for labels
            self.board = [['_' for _ in range(self.rowDimension)] for _ in range(self.colDimension)]
            
            # Tracks the amount of mines
            self.mineCount = totalMines
            
        def getAction(self, number: int) -> "Action Object":
                #self.printBoard()
                #print()
                self.board[self.x][self.y] = number
                
                ##############################
                if self.mineCount == 0:
                    # The board has no more mines
                    if not self.endTiles:
                        self.endTiles.extend(self.getTotalUnmarkedTiles())
                        
                    if not self.endTiles:
                        # No more end tiles
                        return Action(AI.Action.LEAVE)
                    else:
                        # Still more end tiles to uncover
                        self.x, self.y = self.endTiles.pop(0)
                        return Action(AI.Action.UNCOVER, self.x, self.y)
                ##############################
                
                unmarkedNeighbors = self.getNeighborsUnmarked(self.x, self.y)

                if unmarkedNeighbors:
                    #Not empty
                    currTile = self.board[self.x][self.y]
                    
                    if currTile == 0:  # If number is 0, then all neighboring mines are safe
                        for t in unmarkedNeighbors:
                            if t not in self.safes and t not in self.checkNow:
                                self.safes.append(t)
                    elif currTile != -1:
                        for t in unmarkedNeighbors:
                            currPos = (self.x, self.y)
                            if currPos not in self.checkNow and currPos not in self.checkAfter:
                                self.checkNow.append(currPos)
                    else:
                        ## TODO append to bomb list?
                        pass
                
                if self.safes:
                    return self.returnUncover()
                
                if self.bombs:
                    return self.returnFlag()
                score = 8
                cont = 0
                for _ in range(20):  # Maybe change to 40
                    if not self.checkNow:
                        break
                    pos = self.checkNow.pop(0)
                    
                    if self.board[pos[0]][pos[1]] != -1:
                        numBombs = self.getNumBombs(pos[0], pos[1])
                        if numBombs == 0 or len(self.getNeighborsUnmarked(pos[0], pos[1])) == numBombs:
                            # is known
                            unmarkedNeighbors = self.getNeighborsUnmarked(pos[0], pos[1])
                            
                            if numBombs > 0:
                                for neighbor in unmarkedNeighbors:
                                    if neighbor not in self.bombs:
                                        self.bombs.append(neighbor)
                            elif numBombs == 0:
                                for neighbor in unmarkedNeighbors:
                                    if neighbor not in self.safes:
                                        self.safes.append(neighbor)
                            if self.bombs or self.safes:
                                self.checkNow.extend(self.checkAfter)
                                self.checkNow.append(pos)
                                self.checkAfter.clear() # we don't need this anymore
                                
                            if self.safes:
                                return self.returnUncover()
                            
                            if self.bombs:
                                return self.returnFlag()
                            
                            
                        else:
                            # Not known
                            if pos not in self.checkAfter:
                                self.checkAfter.append(pos)
                            pass
                for i in self.checkNow:
                    if i not in self.checkAfter:
                        self.checkAfter.append(i)
                
                self.checkNow = []
                self.checkNow = copy.deepcopy(self.checkAfter)
                self.checkAfter = []
                if self.safes:
                    return self.returnUncover()
                
                if self.bombs:
                    return self.returnFlag()        
                
                
                possible = []
                for x in range(len(self.board)):
                        for y in range(len(self.board[x])):
                                if self.board[x][y] == -2:
                                        possible.append((x,y))

                if len(possible) == self.mineCount:
                        for f in possible:
                                self.bombs.append(f)
                        if self.safes:
                            return self.returnUncover()
                        
                        if self.bombs:
                            return self.returnFlag()  
                score2 = (self.x, self.y)
                scoreFinal = score2
                prob = 1
                for i in self.checkNow:
                        s1 = self.getNumBombs(i[0], i[1]) 
                        p = len(self.getNeighborsUnmarked(i[0], i[1]))
                        if p == 0:
                                continue
                        if prob > float(s1/p):
                                prob = float(s1/p)
                                score2 = (i[0], i[1])


                for i in self.getNeighborsUnmarked(score2[0], score2[1]):
                        if score > len(self.getNeighborsMarked(i[0], i[1])):
                                score = len(self.getNeighborsMarked(i[0], i[1]))
                                scoreFinal = i

                self.x, self.y = scoreFinal
                return Action(AI.Action.UNCOVER, self.x, self.y)
         
        def isValidCoor(self, x, y):
                if x < 0 or x >= self.colDimension:
                        return False
                if y < 0 or y >= self.rowDimension:
                        return False
                return True

        def getTotalUnmarkedTiles(self):
            result = []
            for x in range(len(self.board)):
                for y in range(len(self.board[x])):
                    if self.board[x][y] == '_':
                        result.append((x, y))
            return result


        def getNeighbors(self, x, y):
            result = []
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    newX = x + dx
                    newY = y + dy
                    if self.isValidCoor(newX, newY):
                        result.append((newX, newY))
            return result
                    
                    
        def getNeighborsUnmarked(self, x, y):
            #intersection function
            list1 = self.getTotalUnmarkedTiles()
            list2 = self.getNeighbors(x, y)
            
            result = []
            for item in list1:
                if item in list2 and item not in result:
                    result.append(item)
            
            return result
    
        def getNeighborsMarked(self, x, y):
            result = []
            neighbors = self.getNeighbors(x, y)
            for n in neighbors:
                if self.board[n[0]][n[1]] != '_':
                    result.append((n[0], n[1]))
            return result
    
        def returnUncover(self):
            self.x, self.y = self.safes.pop(0) # Pop the first element
            return Action(AI.Action.UNCOVER, self.x, self.y)

        def returnFlag(self):
            self.x, self.y = self.bombs.pop(0) # Pop the first element
            self.mineCount -= 1
            return Action(AI.Action.FLAG, self.x, self.y)

        def getNumBombs(self, x, y):
            result = self.board[x][y]
            markedNeighbors = self.getNeighborsMarked(x, y)
            if markedNeighbors:
                for i in markedNeighbors:
                    if self.board[i[0]][i[1]] == -1:
                        result = result - 1
            
            return result
        
        
        def printBoard(self):
            for sub in self.board:
                for i in sub:
                    print('', i, end='')
                print()