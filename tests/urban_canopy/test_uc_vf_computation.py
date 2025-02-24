"""

"""

import pytest

from honeybee.boundarycondition import Outdoors

from tests.urban_canopy.uc_test_utils import init_urban_canopy_with_one_buildingmodel,init_urban_canopy_with_two_buildingmodels


class TestUrbCanRadSurMan:

    def test_init_rsm(self, init_urban_canopy_with_one_buildingmodel):
        """

        """
        urban_canopy_object = init_urban_canopy_with_one_buildingmodel
        rsm = urban_canopy_object.lwr_radiative_surface_manager
        assert rsm is not None
        assert rsm.num_surface == 0
        assert rsm._radiative_surface_dict == {}
        assert rsm._radiative_surface_id_list == []
        assert rsm._radiance_argument_list == []
        assert rsm._sim_parameter_dict["num_rays"] == None

    def test_include_surfaces_in_rsm_one_building(self, init_urban_canopy_with_one_buildingmodel):
        """

        """
        urban_canopy_object = init_urban_canopy_with_one_buildingmodel
        # Get number of surfaces
        building_obj = list(urban_canopy_object.building_dict.values())[0]
        building_hb_model = building_obj.hb_model_obj
        num_outdoor_surfaces = sum(
            [1 if isinstance(surface.boundary_condition, Outdoors) else 0 for surface in
             building_hb_model.faces])
        print(f"\n num_outdoor_surfaces: {num_outdoor_surfaces}")
        # get number of windows
        num_windows = sum(
            [len(surface.apertures) for surface in building_hb_model.faces if
             isinstance(surface.boundary_condition, Outdoors)])
        print(f"\n num_windows: {num_windows}")

        tot_surfaces = num_outdoor_surfaces + num_windows

        # Check without windows
        urban_canopy_object._generate_radiative_surface_manager_for_lwr_computation(include_windows=False)
        assert urban_canopy_object.lwr_radiative_surface_manager.num_surface == num_outdoor_surfaces

        # Check with windows
        urban_canopy_object._generate_radiative_surface_manager_for_lwr_computation(overwrite=True,
                                                                                    include_windows=True)
        assert urban_canopy_object.lwr_radiative_surface_manager.num_surface == tot_surfaces

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
        urban_canopy_object._generate_radiative_surface_manager_for_lwr_computation(include_windows=False)
        assert urban_canopy_object.lwr_radiative_surface_manager.num_surface == num_outdoor_surfaces

        # Check with windows
        urban_canopy_object._generate_radiative_surface_manager_for_lwr_computation(overwrite=True,
                                                                                    include_windows=True)
        assert urban_canopy_object.lwr_radiative_surface_manager.num_surface == tot_surfaces
