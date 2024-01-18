from room import *
from enum import Enum
from RNG_save import RNG
from RNG_save import Stream
import random
import time

from termcolor import colored as clr
class Stats:
    VACCINATED_INFECTION = 0
    NOT_VACCINATED_INFECTION = 0
    NEWLYINFECTED = 0
    STARTING_INFECTIONS = 0

class Type(Enum):
    NOT_INFECTED_AND_NOT_VACCINATED = 0
    INFECTED = 1
    NOT_INFECTED_AND_VACCINATED = 2

class Person:
    ''' class to represent a person in the simulation, whether a
        vaccinated, unvaccinated, or infected student
    '''
    __slots__ = ("_id", "_type", "_loc", "_vision", "_time_infection")

    # class-level variable
    count = 0
    str_length = None  # initialized in simulation.py

    def __init__(self, prop_infected: float, prop_v_and_not_i: float) -> None:
        ''' initializer for a Person object
        Parameters:
            prop_infected: proportion of infected
            prop_v_and_not_i: proportion of vaccinated and not infected
        '''
        self._id    : int  = Person.count
        Person.count += 1
        #generates a percentage of vaccinated, unvaccinated, and infected students
        self._type  : Type = Type(random.choices([0,1,2], weights = [1-(prop_infected+prop_v_and_not_i), prop_infected, prop_v_and_not_i], k = 1)[0])
        self._vision: int  = 1   # could be random!
        self._time_infection: float = 0

        # when person arrives, they appear in the Room' entry location
        Room.arrival(self)  # sets this Person's _loc

    ''' simple getter methods '''
    def row(self)    -> int: return self._loc.row()
    def col(self)    -> int: return self._loc.col()
    def vision(self) -> int: return self._vision

    def __str__(self) -> str:
        unicode = True
        if unicode:
            if self._type is Type.NOT_INFECTED_AND_NOT_VACCINATED:
                value = "😐" #unvaccinated
            if self._type is Type.INFECTED:
                value = "🤢" #infected
            if self._type is Type.NOT_INFECTED_AND_VACCINATED:
                value = "😷" #vaccinated
        else:
            ''' returns str representation of a Person object '''
            id_ = f"{self._id:>{Person.str_length}d}"
            if self._type is Type.BUTTERFLY:
                value = clr(f"B{id_}", "green", attrs = ["bold"])
            else:
                value = clr(f"W{id_}", "red")
        return value

    def setLocation(self, location: None) -> None:
        ''' setter method to update the (new) location of this Person,
            called from methods in room.py
        Parameters:
            location: a Location object, if occupying, or None, if leaving
        '''
        self._loc = location

    def move(self, debug: bool = False) -> None:
        ''' Method to handle a Person moving within the room.  The Person
            should use Room.getNeighborhood (which is based on the Person's
            vision) to have a valid list of currently-unoccupied locations.
            The Person should then use Room.getNeighborCount using each of
            those locations, and:
                - if a butterfly, choose the currently-unoccupied location
                  having the highest neighbor count (ties should be broken
                  at random -- i.e., select one at random from a list)
                - if a wallflower, choose the currently-unoccupied location
                  having the lower neighbor count (break ties at random)
            Relevant methods to consider:
                - Room.getNeighborhood
                - Room.getNeighborCount
                - Room.departCurrentLocation
                - Room.occupyNewLocation
        Parameters:
            debug: boolean indicating whther to print debugging info
        '''
        location_list = []
        list_of_neighbors = Room.getNeighborhood(self)
        for element in list_of_neighbors:
            if (element.row() < Room.rows and element.row() >= 0) and (element.col() < Room.cols and element.col() >= 0):
                location_list.append(element)
        new_location = location_list[random.randint(0, len(location_list)-1)]
        Room.departCurrentLocation(self)
        Room.occupyNewLocation(self, new_location.row(), new_location.col())

    def exposureStatus(self, debug = False) -> None:
        ''' Method to determine whether a student has been infected with Covid, using uniform distributions
        Parameters:
            debug: boolean indicating whther to print debugging info
        Returns:
            None
        '''
        if self._type is Type.INFECTED:
            return
        new_list = []
        probability_of_infection = 0
        list_of_neighbors = Room.getNeighbors(self)
        for element in list_of_neighbors:
            if element._type is Type.INFECTED:
                if self._type is Type.NOT_INFECTED_AND_NOT_VACCINATED:
                    probability_of_infection += RNG.uniform(0.2, 0.257, Stream.TASKS)
                if self._type is Type.NOT_INFECTED_AND_VACCINATED:
                    probability_of_infection += RNG.uniform(0.05, 0.107, Stream.TIME_PER_TASK)
        if random.choices([0, 1], weights = [1-probability_of_infection, probability_of_infection])[0]== 1:
            if self._type is Type.NOT_INFECTED_AND_VACCINATED:
                Stats.VACCINATED_INFECTION +=1
            else:
                Stats.NOT_VACCINATED_INFECTION +=1
            self._type = Type.INFECTED
            Stats.NEWLYINFECTED += 1
            self._time_infection = time.time()

    def recoveryPeriod(self, debug = False) -> None:

        if time.time() - self._time_infection >= 60:
            if random.choices([0,1], weights = [0.5, 0.5], k = 1)[0] == 1:
                self._type = Type(random.choices([0,2], weights = [0.40, 0.60], k = 1)[0])
            else:
                return
        if time.time() - self._time_infection >= 100:
            self._type = self._type = Type(random.choices([0,2], weights = [0.40, 0.60], k = 1)[0])
