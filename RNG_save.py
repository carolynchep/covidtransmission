from enum import Enum
import random
from numpy.random import MT19937, Generator
import numpy.typing

#############################################################################
from typing import List
import numpy as np



class Stream(Enum):
    ''' enumeration to identify different streams (one per stochastic component
        in the model) for the random number generator
    '''
    ARRIVAL    = 0
    TIME_PER_TASK = 1
    TASKS = 2

######################################################################
class RNG:
    ''' This class implements a wrapper around numpy's MT19937 generator
        to allow for a "streams" implementation, i.e., where we can have a
        different stream of random numbers for each different stochastic
        component.  The stream will be indicated using one of the values
        defined in the Stream enumeration class.  Each wrapper method will do
        the right thing to pull and then update the state of the particular
        stream.
    '''

    # class-level variables
    _seed: numpy.int64 = None
    _streams: List[numpy.random.Generator] = []
    _initialized: bool = False

    ############################################################################
    @classmethod
    def setSeed(cls, seed: numpy.int64) -> None:
        cls._seed = seed
        cls.initializeStreams()

    ############################################################################
    @classmethod
    def initializeStreams(cls) -> None:
        ''' Class-level method to initialize streams for generating random
            numbers.  This uses the .jumped() method to set up the streams
            sufficiently far apart, giving us one stream per stochastic
            component (i.e., number of entries in the Stream enum).

            See:
                https://bit.ly/numpy_random_jumping
                https://bit.ly/numpy_random_Generator
        '''
        cls._streams = []
        rng = MT19937(cls._seed)  # construct a Mersenne Twister with appropriate seed
        for i in range(len(Stream)):
            cls._streams.append(Generator(rng.jumped(i)))
        cls._initialized = True

    ############################################################################
    @classmethod
    def geometric(cls, p: float, which_stream: Stream) -> numpy.int64:
        ''' class-level method to generate integer values drawn from a geometric(p)
            distribution, where p corresponds the probability of success on an
            individual trial (see numpy.Generator.geometric)
        Parameters:
            p: floating-point probability of success on any single trial
            which_stream: named entry from Stream class
        Returns:
            a geometric(p) distributed integer value, corresponding to the
            number of failures before the first success
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        # according to the API for numpy.Generator.geometric, it models the
        # number of _trials_ until the first success, rather than the number of
        # _failures_ before the first success as R does... so we subtract 1
        #     https://bit.ly/numpy_Generator_geometric
        #     https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Geometric.html
        #
        #return generator.geometric(p)
        return generator.geometric(p) - 1  # see comment above
    ############################################################################
    @classmethod
    def uniform(cls, a: float, b: float, which_stream: Stream) -> numpy.float64:
        ''' class-level method to generate integer values drawn from a uniform(a, b)
            distribution
        Parameters:
            a: float - lower bound
            b: float - upper bound
            which_stream: named entry from Stream class
        Returns:
            a uniform(a,b) distributed float value
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]
        return generator.uniform(a, b)
    ############################################################################
    @classmethod
    def exponential(cls, mu: float, which_stream: Stream) -> numpy.float64:
        ''' class-level method to generate integer values drawn from a exponential(mu)
            distribution
        Parameters:
            mu: float - rate
            which_stream: named entry from Stream class
        Returns:
            an exponential(mu) distributed float value
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]
        return generator.exponential()
    ############################################################################
    @classmethod
    def gamma(cls, shape: float, scale: float, which_stream: Stream) -> numpy.float64:
        ''' class-level method to generate integer values drawn from a gamma(shape, scale)
            distribution

        Parameters:
            shape: float - number of events modeling
            scale: float - mean time between events
            which_stream: named entry from Stream class
        Returns:
            a gamma(shape, scale) distributed float value
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]
        return generator.gamma(shape, scale)
    ############################################################################
    @classmethod
    def random(cls, which_stream: Stream) -> numpy.float64:
        ''' class-level method to generate integer values drawn from a random()
            distribution
        Parameters:
            which_stream: named entry from Stream class
        Returns:
            a random() distributed integer value
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]
        return generator.random()
    ############################################################################
    @classmethod
    def randint(cls, a: int, b:int, which_stream: Stream) -> numpy.int64:
        ''' class-level method to generate integer values drawn from a randint(a,b), where a corresponds
            to the lower bound value and b correponds to upper bound value
        Parameters:
            a: int - lower bound value
            b: int - upper bound value
            which_stream: named entry from Stream class
        Returns:
            a randomint(a,b) integer value
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]
        return random.randint(a, b)



def main() -> None:
    for i in range(10000):
        print(RNG.uniform(0.1, 0.3, Stream.TIME_PER_TASK))

if __name__ == "__main__":
    main()
