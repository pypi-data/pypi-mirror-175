

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

from py_ballisticcalc.projectile import Ammunition


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

TwistLeft = 2
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

def __pyx_unpickle_TwistInfo(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_Weapon(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_WeaponWithTwist(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_ZeroInfo(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_ZeroInfoDef(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_ZeroInfoWithAmmo(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_ZeroInfoWithAmmoAndAtmo(*args, **kwargs): # real signature unknown
    pass

def __pyx_unpickle_ZeroInfoWithAtmosphere(*args, **kwargs): # real signature unknown
    pass

# classes

class TwistInfo(object):
    # no doc
    def direction(self) -> int: # real signature unknown
        pass

    def twist(self) -> Distance: # real signature unknown
        pass

    def __init__(self, direction: int, twist: Distance): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000022772465140>'


class Weapon(object):
    # no doc
    def click_value(self) -> Angular: # real signature unknown
        pass

    def has_twist(self) -> bool: # real signature unknown
        pass

    def set_click_value(self, click: Angular) -> None: # real signature unknown
        pass

    def sight_height(self) -> Distance: # real signature unknown
        pass

    def twist(self) -> Distance: # real signature unknown
        pass

    def zero(self) -> ZeroInfo: # real signature unknown
        pass

    def __init__(self, sight_height: Distance, zero_info: ZeroInfo,
                 has_twist_info: bool = False, twist: TwistInfo = None, click_value: Angular = None): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x00000227724651A0>'


class WeaponWithTwist(Weapon):
    # no doc
    def __init__(self, sight_height: Distance, zero_info: ZeroInfo, twist: TwistInfo): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000022772465200>'


class ZeroInfo(object):
    # no doc
    def ammunition(self) -> Ammunition: # real signature unknown
        pass

    def atmosphere(self) -> Atmosphere: # real signature unknown
        pass

    def has_ammunition(self) -> bool: # real signature unknown
        pass

    def has_atmosphere(self) -> bool: # real signature unknown
        pass

    def zero_distance(self) -> Distance: # real signature unknown
        pass

    def __init__(self, distance: Distance,
                 has_ammunition: bool = False,
                 has_atmosphere: bool = False,
                 ammunition: Ammunition = None,
                 atmosphere: Atmosphere = None): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000022772464F60>'


class ZeroInfoDef(ZeroInfo):
    # no doc
    def __init__(self, distance: Distance): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000022772464FC0>'


class ZeroInfoWithAmmo(ZeroInfo):
    # no doc
    def __init__(self, distance: Distance, ammo: Ammunition): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000022772465080>'


class ZeroInfoWithAmmoAndAtmo(ZeroInfo):
    # no doc
    def __init__(self, distance: Distance, ammo: Ammunition, atmosphere: Atmosphere): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x00000227724650E0>'


class ZeroInfoWithAtmosphere(ZeroInfo):
    # no doc
    def __init__(self, distance: Distance, atmosphere: Atmosphere): # real signature unknown
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

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000022772465020>'


# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x0000022770C79FD0>'

__spec__ = None # (!) real value is "ModuleSpec(name='py_ballisticcalc.weapon', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x0000022770C79FD0>, origin='C:\\\\Users\\\\Sergey\\\\PycharmProjects\\\\archer_ballistics_constructor\\\\venv11\\\\Lib\\\\site-packages\\\\py_ballisticcalc\\\\weapon.cp311-win_amd64.pyd')"

__test__ = {}

