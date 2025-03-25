"""

"""
import os
import random
import pytest

from bua.bipv.bipv_subsidies import BipvSubsidy
from bua.urban_canopy.bipv_scenario_urban_canopy import BipvScenario

path_test_folder =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path_test_data_bipv_dir=os.path.join(path_test_folder,'test_data',"bipv")

name_json_bipv_subsidies_test= "subsidies_julius.json"

class TestBipvSubsidiesObj:

    def test_initialize(self):
        bipv_sub_obj = BipvSubsidy("test")
        assert type(bipv_sub_obj) == BipvSubsidy


    def test_load_json(self):
        print(path_test_folder)
        subsidy_obj_dict = {}
        BipvSubsidy.create_bipv_subsidy_obj_from_json(subsidy_obj_dict, path_test_data_bipv_dir)

        print(subsidy_obj_dict)

    def test_get_feed_in_tariff(self):
        subsidy_obj_dict = {}
        BipvSubsidy.create_bipv_subsidy_obj_from_json(subsidy_obj_dict, path_test_data_bipv_dir)
        bipv_sub_obj = subsidy_obj_dict["fit_time_of_use"]
        hour = random.randint(0,8760)
        print(hour)

        price = bipv_sub_obj.get_electricity_price_per_hour(hour)
        print(price)

    def test_loan_payments(self):
        start_year = 2025
        end_year = 2075
        subsidy_obj_dict = {}
        BipvSubsidy.create_bipv_subsidy_obj_from_json(subsidy_obj_dict, path_test_data_bipv_dir)
        bipv_sub_obj = subsidy_obj_dict["loan_low"]
        bipv_results_dict = {"cost": {
            "investment": {
                "gate_to_gate": {
                    "yearly": [random.randint(1, 100000) for _ in range(end_year-start_year)]
                    }}}}
        print(bipv_results_dict["cost"]["investment"]["gate_to_gate"]["yearly"][0])

        payments = bipv_sub_obj.calculate_loan_payment_list(start_year, end_year, 25, bipv_results_dict)

        print(sum(payments), bipv_results_dict["cost"]["investment"]["gate_to_gate"]["yearly"][0])

    def test_energy_harvesting_stretched_list(self):

        sun_hours = [7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5]

        hourly_energy_table = [[7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5],
                               [7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5],
                               [7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5],
                               [7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5],
                               [7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5]]


        bipv_scenario_obj = BipvScenario("baseline", 2025, 2075)
        bipv_scenario_obj.init_bipv_results_dict()
        bipv_scenario_obj.bipv_results_dict["roof"]["hourly_energy_harvested"]["yearly"] = (
            bipv_scenario_obj.stretch_harvested_energy_list(hourly_energy_table, sun_hours, round_up=False))

        print(bipv_scenario_obj.bipv_results_dict["roof"]["hourly_energy_harvested"]["yearly"])