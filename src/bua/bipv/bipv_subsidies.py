"""
Class of subsidies to integrate in economic assessment
"""

import os
import json




class BipvSubsidy:


    def __init__(self, identifier):
        self.identifier = identifier

        # electricity selling price
        self.electricity_price_peak_hours = None  # in USD/kWh, for 15:00-21:00
        self.electricity_price_offpeak_hours = None  # in USD/kWh, for 10:00-15:00
        self.electricity_price_shoulder_hours = None  # in USD/kWh, for all other hours
        self.electricity_price_decrease_per_year = None # ratio

        # investment support
        self.investment_support = None # ratio, what is paid for by government

        #loan
        self.equity_ratio = None # ratio, how much money is paid upfront
        self.loan_interest_rate = None # interest rate on loan

        #carbon credit
        self.carbon_tax = None # USD per ton CO2

        #income tax
        self.income_tax = None # income tax paid on sold electricity


    @classmethod
    def create_bipv_subsidy_obj_from_json(cls, subsidy_obj_dict, path_json_folder):

        """
        Load the json file with information about subsidies and create the Subsidy objects
        """

        for file in os.listdir(path_json_folder):
            if file.endswith(".json"):
                with open(os.path.join(path_json_folder, file), 'r') as json_file:
                    data = json.load(json_file)
                    for key, value in data.items():
                        if value["type"] != "subsidy":
                            continue
                        subsidy_obj = cls(value["id"])

                        # defining object properties
                        subsidy_obj.electricity_price_peak_hours = float(value["fit_peak"])
                        subsidy_obj.electricity_price_offpeak_hours = float(value["fit_offpeak"])
                        subsidy_obj.electricity_price_shoulder_hours = float(value["fit_shoulder"])
                        subsidy_obj.electricity_price_decrease_per_year = float(value["fit_decrease_per_year"])

                        subsidy_obj.investment_support = float(value["investment_support_ratio"])

                        subsidy_obj.equity_ratio = float(value["loan_equity_ratio"])
                        subsidy_obj.loan_interest_rate = float(value["loan_interest_rate"])

                        subsidy_obj.carbon_tax = int(value["carbon_tax_per_ton_CO2"])
                        subsidy_obj.income_tax = float(value["income_tax_reduction_on_energy_generation"])

                        # Save the object in the dictionary if it does not exist
                        if subsidy_obj.identifier not in subsidy_obj_dict:
                            subsidy_obj_dict[subsidy_obj.identifier] = subsidy_obj
                        else:
                            raise ValueError(f"The subsidy object{subsidy_obj.identifier} already exists, "
                                             f"it must have been duplicated in the json file")

        return subsidy_obj_dict

    def get_electricity_price_per_hour(self, ):

