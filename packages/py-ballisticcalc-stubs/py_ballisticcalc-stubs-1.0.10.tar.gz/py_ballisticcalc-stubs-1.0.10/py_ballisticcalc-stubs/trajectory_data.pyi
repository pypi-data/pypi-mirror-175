

# imports
import builtins as __builtins__ # <module 'builtins' (built-in)>
import py_ballisticcalc.bmath.unit.weight as weight
import py_ballisticcalc.bmath.unit.velocity as velocity
import py_ballisticcalc.bmath.unit.temperature as temperature
import py_ballisticcalc.bmath.unit.pressure as pressure
import py_ballisticcalc.bmath.unit.energy as energy
import py_ballisticcalc.bmath.unit.distance as distance
import py_ballisticcalc.bmath.unit.angular as angular
from py_ballisticcalc.bmath.unit.angular import Angular

from py_ballisticcalc.bmath.unit.distance import Distance

from py_ballisticcalc.bmath.unit.energy import Energy

from py_ballisticcalc.bmath.unit.pressure import Pressure

from py_ballisticcalc.bmath.unit.temperature import Temperature

from py_ballisticcalc.bmath.unit.velocity import Velocity

from py_ballisticcalc.bmath.unit.weight import Weight


# Variables with simple values

AngularCmPer100M = 7
AngularDegree = 1
AngularInchesPer100Yd = 6
AngularMil = 3
AngularMOA = 2
AngularMRad = 4
AngularRadian = 0
AngularThousand = 5

DistanceCentimeter = 16
DistanceFoot = 11
DistanceInch = 10
DistanceKilometer = 18
DistanceLine = 19
DistanceMeter = 17
DistanceMile = 13
DistanceMillimeter = 15
DistanceNauticalMile = 14
DistanceYard = 12

EnergyFootPound = 30
EnergyJoule = 31

PressureBar = 42
PressureHP = 43
PressureInHg = 41
PressureMmHg = 40
PressurePSI = 44

TemperatureCelsius = 51
TemperatureFahrenheit = 50
TemperatureKelvin = 52
TemperatureRankin = 53

VelocityFPS = 62
VelocityKMH = 61
VelocityKT = 64
VelocityMPH = 63
VelocityMPS = 60

WeightGrain = 70
WeightGram = 72
WeightKilogram = 74
WeightNewton = 75
WeightOunce = 71
WeightPound = 73

# functions

def __pyx_unpickle_Timespan(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_TrajectoryData(*args, **kwargs): # real signature unknown
    pass

# classes

class Timespan(object):
    # no doc
    def minutes(self) -> float: # real signature unknown
        pass

    def seconds(self) -> float: # real signature unknown
        pass

    def total_seconds(self) -> float: # real signature unknown
        pass

    def __init__(self, time: float): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(*args, **kwargs): # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    def __reduce_cython__(self, *args, **kwargs): # real signature unknown
        pass

    def __reduce__(self, *args, **kwargs): # real signature unknown
        pass

    def __setstate_cython__(self, *args, **kwargs): # real signature unknown
        pass

    def __setstate__(self, *args, **kwargs): # real signature unknown
        pass

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x000001B8FE394810>'


class TrajectoryData(object):
    # no doc
    def drop(self) -> Distance: # real signature unknown
        pass

    def drop_adjustment(self) -> [Angular, None]: # real signature unknown
        pass

    def energy(self) -> Energy: # real signature unknown
        pass

    def mach_velocity(self) -> float: # real signature unknown
        pass

    def optimal_game_weight(self) -> Weight: # real signature unknown
        pass

    def time(self) -> Timespan: # real signature unknown
        pass

    def travelled_distance(self) -> Distance: # real signature unknown
        pass

    def velocity(self) -> Velocity: # real signature unknown
        pass

    def windage(self) -> Distance: # real signature unknown
        pass

    def windage_adjustment(self) -> [Angular, None]: # real signature unknown
        pass

    def __init__(self, time: Timespan,
                 travel_distance: Distance,
                 velocity: Velocity,
                 mach: float,
                 drop: Distance,
                 drop_adjustment: [Angular, None],
                 windage: Distance,
                 windage_adjustment: [Angular, None],
                 energy: Energy,
                 optimal_game_weight: Weight): # real signature unknown
        pass

    @staticmethod # known case of __new__
    def __new__(*args, **kwargs): # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    def __reduce_cython__(self, *args, **kwargs): # real signature unknown
        pass

    def __reduce__(self, *args, **kwargs): # real signature unknown
        pass

    def __setstate_cython__(self, *args, **kwargs): # real signature unknown
        pass

    def __setstate__(self, *args, **kwargs): # real signature unknown
        pass

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x000001B8FE3947B0>'


# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x000001B8FCB79F50>'

__spec__ = None # (!) real value is "ModuleSpec(name='py_ballisticcalc.trajectory_data', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x000001B8FCB79F50>, origin='C:\\\\Users\\\\Sergey\\\\PycharmProjects\\\\archer_ballistics_constructor\\\\venv11\\\\Lib\\\\site-packages\\\\py_ballisticcalc\\\\trajectory_data.cp311-win_amd64.pyd')"

__test__ = {}

