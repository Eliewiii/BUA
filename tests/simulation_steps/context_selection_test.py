"""
Unit tests BIPV_simulation
"""

import os
import pytest

from src.bua.simulation_steps import *
from src.bua.config.config_default_values_user_parameters import *

from src.bua.building import BuildingModeled

from .conftest import init_urban_canopy_with_buildingmodels_and_buildingbasic


class TestContextSelection:

    @pytest.mark.parametrize("mvfc", [0.99, 0.01, 0.0000001])
    def test_first_pass_context_selection(self, init_urban_canopy_with_buildingmodels_and_buildingbasic,
                                          mvfc):
        """
        Check the first pass of context selection
        """
        ContextSelection.perform_first_pass_of_context_filtering_on_buildings(
            urban_canopy_object=init_urban_canopy_with_buildingmodels_and_buildingbasic,
            min_vf_criterion=mvfc)

        for building_obj in init_urban_canopy_with_buildingmodels_and_buildingbasic.building_dict.values():
            if isinstance(building_obj, BuildingModeled):
                assert building_obj.shading_context_obj.first_pass_done
                if mvfc == 0.99:
                    assert building_obj.shading_context_obj.selected_context_building_id_list == []
                else:
                    assert building_obj.shading_context_obj.selected_context_building_id_list != []

