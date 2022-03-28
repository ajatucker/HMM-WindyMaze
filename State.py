from __future__ import annotations
from operator import index
import numpy 
import itertools
from array import*
from abc import ABC, abstractmethod

"""
   This is the robot's context
    """
class Robot:
    """
   the state represents the robot's current state
    """
    _my_map = []

    _state = None

    def __init__(self, state: State, map) -> None:
        self.my_map = map
        self.change_state(state)
        

    def change_state(self, state: State):
        """
        Change to another state
        """
        print(f"Context: Change state to {type(state).__name__}")
        self._state = state
        self._state.context = self

    """
    Sensing calls sensing class
    """
    def sensing(self, senses):
        self._state.sensing(self.my_map, senses)
    """
    Moving calls moving class
    """
    def moving(self, moves):
        self._state.moving(self.my_map, moves)
    
    def filtering(self):
        self._state.filtering(self.my_map)
    
    def printMatrix(self):
        #print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in self._my_map]))
        rows = [' '.join(map(lambda x:'{0:.2f}'.format(x),r)) + ' ' for r in self._my_map]
        print(' ' + '\n '.join(rows) + ' ')


class State(ABC):
    """
    Abstract State class
    """

    @property
    def context(self) -> Robot:
        return self._context

    @context.setter
    def context(self, context: Robot) -> None:
        self._context = context

    @abstractmethod
    def sensing(self, map) -> None:
        pass
    @abstractmethod
    def filtering(self, map) -> None:
        pass
    @abstractmethod
    def moving(self, map) -> None:
        pass


