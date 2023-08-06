# imports
import builtins as __builtins__ # <module 'builtins' (built-in)>

# functions

def __pyx_unpickle_Vector(*args, **kwargs): # real signature unknown
    pass

# classes

class Vector(object):
    # no doc
    def add(self, v2: Vector) -> Vector: # real signature unknown
        """
        Adds two vectors
        :param v2: Vector(x2, y2, z2)
        :return: sum of two vectors
        """
        pass

    def copy(self) -> Vector: # real signature unknown
        """
        Creates a copy of the vector
        :return: Vector
        """
        pass

    def magnitude(self) -> float: # real signature unknown
        """
        Returns a magnitude of the vector
        The magnitude of the vector is the length of a line that starts in point (0,0,0)
        and ends in the point set by the vector coordinates
        :return: magnitude of the vector
        """
        pass

    def multiply_by_const(self, a: float) -> Vector: # real signature unknown
        """
        Multiplies the vector by the constant
        :param a: float multiplier
        :return: Vector
        """
        pass

    def multiply_by_vector(self, v2: Vector) -> float: # real signature unknown
        """
        Returns a product of two vectors
        The product of two vectors is a sum of products of each coordinate
        :param v2: Vector(x2, y2, z2)
        :return: float
        """
        pass

    def negate(self) -> Vector: # real signature unknown
        """
        Returns a vector which is symmetrical to this vector vs (0,0,0) point
        :return: Vector
        """
        pass

    def normalize(self) -> Vector: # real signature unknown
        """
        Returns a vector of magnitude one which is collinear to this vector
        :return: Vector
        """
        pass

    def subtract(self, v2: Vector) -> Vector: # real signature unknown
        """
        Subtracts one vector from another
        :param v2: Vector(x2, y2, z2)
        :return: Vector
        """
        pass

    def x(self) -> float: # real signature unknown
        pass

    def y(self) -> float: # real signature unknown
        pass

    def z(self) -> float: # real signature unknown
        pass

    def __init__(self, x: float, y: float, z: float): # real signature unknown
        """
        Create create a vector from its coordinates
        :param x: X-coordinate
        :param y: Y-coordinate
        :param z: Z-coordinate
        """
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

    def __str__(self) -> str: # real signature unknown
        """
        Converts a vector into a string
        :return: formatted string [X, Y, Z]
        """
        pass

    __pyx_vtable__ = None # (!) real value is '<capsule object NULL at 0x0000015AE51C4930>'


# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x0000015AE39DB0D0>'

__spec__ = None # (!) real value is "ModuleSpec(name='py_ballisticcalc.bmath.vector.vector', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x0000015AE39DB0D0>, origin='C:\\\\Users\\\\Sergey\\\\PycharmProjects\\\\archer_ballistics_constructor\\\\venv11\\\\Lib\\\\site-packages\\\\py_ballisticcalc\\\\bmath\\\\vector\\\\vector.cp311-win_amd64.pyd')"

__test__ = {}

