from __future__ import annotations
from operator import index
import numpy as np
import itertools
from array import*
from abc import ABC, abstractmethod
#use this for math helps reduce the amount of code.
import matplotlib.pyplot as plt

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
    
    def show(self):
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
        total = 0
        for i in range(len(map)):
            for j in range(len(map[i])):
                if(map[i][j] != -1): 
                    update = self.filtering(i, j, map, sense) #filtering creates a multiplier for each spot
                    map[i][j] = map[i][j] * (update) * 1000#
                    total += map[i][j]
                    
        print("Sensing wants to change the state of the context.")
        self.context._my_map = map
        self.context.change_state(MovingState())
        
    #def filtering(self,_moving_matrix):
     #   new_state = np.dot(_moving_matrix,np.dot(self.WindMaze,self.current_state))
      #  new_state_normalized = new_state/np.sum(new_state)
       # self.current_state = new_state_normalized
        #return new_state_normalized
    
    def filtering(self, indexI, indexJ, map, dir) -> None:
        checkNum = 1
        if(checkNum > -1):
            print(checkNum)
            length = len(map)
            width = len(map[indexI])
            #mult = np.multiply(self._sensing_matrix, dir)
            #print(mult)
            if dir == ([1,0,0,0]): #W
                pass
                #need to look west
            elif (dir == ([0,1,0,0])): #N
                pass
                 #need to look north
            elif(dir == [0,0,1,0]): #E
                pass
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
                     checkNum = checkNum * 85/100 #misses an obstacle/barrier
                     print("miss barrier ", checkNum)
                else:
                    checkNum = checkNum * 1/10 #know its an obstacle
                
                if(indexJ+1 >= width or (indexJ+1 < width and map[indexI][indexJ+1] == -1.00)):
                     checkNum = checkNum * 15/100 #mistakes an open square for obstacle
                     print("find barrier ", checkNum)
                else:
                    checkNum = checkNum * 90/100 #know its an obstacle
            
            print(checkNum)
                 #need to look south
            return checkNum
        #print("Sensing handles filtering request.")
        
    def moving(self, map) -> None:
        pass


class MovingState(State):
       
    """
                       W   N   E   S    
    """
    _moving_matrix =[[.8, .1,  0, .1],  #W
                     [.1, .8, .1,  0],  #N
                     [ 0, .1, .8, .1],  #E
                     [.1,  0, .1, .8]]  #S

    def moving(self, map, move) -> None:
        #print("We need to filter after moving.")
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
    movements = [[0,1,0,0],[0,0,1,0],[0,0,1,0]]

    sense = [[0, 0, 0, 1],[0, 1, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0]]

    WindMaze = np.array =  [[1.0/31, 1.0/31, 1/31, 1/31, 1/31, 1/31, 1/31], 
                            [1/31, 1/31, -1.0, -1.0, -1.0, -1.0, 1/31],
                            [1/31, 1/31, -1.0, 1/31, 1/31, -1.0, 1/31],
                            [1/31, -1.0, -1.0, 1/31, 1/31, -1.0, 1/31],
                            [1/31, 1/31, 1/31, 1/31, -1.0, -1.0, 1/31],
                            [1/31, 1/31, 1/31, 1/31, 1/31, 1/31, 1/31]]
    context = Robot(SensingState(), WindMaze)
    context.sensing(sense[0])
    context.show()
    #context.moving(movements[0])
    #context.show()
#print (WindMaze)