"""
Class of subsidies to integrate in economic assessment with different parameters
"""

import os
import json
from xmlrpc.client import boolean

from bua.config.config_default_values_user_parameters import default_grid_ghg_intensity


class BipvSubsidy:


    def __init__(self, identifier):
        self.identifier = identifier
        self.type = None
        # electricity selling price, depending on hour of the day
        self.electricity_price_peak_hours = None  # in USD/kWh; for 15:00-21:00
        self.electricity_price_offpeak_hours = None  # in USD/kWh; for 10:00-15:00
        self.electricity_price_shoulder_hours = None  # in USD/kWh; for all other hours
        self.electricity_price_decrease_per_year = None # ratio

        # investment support
        self.investment_support = None # ratio; amount that is paid for by government (e.g. 0.3 means 30 % of the investment cost are taken over by the government)

        #loan
        self.equity_ratio = None # ratio; amount of investment cost that are paid for upfront
        self.loan_interest_rate = None # interest rate on loan
        self.payback_years = None # years over which loan is paid back

        #carbon credit
        self.carbon_tax = None # USD per ton CO2

        #income tax
        self.income_tax = None # income tax paid on sold electricity

        #remuneration
        self.remuneration = None #boolean, is excess energy sold or is value only created for self-consumed energy


    @classmethod
    def create_bipv_subsidy_obj_from_json(cls, subsidy_obj_dict, path_json_folder):

        """
        Load the json file with information about subsidies and create the Subsidy objects as dictionary
        :param subsidy_obj_dict: dictionary with stored subsidy information
        :param path_json_folder: path to folder where input parameters are stored
        """

        list_of_files = os.listdir(path_json_folder)
        for file in os.listdir(path_json_folder):
            if file.endswith(".json"):
                with open(os.path.join(path_json_folder, file), 'r') as json_file:
                    data = json.load(json_file)
                    for key, value in data.items():
                        if value["type"] != "subsidy":
                            continue
                        subsidy_obj = cls(value["id"])
                        subsidy_obj.type = str(value["type"])
                        # defining object properties
                        subsidy_obj.electricity_price_peak_hours = float(value["fit_peak"])
                        subsidy_obj.electricity_price_offpeak_hours = float(value["fit_offpeak"])
                        subsidy_obj.electricity_price_shoulder_hours = float(value["fit_shoulder"])
                        subsidy_obj.electricity_price_decrease_per_year = float(value["fit_decrease_per_year"])

                        subsidy_obj.investment_support = float(value["investment_support_ratio"])

                        subsidy_obj.equity_ratio = float(value["loan_equity_ratio"])
                        subsidy_obj.loan_interest_rate = float(value["loan_interest_rate"])
                        subsidy_obj.payback_years = int(value["loan_payback_years"])

                        subsidy_obj.carbon_tax = int(value["carbon_tax_per_ton_CO2"])
                        subsidy_obj.income_tax = float(value["income_tax_reduction_on_energy_generation"])

                        subsidy_obj.remuneration = str(value["remuneration"])

                        # Save the object in the dictionary if it does not exist
                        if subsidy_obj.identifier not in subsidy_obj_dict:
                            subsidy_obj_dict[subsidy_obj.identifier] = subsidy_obj
                        else:
                            raise ValueError(f"The subsidy object{subsidy_obj.identifier} already exists, "
                                             f"it must have been duplicated in the json file")

        return subsidy_obj_dict

    def get_electricity_price_per_hour(self, hour):
        """
        obtains the electricity price for a specific hour of the day to account for dynamic pricing
        :param hour: hour of the day (0-23)
        """
        hour_of_day = hour % 24
        if 21 <= hour_of_day or hour_of_day < 10:  # 21:00 - 10:00
            electricity_price_per_hour = self.electricity_price_offpeak_hours
        elif 10 <= hour_of_day < 15:  # 10:00 - 15:00
            electricity_price_per_hour = self.electricity_price_shoulder_hours
        elif 15 <= hour_of_day < 21:  # 15:00 - 21:00
            electricity_price_per_hour = self.electricity_price_peak_hours

        return electricity_price_per_hour

    def calculate_investment_subsidy(self, start_year, end_year, gate_to_gate_dict):
        """
        adjusts the gate to gate dictionary from solar_rad_and_BIPV to reduce the investment cost in year 0
        :param start_year: first year of analysis
        :param end_year: last year of analysis
        :param gate_to_gate_dict: dictionary that contains GHG emissions, energy demand, and costs of the gate to gate step (investment)
        """

        investment_support_yearly_list = [0] * (end_year - start_year)
        investment_support_yearly_list[0] = self.investment_support*gate_to_gate_dict["cost"]["investment"][0]

        return investment_support_yearly_list

    def calculate_loan_payment_list(self, start_year, end_year, gate_to_gate_dict):
        """
        calculates the loan payments from the equity rate and the interest rate. the function adjusts the investment costs in the gate to gate dictionary and adds the loan payments
        :param start_year: first year of analysis
        :param end_year: last year of analysis
        :param gate_to_gate_dict: dictionary that contains GHG emissions, energy demand, and costs of the gate to gate step (investment)
        """

        loan_payments = []
        r = self.loan_interest_rate
        initial_investment_cost = gate_to_gate_dict["cost"]["investment"][0] # investment costs in the first year

        # construct yearly list of loan payments
        for year in range((end_year + 1) - start_year):
            if year == 0:
                loan_payments.append(0)
            elif year < self.payback_years:
                loan_payments.append((initial_investment_cost*(1-self.equity_ratio) * r) / (1 - (1 + r) ** - self.payback_years))
            elif year > self.payback_years:
                loan_payments.append(0)

        # correct investment cost in year 0
        gate_to_gate_dict["cost"]["investment"][0] = initial_investment_cost*self.equity_ratio

        # add loan payments to the gate to gate dictionary
        gate_to_gate_dict["cost"]["loan_payments"] = loan_payments

        return gate_to_gate_dict

    def calculate_carbon_tax_savings_list(self, energy_harvested_list, grid_ghg_intensity = default_grid_ghg_intensity):
        """
        calculate the revenue created from omitting carbon emissions
        :param energy_harvested_list: list with yearly values of energy harvesting
        :param grid_ghg_intensity: grid ghg intensity of the regular grid, used to calculate the omitted emissions from producing green energy
        """

        carbon_tax_savings = [grid_ghg_intensity * self.carbon_tax/1000 * energy_harvested_list[year]
                              for year in range(len(energy_harvested_list))]

        return carbon_tax_savings

