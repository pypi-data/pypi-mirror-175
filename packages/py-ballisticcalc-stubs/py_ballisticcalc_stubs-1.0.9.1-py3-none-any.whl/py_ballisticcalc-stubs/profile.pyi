

# imports
import builtins as __builtins__ # <module 'builtins' (built-in)>
import py_ballisticcalc.bmath.unit.weight as weight
import py_ballisticcalc.bmath.unit.velocity as velocity
import py_ballisticcalc.bmath.unit.temperature as temperature
import py_ballisticcalc.bmath.unit.pressure as pressure
import py_ballisticcalc.bmath.unit.energy as energy
import py_ballisticcalc.bmath.unit.distance as distance
import py_ballisticcalc.bmath.unit.angular as angular
from py_ballisticcalc.atmosphere import Atmosphere

from py_ballisticcalc.bmath.unit.angular import Angular

from py_ballisticcalc.bmath.unit.distance import Distance

from py_ballisticcalc.bmath.unit.energy import Energy

from py_ballisticcalc.bmath.unit.pressure import Pressure

from py_ballisticcalc.bmath.unit.temperature import Temperature

from py_ballisticcalc.bmath.unit.velocity import Velocity

from py_ballisticcalc.bmath.unit.weight import Weight

from py_ballisticcalc.drag import BallisticCoefficient

from py_ballisticcalc.multiple_bc import MultipleBallisticCoefficient

from py_ballisticcalc.projectile import Ammunition, ProjectileWithDimensions

from py_ballisticcalc.shot_parameters import ShotParametersUnlevel

from py_ballisticcalc.trajectory_calculator import TrajectoryCalculator

from py_ballisticcalc.weapon import TwistInfo, WeaponWithTwist, ZeroInfo

from py_ballisticcalc.wind import create_only_wind_info


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

DragTableG7 = 5

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

TwistRight = 1

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

def __pyx_unpickle_Profile(*args, **kwargs): # real signature unknown
    pass

# classes

class Profile(object):
    # no doc
    def altitude(self, *args, **kwargs): # real signature unknown
        pass

    def bc_value(self, *args, **kwargs): # real signature unknown
        pass

    def bullet_diameter(self, *args, **kwargs): # real signature unknown
        pass

    def bullet_length(self, *args, **kwargs): # real signature unknown
        pass

    def bullet_weight(self, *args, **kwargs): # real signature unknown
        pass

    def calculate_drag_table(self, *args, **kwargs): # real signature unknown
        pass

    def calculate_trajectory(self, *args, **kwargs): # real signature unknown
        pass

    def custom_drag_function(self, *args, **kwargs): # real signature unknown
        pass

    def dict(self, *args, **kwargs): # real signature unknown
        pass

    def distance_step(self, *args, **kwargs): # real signature unknown
        pass

    def drag_table(self, *args, **kwargs): # real signature unknown
        pass

    def humidity(self, *args, **kwargs): # real signature unknown
        pass

    def maximum_distance(self, *args, **kwargs): # real signature unknown
        pass

    def maximum_step_size(self, *args, **kwargs): # real signature unknown
        pass

    def muzzle_velocity(self, *args, **kwargs): # real signature unknown
        pass

    def pressure(self, *args, **kwargs): # real signature unknown
        pass

    def set_altitude(self, *args, **kwargs): # real signature unknown
        pass

    def set_bc_value(self, *args, **kwargs): # real signature unknown
        pass

    def set_bullet_diameter(self, *args, **kwargs): # real signature unknown
        pass

    def set_bullet_length(self, *args, **kwargs): # real signature unknown
        pass

    def set_bullet_weight(self, *args, **kwargs): # real signature unknown
        pass

    def set_custom_drag_function(self, *args, **kwargs): # real signature unknown
        pass

    def set_distance_step(self, *args, **kwargs): # real signature unknown
        pass

    def set_drag_table(self, *args, **kwargs): # real signature unknown
        pass

    def set_humidity(self, *args, **kwargs): # real signature unknown
        pass

    def set_maximum_distance(self, *args, **kwargs): # real signature unknown
        pass

    def set_maximum_step_size(self, *args, **kwargs): # real signature unknown
        pass

    def set_muzzle_velocity(self, *args, **kwargs): # real signature unknown
        pass

    def set_pressure(self, *args, **kwargs): # real signature unknown
        pass

    def set_sight_angle(self, *args, **kwargs): # real signature unknown
        pass

    def set_sight_height(self, *args, **kwargs): # real signature unknown
        pass

    def set_temperature(self, *args, **kwargs): # real signature unknown
        pass

    def set_twist(self, *args, **kwargs): # real signature unknown
        pass

    def set_twist_direction(self, *args, **kwargs): # real signature unknown
        pass

    def set_wind_direction(self, *args, **kwargs): # real signature unknown
        pass

    def set_wind_velocity(self, *args, **kwargs): # real signature unknown
        pass

    def set_zero_distance(self, *args, **kwargs): # real signature unknown
        pass

    def sight_angle(self, *args, **kwargs): # real signature unknown
        pass

    def sight_height(self, *args, **kwargs): # real signature unknown
        pass

    def temperature(self, *args, **kwargs): # real signature unknown
        pass

    def twist(self, *args, **kwargs): # real signature unknown
        pass

    def twist_direction(self, *args, **kwargs): # real signature unknown
        pass

    def wind_direction(self, *args, **kwargs): # real signature unknown
        pass

    def wind_velocity(self, *args, **kwargs): # real signature unknown
        pass

    def zero_distance(self, *args, **kwargs): # real signature unknown
        pass

    def __init__(self, *args, **kwargs): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000021CF9FB5380>'


# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x0000021CF8799F90>'

__spec__ = None # (!) real value is "ModuleSpec(name='py_ballisticcalc.profile', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x0000021CF8799F90>, origin='C:\\\\Users\\\\Sergey\\\\PycharmProjects\\\\archer_ballistics_constructor\\\\venv11\\\\Lib\\\\site-packages\\\\py_ballisticcalc\\\\profile.cp311-win_amd64.pyd')"

__test__ = {}

