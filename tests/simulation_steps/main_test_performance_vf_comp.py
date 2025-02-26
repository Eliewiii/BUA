

import time

from src.bua.urban_canopy import UrbanCanopy
from src.bua.simulation_steps import *
from src.bua.config.config_default_values_user_parameters import *

# Inputs to be used
test_file_dir = os.path.dirname(os.path.abspath(__file__))
test_folder_dir = os.path.dirname(test_file_dir)
test_data_dir = os.path.join(test_folder_dir, "test_data")
path_test_building_hbjson_0 = os.path.join(test_data_dir, "test_hbjsons", "Building_sample_0.hbjson")
path_test_building_hbjson_1 = os.path.join(test_data_dir, "test_hbjsons", "Building_sample_1.hbjson")
path_test_lb_polyface3d_context = os.path.join(test_data_dir, "test_lb_polyface3d_context.json")
# print("")
# print(f"path_test_building_hbjson_0: {path_test_building_hbjson_0}")
# print(f"path_test_building_hbjson_1: {path_test_building_hbjson_1}")
# print(f"path_test_lb_polyface3d_context: {path_test_lb_polyface3d_context}")



def init_urban_canopy_with_all_buildingmodels() -> UrbanCanopy:
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
        path_folder_hbjson=os.path.join(test_data_dir, "test_hbjsons"),
        path_file_hbjson=None,
        are_buildings_targets=True,
        keep_context_from_hbjson=False)

    return urban_canopy_object



def init_urban_canopy_with_x_buildingmodels(num_buildings) -> UrbanCanopy:
    """
    Generate an UrbanCanopy object with 2 BuildingModeled and BuildingBasic objects
    """
    path_hbjson_folder= os.path.join(test_data_dir, "test_hbjsons")
    list_hbjson_files = os.listdir(path_hbjson_folder)
    if num_buildings > len(list_hbjson_files):
        raise ValueError("num_buildings should be less than the number of HBJSON files in the folder")
    # Clear simulation temp folder
    SimulationCommonMethods.clear_simulation_temp_folder()
    # Create simulation folder
    SimulationCommonMethods.make_simulation_folder(path_simulation_folder=default_path_simulation_folder)
    # Create an UrabanCanopy object
    urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(
        path_simulation_folder=default_path_simulation_folder)

    for i in range(num_buildings):
        path_hbjson = os.path.join(path_hbjson_folder, list_hbjson_files[i])
        SimulationLoadBuildingOrGeometry.add_buildings_from_hbjson_to_urban_canopy(
            urban_canopy_object=urban_canopy_object,
            path_folder_hbjson=None,
            path_file_hbjson=path_hbjson,
            are_buildings_targets=True,
            keep_context_from_hbjson=False)

    return urban_canopy_object


def init_urban_canopy_with_two_buildingmodels() -> UrbanCanopy:
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

    return urban_canopy_object


def run_vf_comp_from_subprocess(urban_canopy_obj,include_windows=True):
    """

    """
    SimulationLWR.generate_radiative_surface_manager_for_lwr_computation(urban_canopy_obj,
                                                                         overwrite=True,
                                                                         include_windows=True)

    SimulationLWR.perform_lwr_vf_computation(urban_canopy_obj, overwrite=True, save_to_pkl= True)


if __name__ == "__main__":

    include_windows = False
    # include_windows = True

    max_num_buildings = 2

    duration_list = []

    for i in range(1, max_num_buildings+1):
        dur= time.time()
        print(f"Running for {i} buildings")
        urban_canopy_obj = init_urban_canopy_with_x_buildingmodels(i)
        run_vf_comp_from_subprocess(urban_canopy_obj, include_windows)
        duration_list.append(time.time()-dur)

    print("\n\n\n")

    for i in range(max_num_buildings):
        print(f"Duration for {i+1} buildings: {duration_list[i]}")

