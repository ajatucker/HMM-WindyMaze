from __future__ import annotations
from operator import index
import itertools
from array import*
from abc import ABC, abstractmethod
#use this for math helps reduce the amount of code.

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
        self._my_map = map
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
        self._state.sensing(self._my_map, senses)
    """
    Moving calls moving class
    """
    def moving(self, moves):
        self._state.moving(self._my_map, moves)
    
    def filtering(self):
        self._state.filtering(self._my_map)
    
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
        length = len(map)
        width = len(map[0])
        for i in range(len(map)):
            for j in range(len(map[0])):
                if map[i][j] !=-1:
                    if move == "N":
                        if j-1 < 0 or (j-1 < width and map[i][j-1] == -1.00):
                            map[i][j] += (.1*map[i][j])
                        else:
                             map[i][j] += (.1*map[i][j])
                        if i - 1 > 0 or (i-1 < length and map[i-1][j] != -1.00):
                             map[i][j] += (.8*map[i][j])
                        else:
                            map[i][j] += (.1*map[i][j])
                        if j+1 >= len(map[0]) or(j+1 < width and map[i][j+1] == -1.00):
                             map[i][j] += (.1*map[i][j])
                        else:
                            map[i][j] += (.1*map[i][j])
                        
                        if i+1 < length or (i+1 < length and map[i+1][j] != -1.00):
                            pass #map[i][j] = (.8*map[i][j])
                        elif i+1 >= length or (i+1 < length and map[i+1][j] == -1.00):
                           pass# map[i][j] = (.1*map[i][j])
                            
                    #WE GO EAST        
                    elif move == "E":
                        if j-1 < 0 or map[i][j] == -1:
                            map[i][j] = (.1*map[i][j])
                        if i - 1 < 0 or map[i-1][j] == -1:
                            map[i][j] = (.8*map[i][j])
                        else:
                            map[i][j] = (.8*map[i][j+1])
                        if i+1 >= length or map[i+1][j] == -1:
                            map[i][j] = (.1*map[i][j])
                        else:
                            map[i][j] = (.1*map[i+1][j])
                        if j+1 >= len(map[0]) or map[i][j+1] == -1:
                            pass
                        else:
                            map[i][j] = (.8*map[i][j+1])

        self.context._my_map = map                      
        self.context.change_state(SensingState())



    def filtering(self, indexI, indexJ, map, move) -> None:
        checkNum = map[indexI][indexJ]
        length = len(map)
        width = len(map[0])
        addNum = 0
        #WE GO NORTH LETS GO
        if move == "N":
            if indexJ-1 < 0 or (indexJ-1 < width and map[indexI][indexJ-1] == -1.00):
                pass#map[i][j] += (.1*map[i][j])
            else:
                addNum += (.1*checkNum)
            if indexI - 1 < 0 or (indexI-1 < length and map[indexI-1][indexJ] == -1.00):
                pass#map[i][j] = (.8*map[i][j])
            if indexJ+1 >= len(map[0]) or(j+1 < width and map[indexI][indexJ+1] == -1.00):
                addNum += (.1*checkNum)
            else:
               addNum += (.1*checkNum)#map[i][j] += (.1*map[i][j+1])
                        
            if indexI+1 >= 6:
                pass
            elif indexI+1 >= 6 or (i < length and map[indexI+1][indexJ] == -1.00):
                addNum += (.8*checkNum)
                            
                    #WE GO EAST        
        elif move == "E":
            if indexJ-1 < 0 or map[indexI][indexJ-1] == -1:
                map[indexI][indexJ] = (.1*map[indexI][indexJ])
            if indexI - 1 < 0 or map[indexI-1][indexJ] == -1:
                map[indexI][indexJ] = (.8*map[indexI][indexJ])
            else:
                map[indexI][indexJ] = (.8*map[indexI][indexJ])
            if indexI+1 >= length or map[indexI+1][indexJ] == -1:
                map[indexI][indexJ] = (.1*map[indexI][indexJ])
            else:
                map[indexI][indexJ] = (.1*map[indexI+1][indexJ])
            if indexJ+1 >= len(map[0]) or map[indexI][indexJ+1] == -1:
                pass
            else:
                map[indexI][indexJ] = (.8*map[indexI][indexJ])            
        
        checknum = addNum /(addNum + checkNum)
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
    context.printMatrix()
    context.sensing(sense[0])
    context.printMatrix()
    context.moving(movements[0])
    context.printMatrix()

