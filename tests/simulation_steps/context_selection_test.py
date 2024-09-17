"""
Unit tests BIPV_simulation
"""

import os
import pytest

from src.bua.simulation_steps import *
from src.bua.config.config_default_values_user_parameters import *

from .conftest import init_urban_canopy_with_buildingmodels_and_buildingbasic

class TestContextSelection:

    @pytest.mark.parametrize("mvfc", ["0.99", "0.1", "0.000000000000001"])
    def test_first_pass_context_selection(self,init_urban_canopy_with_buildingmodels_and_buildingbasic):
        """
        Check that
        """


