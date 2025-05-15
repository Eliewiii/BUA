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
        "net_metering_0_csi_test": {
            "rooftech": "mitrex_roof c-Si M390-A1F 2025",
            "envtech": "mitrex_facades c-Si Solar Siding 350W - Dove Grey china 2025",
            "replacement": 10,
            "subsidy_type": "nm_0"
        },
        "net_metering_0_cigs_test": {
            "rooftech": "cigs eterbright CIGS-3650A1 roof 2025",
            "envtech": "cigs eterbright CIGS-3650A1 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_0"
        },
}
"""
scenarios_dict = {
        "net_metering_0_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_0"
        },
        "net_metering_5_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_5"
        },
        "net_metering_10_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_10"
        },
        "net_metering_15_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_15"
        },
        "net_metering_20_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_20"
        },
        "net_metering_25_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_25"
        },
        "net_metering_30_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "nm_30"
        },
        "basecase_0_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "basecase_0"
        },
        "basecase_5_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "basecase_5"
        },
        "basecase_10_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "basecase_10"
        },
        "basecase_15_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "basecase_15"
        },
        "basecase_20_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "basecase_20"
        },
        "basecase_25_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "basecase_25"
        },
        "basecase_30_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "basecase_30"
        },
        "fixed_fit_0_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_0"
        },
        "fixed_fit_5_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_5"
        },
        "fixed_fit_10_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_10"
        },
        "fixed_fit_15_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_15"
        },
        "fixed_fit_20_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_20"
        },
        "fixed_fit_25_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_25"
        },
        "fixed_fit_30_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_30"
        },
        "decr_fit_0_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "decr_fit_0"
        },
        "decr_fit_5_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "decr_fit_5"
        },
        "decr_fit_10_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "decr_fit_10"
        },
        "decr_fit_15_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "decr_fit_15"
        },
        "decr_fit_20_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "decr_fit_20"
        },
        "decr_fit_25_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "decr_fit_25"
        },
        "decr_fit_30_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "decr_fit_30"
        },
        "tou_fit_0_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "tou_fit_0"
        },
        "tou_fit_5_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "tou_fit_5"
        },
        "tou_fit_10_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "tou_fit_10"
        },
        "tou_fit_15_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "tou_fit_15"
        },
        "tou_fit_20_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "tou_fit_20"
        },
        "tou_fit_25_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "tou_fit_25"
        },
        "tou_fit_30_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "tou_fit_30"
        },
        "fit_var_0_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_6"
        },
        "fit_var_8_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_8"
        },
        "fit_var_10_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_10"
        },
        "fit_var_12_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_12"
        },
        "fit_var_14_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_14"
        },
        "fit_var_16_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_16"
        },
        "fit_var_18_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_18"
        },
        "fit_var_20_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_20"
        },
        "fit_var_22_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_22"
        },
        "fit_var_24_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "fit_var_24"
        },
        "CC_10_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "cc_10"
        },
        "CC_20_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "cc_20"
        },
        "CC_40_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "cc_40"
        },
        "CC_50_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "cc_50"
        },
        "CC_60_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "cc_60"
        },
        "CC_80_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "cc_80"
        },
        "CC_100_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "cc_100"
        },
        "loan_1_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "loan_1"
        },
        "loan_2_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "loan_2"
        },
        "loan_3_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "loan_3"
        },
        "loan_4_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "loan_4"
        },
        "loan_5_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "loan_5"
        },
        "loan_6_cdte": {
            "rooftech": "cdte firstsolar FS-6445 roof 2025",
            "envtech": "cdte firstsolar FS-6445 facade 2025",
            "replacement": 10,
            "subsidy_type": "loan_6"
        }
    }
"""
scenario_id_list = list(scenarios_dict.keys())


# load urban canopy object from generate_sample_for_bipv
json_result_dict = {}
with open(path_json_result_file, 'w') as json_file:
    json.dump(json_result_dict, json_file)

urban_canopy_object = SimulationCommonMethods.create_or_load_urban_canopy_object(path_simulation_folder=path_urban_canopy_file)

for scenario_id in scenario_id_list:


    SimFunSolarRadAndBipv.run_bipv_harvesting_and_lca_simulation(
                urban_canopy_object=urban_canopy_object,
                building_id_list=None,
                bipv_scenario_identifier=scenario_id,
                roof_id_pv_tech=scenarios_dict[scenario_id]["rooftech"],
                facades_id_pv_tech=scenarios_dict[scenario_id]["envtech"],
                subsidy_id=scenarios_dict[scenario_id]["subsidy_type"],
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
                                             subsidy_type = scenarios_dict[scenario_id]["subsidy_type"],
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