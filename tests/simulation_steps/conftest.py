"""
F
"""

import os
import pytest

from src.bua.simulation_steps import *
from src.bua.config.config_default_values_user_parameters import *

# Inputs to be used
test_file_dir = os.path.dirname(os.path.abspath(__file__))
test_folder_dir = os.path.dirname(test_file_dir)
test_data_dir = os.path.join(test_folder_dir, "test_data")
path_test_building_hbjson_0 = os.path.join(test_data_dir, "test_hbjsons", "Building_sample_0.hbjson")
path_test_building_hbjson_1 = os.path.join(test_data_dir, "test_hbjsons", "Building_sample_1.hbjson")
path_test_lb_polyface3d_context = os.path.join(test_data_dir, "test_lb_polyface3d_context.json")
print("")
print(f"path_test_building_hbjson_0: {path_test_building_hbjson_0}")
print(f"path_test_building_hbjson_1: {path_test_building_hbjson_1}")
print(f"path_test_lb_polyface3d_context: {path_test_lb_polyface3d_context}")


@pytest.fixture(scope='function')
def init_urban_canopy_with_buildingmodels_and_buildingbasic():
    """
    Generate an UrbanCanopy object with 2 BuildingModeled and BuildingBasic objects
    """
    # Clear simulation temp folder
    SimulationCommonMethods.clear_simulation_temp_folder()
    # Create simulation folder
    SimulationCommonMethods.make_simulation_folder(path_simulation_folder=default_path_simulation_folder)
    # Create an UrabanCanopy object
    urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(
        path_simulation_folder=default_path_simulation_folder)
    # Load HBJSONs
    SimulationLoadBuildingOrGeometry.add_buildings_from_hbjson_to_urban_canopy(
        urban_canopy_object=urban_canopy_object,
        path_folder_hbjson=None,
        path_file_hbjson=path_test_building_hbjson_0,
        are_buildings_targets=True,
        keep_context_from_hbjson=False)
    SimulationLoadBuildingOrGeometry.add_buildings_from_hbjson_to_urban_canopy(
        urban_canopy_object=urban_canopy_object,
        path_folder_hbjson=None,
        path_file_hbjson=path_test_building_hbjson_1,
        are_buildings_targets=True,
        keep_context_from_hbjson=False)
    # Load LB_POLYFACE3D context
    SimulationLoadBuildingOrGeometry.add_buildings_from_lb_polyface3d_json_in_urban_canopy(
        urban_canopy_object=urban_canopy_object,
        path_lb_polyface3d_json_file=path_test_lb_polyface3d_context)

    return urban_canopy_object

# def test_init_urban_canopy_with_buildingmodels_and_buildingbasic(init_urban_canopy_with_buildingmodels_and_buildingbasic):
#     """
#     Check the initialization of the UrbanCanopy object with 2 BuildingModeled and BuildingBasic objects
#     """
#     urban_canopy_object = init_urban_canopy_with_buildingmodels_and_buildingbasic
#