class SensingState(State):
    """
    Sensing matrix is only available in the sensing state                    
    """
    """
                          W   N   E   S    
    """        

    def sensing(self, map, sense) -> None:
        #total = 0
        for i in range(len(map)):
            for j in range(len(map[i])):
                if(map[i][j] != -1): 
                    update = self.filtering(i, j, map, sense) #filtering creates a multiplier for each spot
                    map[i][j] = map[i][j] * (update) * 1000#
                    #total += map[i][j]
                    
        print("Sensing wants to change the state of the context.")
        self.context._my_map = map
        self.context.change_state(MovingState())
        
    
    def filtering(self, indexI, indexJ, map, dir) -> None:
        checkNum = 1
        if(checkNum > -1):
            print(checkNum)
            length = len(map)
            width = len(map[indexI])
            if dir == ([1,0,0,0]): #W
                if(indexI-1 < 0 or (indexI-1 > 0 and map[indexI-1][indexJ] == -1.00)):
                    checkNum = checkNum * 15/100 #misses an obstacle/barrier
                    print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an open square

                if(indexJ-1 < 0 or (indexJ-1 > 0 and map[indexI][indexJ-1] == -1.00)):
                     checkNum = checkNum * 85/100 
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 1/10 
                
                if(indexI+1 >= length or (indexI+1 < length and map[indexI+1][indexJ] == -1.00)):
                     checkNum = checkNum * 15/100 
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 
                
                if(indexJ+1 >= width or (indexJ+1 < width and map[indexI][indexJ+1] == -1.00)):
                     checkNum = checkNum * 15/100 
                     print("find barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 
                #need to look west
            elif (dir == ([0,1,0,0])): #N
                if(indexI-1 < 0 or (indexI-1 > 0 and map[indexI-1][indexJ] == -1.00)):
                    checkNum = checkNum * 85/100
                    print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 1/10

                if(indexJ-1 < 0 or (indexJ-1 > 0 and map[indexI][indexJ-1] == -1.00)):
                     checkNum = checkNum * 15/100 #misses an obstacle/barrier
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an open square
                
                if(indexI+1 >= length or (indexI+1 < length and map[indexI+1][indexJ] == -1.00)):
                     checkNum = checkNum * 15/100 #misses an obstacle/barrier
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an obstacle
                
                if(indexJ+1 >= width or (indexJ+1 < width and map[indexI][indexJ+1] == -1.00)):
                     checkNum = checkNum * 15/100 #know its an obstacle
                     print("find barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100
                 #need to look north
            elif(dir == [0,0,1,0]): #E
                if(indexI-1 < 0 or (indexI-1 > 0 and map[indexI-1][indexJ] == -1.00)):
                    checkNum = checkNum * 15/100 #misses an obstacle/barrier
                    print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an open square

                if(indexJ-1 < 0 or (indexJ-1 > 0 and map[indexI][indexJ-1] == -1.00)):
                     checkNum = checkNum * 15/100 #misses an obstacle/barrier
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an open square
                
                if(indexI+1 >= length or (indexI+1 < length and map[indexI+1][indexJ] == -1.00)):
                     checkNum = checkNum * 15/100 #misses an obstacle/barrier
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an obstacle
                
                if(indexJ+1 >= width or (indexJ+1 < width and map[indexI][indexJ+1] == -1.00)):
                     checkNum = checkNum * 85/100 #know its an obstacle
                     print("find barrier ", checkNum)
                else:
                    checkNum = checkNum * 1/10 
                 #need to look east
            elif(dir == [0,0,0,1]): #S
                if(indexI-1 < 0 or (indexI-1 > 0 and map[indexI-1][indexJ] == -1.00)):
                    checkNum = checkNum * 15/100 #misses an obstacle/barrier
                    print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an open square

                if(indexJ-1 < 0 or (indexJ-1 > 0 and map[indexI][indexJ-1] == -1.00)):
                     checkNum = checkNum * 15/100 #misses an obstacle/barrier
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an open square
                
                if(indexI+1 >= length or (indexI+1 < length and map[indexI+1][indexJ] == -1.00)):
                     checkNum = checkNum * 85/100 #know its an obstacle
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 1/10 
                
                if(indexJ+1 >= width or (indexJ+1 < width and map[indexI][indexJ+1] == -1.00)):
                     checkNum = checkNum * 15/100 
                     print("find barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 
            
            print(checkNum)
                 #need to look south
            return checkNum
        #print("Sensing handles filtering request.")
        
    def moving(self, map) -> None:
        pass


class MovingState(State):
    """
                       W   N   E   S    
    
    moving_matrix =[[.8, .1, .8, .1],  #W
                     [.1, .8, .1, .8],  #N
                     [.8, .1, .8, .1],  #E
                     [.1, .8, .1, .8]]  #S
    """
    def moving(self, map, move) -> None:
        chance = []
        for row in range(len(WindMaze)):
            for collum in range(len(WindMaze[0])):
                if map[row][collum] ==-1:
                    #WE GO NORTH LETS GO
                    if move == "N":
                        if collum-1 < 0 or map[row][collum] == -1:
                            chance.append(.1*map[row][collum])
                        else:
                            chance.append(.1*WindMaze[row][collum-1])
                        if row - 1 < 0 or map[row-1][collum] == -1:
                            chance.append(.8*WindMaze[row][collum])
                        else:
                            chance.append(.1*map[row][collum+1])
                        
                        if row+1 >= 6:
                            pass
                        elif map[row+1][collum] != -1:
                            chance.append(.8*WindMaze[row][collum+1])
                            
                    #WE GO EAST        
                    if move == "E":
                        if collum-1 < 0 or map[row][collum] == -1:
                            chance.append(.1*WindMaze[row][collum])
                        else:
                            chance.append(.8*WindMaze[row][collum-1])
                        if row - 1 < 0 or map[row-1][collum] == -1:
                            chance.append(.8*WindMaze[row][collum])
                        else:
                            chance.append(.8*WindMaze[row][collum+1])
                        
                        if row+1 >= 6:
                            pass
                        elif map[row+1][collum] != -1:
                            chance.append(.8*WindMaze[row][collum+1])
                            
                    #WE GOING DOWN SOUTH         
                    if move == "S":
                        if collum-1 < 0 or map[row][collum-1] == -1:
                            chance.append(.1*WindMaze[row][collum])
                        else:
                            chance.append(.1*WindMaze[row][collum-1])
                        if row - 1 < 0 or map[row-1][collum] == -1:
                            chance.append(.8*WindMaze[row][collum])
                        else:
                            chance.append(.1*WindMaze[row][collum+1])
                        
                        if row+1 >= 6:
                            pass
                        elif WindMaze[row+1][collum] != -1:
                            chance.append(.8*WindMaze[row][collum+1])
                            
                    # GOING ON WEST DOWN THE ORIGON TRAIL    
                    if move == "W":
                        if collum-1 < 0 or map[row][collum] == -1:
                            chance.append(.8*WindMaze[row][collum])
                        else:
                            chance.append(.1*WindMaze[row][collum-1])
                        if row - 1 < 0 or map[row-1][collum] == -1:
                            chance.append(.1*WindMaze[row][collum])
                        else:
                            chance.append(.1*WindMaze[row][collum+1])
                        
                        if row+1 >= 6:
                            pass
                        elif WindMaze[row+1][collum] != -1:
                            chance.append(.1*WindMaze[row][collum+1])
        
        print(chance)
        self.context._my_map = chance
        self.context.change_state(SensingState())



    def filtering(self, indexI, indexJ, map, dir) -> None:
        checkNum = 1
        print(checkNum)
        return checkNum
    def sensing(self, map) -> None:
        pass

if __name__ == "__main__":
    #main
    """
    Need to add while loop that loops the changing state context until we see a value of 98% or so given the test he gave us to go off of??
    """
    """
    Move/Sense format [W, N, E, S]
    """
    #movements = [[0,1,0,0],[0,0,1,0],[0,0,1,0]]
    movements = ["N","E","E"]
    N = [0,1,0,0]
    E = [0,0,1,0]
    S = [0,0,0,1]
    W = [1,0,0,0]

    sense = [[0, 0, 0, 1],[0, 1, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0]]

    WindMaze = array =  [[1/31, 1/31, 1/31, 1/31, 1/31, 1/31, 1/31], 
                            [1/31, 1/31, -1.0, -1.0, -1.0, -1.0, 1/31],
                            [1/31, 1/31, -1.0, 1/31, 1/31, -1.0, 1/31],
                            [1/31, -1.0, -1.0, 1/31, 1/31, -1.0, 1/31],
                            [1/31, 1/31, 1/31, 1/31, -1.0, -1.0, 1/31],
                            [1/31, 1/31, 1/31, 1/31, 1/31, 1/31, 1/31]]
    context = Robot(SensingState(), WindMaze)
    context.sensing(sense[0])
    context.printMatrix()
    context.moving(movements[0])
    context.printMatrix()

