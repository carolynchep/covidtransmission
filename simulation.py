from room import Room
from person import Person, Type
from calendar import Calendar
from RNG_save import RNG
from RNG_save import Stream
from person import Stats
from typing import List
import simulus
import random
import time


################################################################

class Parameters:
    ''' simple class to define simulation parameter values '''
    CLEAR_SCREEN = True
    DEBUG = False

    MAX_T = 100
    ROOM_ROWS = 20
    ROOM_COLS = 15
    MAX_PEOPLE = (ROOM_ROWS * ROOM_COLS) // 5
    PROP_INFECTED = 0.35
    PROP_VACCINATED_AND_NOT_INFECTED = 0.5 #range of vaccinated high school students

    SEED = 8675309  # or None

    PRINT_DELAY = 0.01
#################################################################

def interarrival() -> float:
    return random.expovariate(1.0)

def intermove() -> float:
    return random.uniform(0.5, 2.5)

def arrival(debug: bool = False) -> None:
    ''' function to handle an arrival of a Person to the Room
    Parameters:
        debug: if True, prints debugging information
    '''
    global num_people
    global people
    # new person shows up at the Room's entry location;
    # make sure there is no one in the entry, otherwise reject
    if not Room.isEntryOccupied():
        p = Person(Parameters.PROP_INFECTED, Parameters.PROP_VACCINATED_AND_NOT_INFECTED)
        people.append(p)
        Room.show(sim.now, clear_screen = Parameters.CLEAR_SCREEN, delay = Parameters.PRINT_DELAY)
        if debug: print(f"\t{p} arrives @ {sim.now:.3f}")
        if debug: print(f"\t{p} @ ({p.row()},{p.col()}) scheduled to move @ {sim.now:.3f}")
        # upon arrival, schedule an immediate movement for this Person
        sim.sched(move, p, Parameters.DEBUG, until = sim.now)
        num_people += 1
    else:
        print(f"\tNo arrival allowed -- entry is filled")

    # schedule the next arrival only if not at maximum Room capacity
    if num_people < Parameters.MAX_PEOPLE:
        sim.sched(arrival, Parameters.DEBUG, offset = interarrival())

    if debug: Calendar.printCalendar(sim)

def move(p: Person, debug: bool = False) -> None:
    ''' function to handle movement of a given Person
    Parameters:
        person: the Person object that is moving
        debug: if True, prints debugging information
    '''
    if p._type is Type.INFECTED:
        p.recoveryPeriod()
    p.exposureStatus()
    p.move()  # call the Person's move method
    Room.show(sim.now, clear_screen = Parameters.CLEAR_SCREEN, delay = Parameters.PRINT_DELAY)
    intermove_time = intermove()
    if debug:
        print(f"\t{p} @ ({p.row()},{p.col()}) scheduled to move @ {(sim.now + intermove_time):.3f}")
    # schedule the next movement for this Person
    sim.sched(move, p, Parameters.DEBUG, offset = intermove_time)

    if debug: Calendar.printCalendar(sim)

######################################################################
######################################################################

num_people = 0
people : List[Person] = []

Person.str_length = len(str(Parameters.ROOM_ROWS * Parameters.ROOM_COLS))
Room.createRoom(Parameters.ROOM_ROWS, Parameters.ROOM_COLS)

if Parameters.SEED is not None:
    random.seed(Parameters.SEED)

#
# create a simulator object, schedule the first arrival, and then
# kick off the simulation for the maximum simulation time
#
sim = simulus.simulator()
sim.sched(arrival, Parameters.DEBUG, offset = interarrival())
sim.run(Parameters.MAX_T)

print(f"Unvaccinated Population: {int(60*(1-(Parameters.PROP_VACCINATED_AND_NOT_INFECTED+Parameters.PROP_INFECTED)))}")
print(f"Vaccinated Population: {int(60*Parameters.PROP_VACCINATED_AND_NOT_INFECTED)}")
print(f"Initial Infections: {int(60*Parameters.PROP_INFECTED)}")
print(f"Newly Infected: {Stats.NEWLYINFECTED}")
print(f"Unvaccinated Infections: {Stats.NOT_VACCINATED_INFECTION}")
print(f"Vaccinated Infections: {Stats.VACCINATED_INFECTION}")
print(f"Percentage of New Infections among Unvaccinated Students: {round(Stats.NOT_VACCINATED_INFECTION/Stats.NEWLYINFECTED,2)*100}%")
print(f"Percentage of New Infections among Vaccinated Students: {round(Stats.VACCINATED_INFECTION/Stats.NEWLYINFECTED,2)*100}%")



def hist_newly_infected():
    newly_infected_list = []
    for i in range(Parameters.MAX_T):
        # Assuming Stats.NEWLYINFECTED is a changing value
        newly_infected_list.append(Stats.NEWLYINFECTED)
        # Optionally, update Stats.NEWLYINFECTED for the next iteration
        # Stats.NEWLYINFECTED = ... (update the value here)
    return newly_infected_list
