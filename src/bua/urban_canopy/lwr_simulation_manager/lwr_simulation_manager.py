"""

"""
import logging

from typing import List, Dict

from honeybee.model import Model

from radiance_comp_vf import RadiativeSurfaceManager
from lwrepcoupling import EpLwrSimulationManager

from .utils_hb_model_to_radiative_surfaces import generate_radiative_surface_objects_from_hb_model


class LwrSimulationManager:

    def __init__(self):
        """

        """
        self._radiative_surface_manager = RadiativeSurfaceManager()
        self._ep_lwr_simulation_manager = EpLwrSimulationManager()
        #
        self._building_id_list = []
        self._building_outdoor_surface_id_table: List[List[str]] = []
        #
        self.vf_sim_performed = False
        self.lwr_sim_performed = False

    @property
    def is_empty(self):
        """ Check if the RadiativeSurfaceManager object is empty."""
        return self._radiative_surface_manager.is_empty

    def reset(self):
        """ Reset the RadiativeSurfaceManager object."""
        self.init_radiative_surface_manager()
        self.init_ep_lwr_simulation_manager()
        self._building_id_list = []
        self._building_outdoor_surface_id_table = []
        self.vf_sim_performed = False
        self.lwr_sim_performed = False

    def init_radiative_surface_manager(self):
        """ Reinitialize the RadiativeSurfaceManager object if needed. """
        self._radiative_surface_manager = RadiativeSurfaceManager()

    def init_ep_lwr_simulation_manager(self):
        """ Reinitialize the EpLwrSimulationManager object if needed. """
        self._ep_lwr_simulation_manager = EpLwrSimulationManager()

    def add_building(self, building_id: str, hb_model: Model, include_windows: bool = True):
        """

        """
        radiative_surface_object_list, surface_id_list = generate_radiative_surface_objects_from_hb_model(
            hb_model, include_windows)

        self._radiative_surface_manager.add_radiative_surfaces(radiative_surface_object_list)
        self._building_id_list.append(building_id)
        self._building_outdoor_surface_id_table.append(surface_id_list)

    def run_vf_computation(self, path_vf_computation_temp_dir: str, path_vf_results_dir: str,
                               num_worker_cpu_bound: int = 0,
                               num_worker_io_bound: int = 0,
                               num_rays: int = 100000,
                               mvfc_check: bool = True,
                               mvfc: float = None,
                               ray_traced_check: bool = True,
                               ray_tracing_among_all_corners: bool = False,
                               num_receiver_per_file: int = 40,
                               overwrite_folders: bool = False,
                               consider_octree: bool = True,
                               one_octree_for_all: bool = False,
                               save_to_pkl: bool = False):
        """

        """
        if self.radiative_surface_manager.is_empty:
            logging.warning(
                "The radiative surface manager is empty, the visibility check cannot be performed.")
            return
        if self.vf_sim_performed:
            logging.warning(
                "The view factor computation has already been performed, the computation will be skipped.")
            return

        # Run the simulation
        path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz = self.radiative_surface_manager.run_view_factor_computation_in_subprocess(
            path_simulation_folder=path_vf_computation_temp_dir,
            path_result_folder=path_vf_results_dir,
            num_worker_cpu_bound=num_worker_cpu_bound,
            num_worker_io_bound=num_worker_io_bound,
            num_rays=num_rays,
            mvfc_check=mvfc_check,
            mvfc=mvfc,
            ray_traced_check=ray_traced_check,
            ray_tracing_among_all_corners=ray_tracing_among_all_corners,
            num_receiver_per_file=num_receiver_per_file,
            overwrite_folders=overwrite_folders,
            consider_octree=consider_octree,
            one_octree_for_all=one_octree_for_all,
            save_to_pkl=save_to_pkl)
        # Check if the simulation succeeded
        # todo add a check for the simulation success

        self.vf_sim_performed = True

        return path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz

    def initialize_ep_coupled_lwr_simulation(self, path_dir_lwr_sim: str, path_epw_file: str,
                                             path_energyplus_dir: str, path_idf_file_dict: Dict[str, str],
                                             path_vf_mtx_crs_npz: str, path_eps_mtx_crs_npz: str,
                                             path_rho_mtx_crs_npz: str, path_tau_mtx_crs_npz: str,
                                             tol: float = 1e-6,
                                             maxiter: int = 150, rtol=1e-5, precondition=False, num_worker=0):
        """

        """
        # Check
        if not self.vf_sim_performed:
            raise Exception(
                "The view factor computation has not been performed yet, the LWR simulation cannot be run")
        # Generate the configuration dictionary
        config_dict = self.make_config_dict_for_ep_coupled_lwr_simulation(path_dir_lwr_sim,
                                                                          path_epw_file,
                                                                          path_energyplus_dir,
                                                                          path_idf_file_dict,
                                                                          path_vf_mtx_crs_npz,
                                                                          path_eps_mtx_crs_npz,
                                                                          path_rho_mtx_crs_npz,
                                                                          path_tau_mtx_crs_npz, tol=tol,
                                                                          maxiter=maxiter, rtol=rtol,
                                                                          precondition=precondition,
                                                                          num_worker=num_worker)
        # Initialize the EP coupled LWR simulation manager and generartes the configuration file
        """
        This initialization includes some preprocessing, generating additional strings for IDF files to 
        include the LWR computation, and finally generating the adjusted idf files.
        """
        self._ep_lwr_simulation_manager.set_up_coupled_lwr_simulation_from_config_file(config_dict)

    def make_config_dict_for_ep_coupled_lwr_simulation(self, path_dir_lwr_sim: str,
                                                       path_epw_file: str,
                                                       path_energyplus_dir: str,
                                                       path_idf_file_dict: Dict[str, str],
                                                       path_vf_mtx_crs_npz: str, path_eps_mtx_crs_npz: str,
                                                       path_rho_mtx_crs_npz: str, path_tau_mtx_crs_npz: str,
                                                       tol: float = 1e-6,
                                                       maxiter: int = 150, rtol=1e-5, precondition=False,
                                                       num_worker=0):
        """
        Generate the configuration dictionary for the EP coupled LWR simulation.
        It is put in a separate function to generate the configuration dict and then debug the
        EpLwrSimulationManager separately.
        :param path_dir_lwr_sim: str, path to the directory where the LWR simulation will be run
        :param path_idf_file_dict: dict, dictionary of building_id: path_to_idf_file
         :param path_vf_mtx_crs_npz: Path to the view factor matrix in compressed sparse format.
        :param path_eps_mtx_crs_npz: Path to the emissivity matrix in compressed sparse format.
        :param path_rho_mtx_crs_npz: Path to the reflectivity matrix in compressed sparse format.
        :param path_tau_mtx_crs_npz: Path to the transmissivity matrix in compressed sparse format.
        :param : Optional parameters for the GMRES-based matrix inversion method.
            - **tol** (float, optional): Overall inverse tolerance (default: 1e-5, valid range: 1e-10 to 1e-2).
            - **maxiter** (int, optional): Maximum number of iterations (default: 150, valid range: 1 to 1000).
            - **rtol** (float, optional): Relative tolerance within iterations on columns  (default: 5e-7, valid range: 1e-10 to 1e-5).
            - **precondition** (bool, optional): Whether to apply preconditioning (default: False).
            - **num_workers** (int, optional): Number of parallel workers (default: 0, valid range: 0 to 64).

        """
        list_path_idf_file = [path_idf_file_dict[building_id] for building_id in self._building_id_list]
        config_dict = self._ep_lwr_simulation_manager.make_config_dict(
            path_dir_outputs=path_dir_lwr_sim,
            path_epw_file=path_epw_file,
            path_energyplus_dir=path_energyplus_dir,
            list_building_id=self._building_id_list,
            list_path_idf_file=list_path_idf_file,
            list_of_list_outdoor_surface_name=self._building_outdoor_surface_id_table,
            path_vf_mtx_crs_npz=path_vf_mtx_crs_npz,
            path_eps_mtx_crs_npz=path_eps_mtx_crs_npz,
            path_rho_mtx_crs_npz=path_rho_mtx_crs_npz,
            path_tau_mtx_crs_npz=path_tau_mtx_crs_npz,
            tol=tol,
            maxiter=maxiter, rtol=rtol,
            precondition=precondition,
            num_worker=num_worker
        )
        return config_dict

    def run_ep_coupled_lwr_simulation(self):
        """

        """
        self._ep_lwr_simulation_manager.run_lwr_coupled_simulation_in_subprocess()
