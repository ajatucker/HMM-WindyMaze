from __future__ import annotations
#import numpy
import itertools
from array import*
from abc import ABC, abstractmethod

class Robot:
    """
   This is the robot's context
    """

    _state = None
    """
    A reference to the current state of the Context.
    """

    def __init__(self, state: State) -> None:
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

    def sensing(self):
        self._state.sensing()
    """
    Moving calls moving class
    """
    def moving(self):
        self._state.moving()
    """
    Filtering will not be called directly, but it can be if needed. Filtering will vary whether the state is moving or sensing
    """
    def filtering(self):
        self._state.filtering()


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
    def sensing(self) -> None:
        pass
    @abstractmethod
    def filtering(self) -> None:
        pass
    @abstractmethod
    def moving(self) -> None:
        pass


class SensingState(State):
    def sensing(self) -> None:
        print("Sensing state handles sensing.")
        print("Sensing wants to change the state of the context.")
        print("We need to filter after sensing.")
        self.context.filtering()
        self.context.change_state(MovingState())

    def filtering(self) -> None:
        print("Sensing handles filtering request.")
    def moving(self) -> None:
        pass


class MovingState(State):
    def moving(self) -> None:
        print("Moving state handles moving.")
        print("Moving wants to change the state of the context.")
        print("We need to filter after moving.")
        self.context.filtering()
        self.context.change_state(SensingState())

    def filtering(self) -> None:
        print("Moving state handles filtering request.")
        #self.context.transition_to(ConcreteStateA())
    def sensing(self) -> None:
        pass


"""
Need to add adjustments to accept the maze into the classes, the maze is our little robot's map

"""

if __name__ == "__main__":
    # The client code.

    context = Robot(SensingState())
    context.sensing()
    context.moving()
    """
    Need to add while loop that loops the changing state context until we see a value of 98% or so given the test he gave us to go off of
    """
    #test git#

WindMaze = [[3.23, 3.23, 3.23, 3.23, 3.23, 3.23, 3.23], 
            [3.23, 3.23, -1.0, -1.0, -1.0, -1.0, 3.23],
            [3.23, 3.23, -1.0, 3.23, 3.23, -1.0, 3.23],
            [3.23, -1.0, -1.0, 3.23, 3.23, -1.0, 3.23],
            [3.23, 3.23, 3.23, 3.23, -1.0, -1.0, 3.23],
            [3.23, 3.23, 3.23, 3.23, 3.23, 3.23, 3.23]]

#print (WindMaze)