from __future__ import annotations
#import numpy
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

    _sensor_accuracy = .85
    """
                          W N E S
    """
    _transition_matrix = [[0,0,0,0],
                          [0,.1,.1,.1],
                          [0,0,0,0],
                          [0,0,0,0]]

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
    """
    Filtering will not be called directly, but it can be if needed. Filtering will vary whether the state is moving or sensing
    """
    def filtering(self):
        self._state.filtering(self.my_map)
    
    def show(self):
        rows = ['[' + ','.join(map(lambda x: '{0:.2f}'.format(x),r)) + ']' for r in self._my_map]
        print('[' + ',\n '.join(rows) + ']')


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
    def sensing(self, map, sense) -> None:
        q = map
        s = 0.0
        for i in range(len(map)):
            for j in range(len(map[i])):
                update = (sense == map[i][j]) #this is never true, so it never updates?
                if(map[i][j] != -1): #add a check here with W,E,N,S in map and if we sense it, multiply it?
                    map[i][j] += map[i][j] * (update * self.context._sensor_accuracy) #+ (1-update)*(1-self.context._sensor_accuracy))
                    s += map[i][j]

        # normalize
        for i in range(len(q)):
            for j in range(len(map[0])):
                if(map[i][j] > 0):
                    map[i][j] /= s
       # print("Sensing state handles sensing.")
        print("Sensing wants to change the state of the context.")
      #print("We need to filter after sensing.")
        self.filtering(map)
        self.context._my_map = map
        self.context.change_state(MovingState())

    def filtering(self, map) -> None:
        #print("Sensing handles filtering request.")
        pass
    def moving(self, map) -> None:
        pass


class MovingState(State):
    def moving(self, map, move) -> None:
        #print("Moving state handles moving.")
        print("Moving wants to change the state of the context.")
        #print("We need to filter after moving.")
        self.filtering(map)
        self.context.change_state(SensingState())

    def filtering(self, map) -> None:
        pass
        #print("Moving state handles filtering request.")
        #self.context.transition_to(ConcreteStateA())
    def sensing(self, map) -> None:
        pass


"""
Need to add adjustments to accept the maze into the classes, the maze is our little robot's map

"""
"""
Need to add probability assignment, but where?? Does the robot do it himself? Is there another class we need?
"""

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

    WindMaze = [[3.23, 3.23, 3.23, 3.23, 3.23, 3.23, 3.23], 
            [3.23, 3.23, -1.0, -1.0, -1.0, -1.0, 3.23],
            [3.23, 3.23, -1.0, 3.23, 3.23, -1.0, 3.23],
            [3.23, -1.0, -1.0, 3.23, 3.23, -1.0, 3.23],
            [3.23, 3.23, 3.23, 3.23, -1.0, -1.0, 3.23],
            [3.23, 3.23, 3.23, 3.23, 3.23, 3.23, 3.23]]
    context = Robot(SensingState(), WindMaze)
    context.sensing(sense[1])
    context.show()
    context.moving(movements)
#print (WindMaze)