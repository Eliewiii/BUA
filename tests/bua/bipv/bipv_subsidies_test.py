"""

"""
import os
import random
import pytest
import unittest

from bua.bipv.bipv_subsidies import BipvSubsidy
from bua.urban_canopy.bipv_scenario_urban_canopy import BipvScenario

path_test_folder =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path_test_data_bipv_dir=r"C:\Users\julius.jandl\AppData\Local\BUA\Libraries\BIPV\user"

name_json_bipv_subsidies_test= "subsidies_julius.json"

class TestBipvSubsidiesObj(unittest.TestCase):

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
        gtg_dict = {"cost": {
            "investment": [random.randint(1, 100000) for _ in range(end_year-start_year)]
            },
            "loan_payments" : None
        }
        original_investment_cost = gtg_dict["cost"]["investment"][0]

        gtg_dict = bipv_sub_obj.calculate_loan_payment_list(start_year, end_year, gtg_dict)

        new_investment_cost = gtg_dict["cost"]["investment"][0]

        self.assertEqual(new_investment_cost*2, original_investment_cost)


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


    def test_energy_harvesting_stretched_list_new(self):

        sun_hours = [7.5, 8.5]

        hourly_energy_table = [[2, 3],
                               [4, 3],
                               [1, 5],
                               [4, 2]]

        # Expected output when round_up is False
        expected_output_no_round = [
            [0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        full_year_irradiation_table = BipvScenario.stretch_harvested_energy_list(hourly_energy_table, sun_hours,
                                                                                 round_up=False)

        # Assert that the function returns the expected result
        self.assertEqual(full_year_irradiation_table, expected_output_no_round)

        # Expected output when round_up is True
        expected_output_round_up = [
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        full_year_irradiation_table_round_up = BipvScenario.stretch_harvested_energy_list(hourly_energy_table,
                                                                                          sun_hours, round_up=True)

        # Assert that the function returns the expected result when rounding up
        self.assertEqual(full_year_irradiation_table_round_up, expected_output_round_up)

