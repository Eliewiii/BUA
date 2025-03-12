"""

"""
import os

import pytest

from bua.bipv.bipv_subsidies import BipvSubsidy

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

