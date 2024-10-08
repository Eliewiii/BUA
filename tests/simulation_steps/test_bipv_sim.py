"""
Unit tests BIPV_simulation
"""

import os
import pytest

from src.bua.simulation_steps import *
from src.bua.config.config_default_values_user_parameters import *

from src.bua.urban_canopy import UrbanCanopy
from src.bua.building import BuildingModeled

# Inputs to be used
test_file_dir = os.getcwd()
print()
test_folder_dir = os.path.dirname(test_file_dir)
test_data_dir = os.path.join(test_folder_dir, "test_data")
path_test_building_hbjson_0 = os.path.join(test_data_dir, "test_hbjsons", "Building_sample_0.hbjson")
print("")
print(f"path_test_building_hbjson_0: {path_test_building_hbjson_0}")


def test_bua_simulation_flow_until_bipv():
    """
    Check that
    """
    print("")
    print(f"test_file_dir: {test_file_dir}")
    print(f"path_test_building_hbjson_0: {path_test_building_hbjson_0}")
    # Clear simulation temp folder
    SimulationCommonMethods.clear_simulation_temp_folder()
    assert os.listdir(default_path_simulation_folder) == []
    # Create simulation folder
    SimulationCommonMethods.make_simulation_folder(path_simulation_folder=default_path_simulation_folder)

    # Create an UrabanCanopy object
    urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(
        path_simulation_folder=default_path_simulation_folder)
    # Save the UrbanCanopy object to a pickle and json files
    SimulationCommonMethods.save_urban_canopy_object_to_pickle(urban_canopy_object=urban_canopy_object,
                                                               path_simulation_folder=default_path_simulation_folder)

    ###############################
    # Load HBJSONs
    ###############################

    # Add HBJSON building to the UrbanCanopy object
    SimulationLoadBuildingOrGeometry.add_buildings_from_hbjson_to_urban_canopy(
        urban_canopy_object=urban_canopy_object,
        path_folder_hbjson=None,
        path_file_hbjson=path_test_building_hbjson_0,
        are_buildings_targets=True,
        keep_context_from_hbjson=False)

    print("")
    print(f"UrbanCanopy object after adding the building: {urban_canopy_object.building_dict}")


def other_test():
    ###############################
    # BIPV simulation
    ###############################

    # Generate the sensor grids
    SimFunSolarRadAndBipv.generate_sensor_grid(
        urban_canopy_object=urban_canopy_object,
        bipv_on_roof=True,
        bipv_on_facades=True,
        roof_grid_size_x=default_roof_grid_size_x,
        facades_grid_size_x=default_facades_grid_size_x,
        roof_grid_size_y=default_roof_grid_size_y,
        facades_grid_size_y=default_facades_grid_size_y,
        offset_dist=default_offset_dist,
        overwrite=True
    )

    # Test
    # todo

    # Run Solar Radiation Simulation
    SimFunSolarRadAndBipv.run_annual_solar_irradiance_simulation(
        urban_canopy_object=urban_canopy_object,
        path_simulation_folder=default_path_simulation_folder,
        path_weather_file=default_path_weather_file,
        overwrite=True)

    # Test
    # todo

    # Run BIPV Simulation
    SimFunSolarRadAndBipv.run_bipv_harvesting_and_lca_simulation(
        urban_canopy_object=urban_canopy_object,
        path_simulation_folder=default_path_simulation_folder,
        bipv_scenario_identifier=default_bipv_scenario_identifier,
        roof_id_pv_tech=default_id_pv_tech_roof,
        facades_id_pv_tech=default_id_pv_tech_facades,
        roof_transport_id=default_roof_transport_id,
        facades_transport_id=default_facades_transport_id,
        roof_inverter_id=default_roof_inverter_id,
        facades_inverter_id=default_facades_inverter_id,
        roof_inverter_sizing_ratio=default_roof_inverter_sizing_ratio,
        facades_inverter_sizing_ratio=default_facades_inverter_sizing_ratio,
        minimum_panel_eroi=1.5,
        start_year=0,
        end_year=30,
        replacement_scenario=default_replacement_scenario,
        continue_simulation=False,
        replacement_frequency_in_years=25
    )

    # Save the UrbanCanopy object to a pickle and json files
    SimulationCommonMethods.save_urban_canopy_object_to_pickle(urban_canopy_object=urban_canopy_object,
                                                               path_simulation_folder=default_path_simulation_folder)
    SimulationCommonMethods.save_urban_canopy_to_json(urban_canopy_object=urban_canopy_object,
                                                      path_simulation_folder=default_path_simulation_folder)


def test_bua_bipv_simulation():
    # Create an UrabanCanopy object
    urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(
        path_simulation_folder=default_path_simulation_folder)

    # Run BIPV Simulation
    SimFunSolarRadAndBipv.run_bipv_harvesting_and_lca_simulation(
        urban_canopy_object=urban_canopy_object,
        path_simulation_folder=default_path_simulation_folder,
        bipv_scenario_identifier=default_bipv_scenario_identifier,
        roof_id_pv_tech=default_id_pv_tech_roof,
        facades_id_pv_tech=default_id_pv_tech_facades,
        roof_transport_id=default_roof_transport_id,
        facades_transport_id=default_facades_transport_id,
        roof_inverter_id=default_roof_inverter_id,
        facades_inverter_id=default_facades_inverter_id,
        roof_inverter_sizing_ratio=default_roof_inverter_sizing_ratio,
        facades_inverter_sizing_ratio=default_facades_inverter_sizing_ratio,
        minimum_panel_eroi=1.5,
        start_year=0,
        end_year=50,
        # replacement_scenario=default_replacement_scenario,
        replacement_scenario="replace_all_panels_every_X_years",
        continue_simulation=False,
        replacement_frequency_in_years=10,
        infrastructure_replacement_last_year=40,
        panel_replacement_min_age=25,
        # no_csv=True
    )
    # Save the UrbanCanopy object to a pickle and json files
    SimulationCommonMethods.save_urban_canopy_object_to_pickle(urban_canopy_object=urban_canopy_object,
                                                               path_simulation_folder=default_path_simulation_folder)
    SimulationCommonMethods.save_urban_canopy_to_json(urban_canopy_object=urban_canopy_object,
                                                      path_simulation_folder=default_path_simulation_folder)
