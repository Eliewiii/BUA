"""

"""

from ladybug_geometry.geometry3d.face import Face3D
from src.bua.building.utils_buildings.lbt_obj_methods.core_genration import brent,find_perimeter_offset_for_target_core_area_ratio


def assert_close(val, expected, tol=1e-6):
    if abs(val - expected) > tol:
        raise AssertionError(f"Test failed: got {val}, expected {expected}")
    else:
        print(f"✔ Passed: root ≈ {val:.6f} (expected {expected})")

def test_brent_method():


    print("Running Brent's method tests...\n")

    # Test 1: f(x) = x^2 - 4 → root at x = 2
    def f1(x):
        return x ** 2 - 4

    root1 = brent(f1, a=0, b=4)
    assert_close(root1, 2)

    # Test 2: f(x) = log(x) - 1 → root at x = e ≈ 2.718
    import math
    def f2(x):
        return math.log(x) - 1

    root2 = brent(f2, a=1, b=4)
    assert_close(root2, math.e)

    # Test 3: f(x) = 5x - 15 → root at x = 3
    def f3(x):
        return 5 * x - 15

    root3 = brent(f3, a=0, b=5)
    assert_close(root3, 3)

    # Test 4: Custom black box style: f(x) = (x - p)^3 where p = 1.5
    p = 1.5

    def f4(x):
        return (x - p) ** 3

    root4 = brent(f4, a=0, b=3)
    assert_close(root4, p)

    print("\nAll tests passed!")


def test_find_perimeter_offset_for_target_core_area_ratio():
    lb_face3d = Face3D.from_array([[[0., 0., 0.], [10., 0., 0.], [10., 10., 0.], [0., 10., 0.]]])

    perimeter_offset = find_perimeter_offset_for_target_core_area_ratio(target_ratio=0.01,
                                                                        lb_face_footprint=lb_face3d)

    assert_close(perimeter_offset,4.5,1e-3)

    perimeter_offset = find_perimeter_offset_for_target_core_area_ratio(target_ratio=0.25,
                                                                        lb_face_footprint=lb_face3d)

    assert_close(perimeter_offset, 2.5, 1e-3)

