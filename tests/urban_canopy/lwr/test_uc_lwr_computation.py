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

    def test_set_up_lwr_simulation(self, init_urban_canopy_with_one_buildingmodel):
        """

        """
        urban_canopy_object = init_urban_canopy_with_one_buildingmodel
        SimulationLWR.generate_radiative_surface_manager_for_lwr_computation(urban_canopy_object,
                                                                             overwrite=True,
                                                                             include_windows=True)
        path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz = SimulationLWR.perform_lwr_vf_computation(
            urban_canopy_object, overwrite=True)

        # Set up the LWR simulation
        SimulationLWR.set_up_lwr_simulation(urban_canopy_object,
                                            path_energyplus_dir="C:\EnergyPlusV23-2-0",
                                            path_vf_mtx_crs_npz=path_vf_mtx_crs_npz,
                                            path_eps_mtx_crs_npz=path_eps_mtx_crs_npz,
                                            path_rho_mtx_crs_npz=path_rho_mtx_crs_npz,
                                            path_tau_mtx_crs_npz=path_tau_mtx_crs_npz,
                                            hourly_report_frequency=True,
                                            num_time_steps_per_hour=20,

                                            to_pkl=True
                                            )

        assert urban_canopy_object.lwr_simulation_manager.num_surfaces == urban_canopy_object.lwr_simulation_manager._ep_lwr_simulation_manager.num_outdoor_surfaces
