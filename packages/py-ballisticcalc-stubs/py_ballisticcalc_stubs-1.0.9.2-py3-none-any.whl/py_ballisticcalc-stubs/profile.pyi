

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

from typing import Dict


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
    def altitude(self) -> Distance: # real signature unknown
        pass

    def bc_value(self) -> float: # real signature unknown
        pass

    def bullet_diameter(self) -> Distance: # real signature unknown
        pass

    def bullet_length(self) -> Distance: # real signature unknown
        pass

    def bullet_weight(self) -> Weight: # real signature unknown
        pass

    def calculate_drag_table(self) -> list: # real signature unknown
        pass

    def calculate_trajectory(self) -> list: # real signature unknown
        pass

    def custom_drag_function(self) -> list: # real signature unknown
        pass

    def dict(self) -> Dict: # real signature unknown
        pass

    def distance_step(self) -> Distance: # real signature unknown
        pass

    def drag_table(self) -> int: # real signature unknown
        pass

    def humidity(self) -> float: # real signature unknown
        pass

    def maximum_distance(self) -> Distance: # real signature unknown
        pass

    def maximum_step_size(self) -> Distance: # real signature unknown
        pass

    def muzzle_velocity(self) -> Velocity: # real signature unknown
        pass

    def pressure(self) -> Pressure: # real signature unknown
        pass

    def set_altitude(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_bc_value(self, value: float) -> None: # real signature unknown
        pass

    def set_bullet_diameter(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_bullet_length(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_bullet_weight(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_custom_drag_function(self, data: list[Dict[str, float]]) -> None: # real signature unknown
        pass

    def set_distance_step(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_drag_table(self, drag_table: int) -> None: # real signature unknown
        pass

    def set_humidity(self, value: float) -> None: # real signature unknown
        pass

    def set_maximum_distance(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_maximum_step_size(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_muzzle_velocity(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_pressure(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_sight_angle(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_sight_height(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_temperature(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_twist(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_twist_direction(self, direction: int) -> None: # real signature unknown
        pass

    def set_wind_direction(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_wind_velocity(self, value: float, units: int) -> None: # real signature unknown
        pass

    def set_zero_distance(self, value: float, units: int) -> None: # real signature unknown
        pass

    def sight_angle(self) -> Angular: # real signature unknown
        pass

    def sight_height(self) -> Distance: # real signature unknown
        pass

    def temperature(self) -> Temperature: # real signature unknown
        pass

    def twist(self) -> Distance: # real signature unknown
        pass

    def twist_direction(self) -> int: # real signature unknown
        pass

    def wind_direction(self) -> Angular: # real signature unknown
        pass

    def wind_velocity(self) -> Velocity: # real signature unknown
        pass

    def zero_distance(self) -> Distance: # real signature unknown
        pass

    def __init__(self,
                 bc_value: float = 0.223,
                 drag_table: int = DragTableG7,
                 bullet_diameter: (float, int) = (0.308, DistanceInch),
                 bullet_length: (float, int) = (1.2, DistanceInch),
                 bullet_weight: (float, int) = (167, WeightGrain),
                 muzzle_velocity: (float, int) = (800, VelocityMPS),
                 altitude: (float, int) = (0, DistanceMeter),
                 pressure: (float, int) = (760, PressureMmHg),
                 temperature: (float, int) = (15, TemperatureCelsius),
                 humidity: float = 0.5,
                 zero_distance: (float, int) = (100, DistanceMeter),
                 twist: (float, int) = (11, DistanceInch),
                 twist_direction: int = TwistRight,
                 sight_height: (float, int) = (90, DistanceMillimeter),
                 sight_angle: (float, int) = (0, AngularMOA),
                 maximum_distance: (float, int) = (1001, DistanceMeter),
                 distance_step: (float, int) = (100, DistanceMeter),
                 wind_velocity: (float, int) = (0, VelocityKMH),
                 wind_direction: (float, int) = (0, AngularDegree),
                 maximum_step_size: (float, int) = (1, DistanceFoot),
                 shot_angle: (float, int) = (0, AngularRadian),
                 cant_angle: (float, int) = (0, AngularRadian),
                 custom_drag_function=None,
                 multiple_bc_table=None
                 ): # real signature unknown
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

