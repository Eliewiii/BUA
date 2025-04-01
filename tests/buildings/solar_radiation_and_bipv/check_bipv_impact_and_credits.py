from bua.config.config_default_values_user_parameters import default_path_simulation_folder, default_grid_ghg_intensity, \
    default_grid_energy_intensity, default_grid_electricity_sell_price, default_discount_rate
import json
import logging
import os
from bua.simulation_steps import *

# Initialize json result file
name_result_json_file = "results_context_filter.json"
path_result_folder = r"C:\Users\julius.jandl\OneDrive - Technion\Julius PhD\Codes\test"
path_json_result_file = os.path.join(path_result_folder, name_result_json_file)
path_urban_canopy_file = r"C:\Users\julius.jandl\AppData\Local\BUA\Simulation_temp"

scenarios_dict = {
        "baseline": {
            "rooftech": "mitrex_roof c-Si M390-A1F 2025",
            "envtech": "mitrex_facades c-Si Solar Siding 350W - Dove Grey china 2025",
            "replacement": 10,
            "x_size": 0.996,
            "y_size": 2.030
        }}
scenario_id = list(scenarios_dict.keys())[0]
subsidy_type = "fit_fixed_high"

# load urban canopy object from generate_sample_for_bipv
json_result_dict = {}
with open(path_json_result_file, 'w') as json_file:
    json.dump(json_result_dict, json_file)

urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(path_simulation_folder=path_urban_canopy_file)

SimFunSolarRadAndBipv.run_bipv_harvesting_and_lca_simulation(
            urban_canopy_object=urban_canopy_object,
            building_id_list=None,
            bipv_scenario_identifier=scenario_id,
            roof_id_pv_tech=scenarios_dict[scenario_id]["rooftech"],
            facades_id_pv_tech=scenarios_dict[scenario_id]["envtech"],
            subsidy_id=subsidy_type,
            minimum_panel_eroi=1.5,
            minimum_economic_roi=0,
            electricity_sell_price=0.14,
            start_year=2025,
            end_year=2075,
            replacement_scenario="replace_failed_panels_every_X_years",
            continue_simulation=False,
            update_panel_technology=False,
            replacement_frequency_in_years=scenarios_dict[scenario_id]["replacement"],
            discount_rate=default_discount_rate)

##### Run KPI computation
SimFunSolarRadAndBipv.run_kpi_simulation(urban_canopy_object=urban_canopy_object,
                                         bipv_scenario_identifier=scenario_id,
                                         grid_ghg_intensity=default_grid_ghg_intensity,
                                         grid_energy_intensity=default_grid_energy_intensity,
                                         grid_electricity_sell_price=default_grid_electricity_sell_price,
                                         zone_area=None,
                                         subsidy_type = subsidy_type,
                                         discount_rate = default_discount_rate)

alternative_result_dict = {
    "scenario_id": scenario_id,
    "start_year": 2025,
    'end_year': 2075,
    "bipv_and_kpi_simulation": urban_canopy_object.bipv_scenario_dict[scenario_id].to_dict(),
    "UBES": urban_canopy_object.ubes_obj.to_dict()
}

json_result_dict[scenario_id] = alternative_result_dict
# Overwrite the json file
with open(path_json_result_file, 'w') as json_file:
    json.dump(json_result_dict, json_file)