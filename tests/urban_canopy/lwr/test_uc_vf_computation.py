"""

"""

import pytest
import logging

import time

from honeybee.boundarycondition import Outdoors

from src.bua.simulation_steps import SimulationLWR

from tests.urban_canopy.uc_test_utils import init_urban_canopy_with_one_buildingmodel, \
    init_urban_canopy_with_two_buildingmodels, init_urban_canopy_with_all_buildingmodels


class TestUrbCanRadSurMan:

    def test_init_rsm(self, init_urban_canopy_with_one_buildingmodel):
        """

        """
        urban_canopy_object = init_urban_canopy_with_one_buildingmodel
        lwr_sm = urban_canopy_object.lwr_simulation_manager
        assert lwr_sm is not None
        assert lwr_sm.num_surfaces == 0


    def test_include_surfaces_in_rsm_two_buildings(self, init_urban_canopy_with_two_buildingmodels):
        """

        """
        urban_canopy_object = init_urban_canopy_with_two_buildingmodels
        # Get number of surfaces
        building_obj_list = list(urban_canopy_object.building_dict.values())
        building_hb_model_list = [building_obj.hb_model_obj for building_obj in building_obj_list]
        num_outdoor_surfaces = sum(
            [1 if isinstance(surface.boundary_condition, Outdoors) else 0 for building_hb_model in
             building_hb_model_list for surface in
             building_hb_model.faces])
        print(f"\n num_outdoor_surfaces: {num_outdoor_surfaces}")
        # get number of windows
        num_windows = sum(
            [len(surface.apertures) for building_hb_model in building_hb_model_list for surface in
             building_hb_model.faces if isinstance(surface.boundary_condition, Outdoors)])
        print(f"\n num_windows: {num_windows}")

        tot_surfaces = num_outdoor_surfaces + num_windows

        # Check without windows
        urban_canopy_object.generate_radiative_surface_manager_for_lwr_computation(include_windows=False)
        assert urban_canopy_object.lwr_simulation_manager.num_surfaces == num_outdoor_surfaces

        # Check with windows
        urban_canopy_object.generate_radiative_surface_manager_for_lwr_computation(overwrite=True,
                                                                                   include_windows=True)
        assert urban_canopy_object.lwr_simulation_manager.num_surfaces == tot_surfaces




    def test_run_vf_comp_from_subprocess(self, init_urban_canopy_with_two_buildingmodels):
        """

        """
        urban_canopy_object = init_urban_canopy_with_two_buildingmodels
        SimulationLWR.generate_radiative_surface_manager_for_lwr_computation(urban_canopy_object,
                                                                             overwrite=True,
                                                                             include_windows=True)
        SimulationLWR.perform_lwr_vf_computation(urban_canopy_object, overwrite=True)
