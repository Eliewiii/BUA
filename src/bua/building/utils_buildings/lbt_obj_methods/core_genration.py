"""
Functions to generate cores in footprints
"""
from typing import Callable

from math import ceil

from ladybug_geometry.geometry3d.face import Face3D
from dragonfly.building import Building




def lb_footprint_to_hb_model(identifier:str,lb_face_footprint: Face3D, core_area_ratio: float, height, target_floor_height=3.0,
                             **kwargs):
    """

    """

    # Find offset_perimeter
    perimeter_offset = find_perimeter_offset_for_target_core_area_ratio(target_ratio=core_area_ratio,
                                                                        lb_face_footprint=lb_face_footprint)
    # Find floor height
    num_floor = int(height/target_floor_height)
    floor_to_floor_height = height/num_floor
    floor_to_floor_heights = [floor_to_floor_height]*num_floor

    df_building = Building.from_footprint(identifier=identifier,
                                          footprint=[lb_face_footprint],
                                          floor_to_floor_heights=floor_to_floor_heights,
                                          perimeter_offset=perimeter_offset)

    ## todo



def find_perimeter_offset_for_target_core_area_ratio(target_ratio: float,
                                                     lb_face_footprint: Face3D,
                                                     lower_bound: float = 0.1,
                                                     upper_bound: float = 50.0,
                                                     tol: float = 1e-6,
                                                     max_iter: int = 100) -> float:
    """
    Finds the perimeter offset such that the core area ratio matches the target value.

    This function uses Brent's method to find the root of:
        compute_core_area_ratio_for_offset_value(perimeter_offset, lb_face_footprint) - target_ratio = 0

    Returns 0.0 if no root is found or the target ratio is not bracketed in the given interval.

    :param target_ratio: Desired core area ratio (e.g., 0.25)
    :type target_ratio: float
    :param lb_face_footprint: Building footprint input for the black-box function
    :type lb_face_footprint: Any
    :param lower_bound: Lower bound for perimeter offset
    :type lower_bound: float
    :param upper_bound: Upper bound for perimeter offset
    :type upper_bound: float
    :param tol: Tolerance for convergence
    :type tol: float
    :param max_iter: Maximum number of iterations for Brent's method
    :type max_iter: int

    :return: Optimal perimeter offset, or 0.0 if not found
    :rtype: float
    """
    # Validate the target ratio
    if not (0.0 <= target_ratio < 1.0):
        print(f"Warning: target_ratio={target_ratio} is outside the valid range [0.0, 1.0). Returning 0.0.")
        return 0.0

    def root_function(perimeter_offset: float) -> float:
        return _compute_core_area_ratio_for_offset_value(perimeter_offset, lb_face_footprint) - target_ratio

    try:
        val_low = root_function(lower_bound)
        val_high = root_function(upper_bound)
        if val_low * val_high > 0:
            raise ValueError("Root not bracketed in the interval.")

        return brent(root_function, a=lower_bound, b=upper_bound, tol=tol, max_iter=max_iter)

    except (ValueError, RuntimeError) as e:
        print(f"Warning: {e}. Returning 0.0 as fallback perimeter offset.")
        return 0.0


from typing import Any


def _compute_core_area_ratio_for_offset_value(perimeter_offset: float,
                                              lb_face_footprint: Face3D) -> float:
    """
    Computes the ratio of core area to total footprint area for a given perimeter offset.

    This function constructs a temporary building model from the given footprint,
    solves adjacency between rooms, and then calculates the ratio of floor area
    occupied by core spaces.

    :param perimeter_offset: Offset value to be applied from the perimeter to define the core
    :type perimeter_offset: float
    :param lb_face_footprint: A Ladybug geometry face representing the building footprint
    :type lb_face_footprint: Any

    :return: Ratio of total core area to the footprint area
    :rtype: float
    """
    df_building = Building.from_footprint(
        identifier="temp",
        footprint=[lb_face_footprint],
        floor_to_floor_heights=[3.0],  # Height doesn't affect core ratio here
        perimeter_offset=perimeter_offset,
        tolerance= 0.01
    )
    # Solve the adjacency to identify the core properly
    for room in df_building.unique_room_2ds:
        room.solve_adjacency(df_building.unique_room_2ds)

    total_core_area = sum(
        core.floor_area for core in df_building.unique_room_2ds if core.is_core
    )

    return total_core_area / lb_face_footprint.area


def brent(f: Callable[[float], float],
          a: float,
          b: float,
          tol: float = 1e-6,
          max_iter: int = 100) -> float:
    """
    Brent's method for finding a root of the function f in the interval [a, b].

    Combines bisection, secant, and inverse quadratic interpolation.
    Requires that f(a) and f(b) have opposite signs.

    :param f: Function to find the root of; must take a float and return a float.
    :type f: Callable[[float], float]
    :param a: Lower bound of the interval
    :type a: float
    :param b: Upper bound of the interval
    :type b: float
    :param tol: Tolerance for convergence
    :type tol: float
    :param max_iter: Maximum number of iterations
    :type max_iter: int

    :return: Estimated root of f within [a, b]
    :rtype: float

    :raises ValueError: If f(a) and f(b) do not bracket a root
    :raises RuntimeError: If the method fails to converge within max_iter
    """
    fa = f(a)
    fb = f(b)

    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")

    if abs(fa) < abs(fb):
        a, b = b, a
        fa, fb = fb, fa

    c = a
    fc = fa
    d = e = b - a

    for _ in range(max_iter):
        if fb == 0 or abs(b - a) < tol:
            return b

        if fa != fc and fb != fc:
            # Inverse quadratic interpolation
            s = (a * fb * fc) / ((fa - fb) * (fa - fc)) \
                + (b * fa * fc) / ((fb - fa) * (fb - fc)) \
                + (c * fa * fb) / ((fc - fa) * (fc - fb))
        else:
            # Secant method
            s = b - fb * (b - a) / (fb - fa)

        # Check interpolation conditions
        cond1 = not ((3 * a + b) / 4 < s < b) if a < b else not (b < s < (3 * a + b) / 4)
        cond2 = abs(s - b) >= abs(b - c) / 2
        cond3 = abs(b - c) < tol
        cond4 = abs(c - d) < tol

        if cond1 or cond2 or cond3 or cond4:
            s = (a + b) / 2  # Bisection fallback
            d = e = b - a
        else:
            d = e
            e = b - s

        fs = f(s)
        c, fc = b, fb

        if fa * fs < 0:
            b = s
            fb = fs
        else:
            a = s
            fa = fs

        if abs(fa) < abs(fb):
            a, b = b, a
            fa, fb = fb, fa

    raise RuntimeError("Brent's method did not converge within the maximum number of iterations.")
