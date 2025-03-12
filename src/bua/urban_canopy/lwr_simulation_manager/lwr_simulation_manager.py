"""

"""
import logging

from typing import List

from honeybee.model import Model

from radiance_comp_vf import RadiativeSurfaceManager
from lwrepcoupling import EpLwrSimulationManager

from .utils_hb_model_to_radiative_surfaces import generate_radiative_surface_objects_from_hb_model


class LwrSimulationManager:

    def __init__(self):
        self._radiative_surface_manager = RadiativeSurfaceManager()
        self._ep_lwr_simulation_manager = EpLwrSimulationManager()
        #
        self._building_id_list = []
        self._building_outdoor_surface_id_table: List[List[str]] = []

    def init_radiative_surface_manager(self):
        pass

    def init_ep_lwr_simulation_manager(self):
        pass

    def add_building(self, building_id: str, hb_model: Model, include_windows: bool = True):
        """

        """
        radiative_surface_object_list, surface_id_list = generate_radiative_surface_objects_from_hb_model(
            hb_model, include_windows)

        self._radiative_surface_manager.add_radiative_surfaces(radiative_surface_object_list)
        self._building_id_list.append(building_id)
        self._building_outdoor_surface_id_table.append(surface_id_list)

    def perform_vf_computation(self,path_vf_computation_temp_dir: str,path_vf_results_dir: str, **kwargs):
        """

        """
        if self.radiative_surface_manager.is_empty:
            logging.warning(
                "The radiative surface manager is empty, the visibility check cannot be performed.")
            return

        # Run the simulation
        path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz = self.radiative_surface_manager.run_view_factor_computation_in_subprocess(
            path_simulation_folder=path_vf_computation_temp_dir,
            path_result_folder=path_vf_results_dir, **kwargs)
        # Check if the simulation succeeded
        # todo add a check for the simulation success

        return path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz


    def initialize_ep_coupled_lwr_simulation(self):
        pass

    def run_ep_coupled_lwr_simulation(self):
        pass
