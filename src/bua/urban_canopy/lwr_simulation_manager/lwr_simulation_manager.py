"""

"""
import logging

from time import time

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
        self._vf_sim_performed = False
        self._lwr_sim_performed = False
        # Duration of the simulations
        self._vf_comp_duration: float = None
        self._lwr_sim_duration: float = None

    @property
    def is_empty(self):
        """ Check if the RadiativeSurfaceManager object is empty."""
        return self._radiative_surface_manager.is_empty

    @property
    def building_id_list(self):
        """ Check if the RadiativeSurfaceManager object is empty."""
        return self._building_id_list

    @property
    def num_surfaces(self):
        """ Number of surfaces  in the RadiativeSurfaceManager object."""
        return self._radiative_surface_manager.num_surface

    @property
    def vf_sim_performed(self):
        """ Duration of the view factor computation."""
        return self._vf_sim_performed

    @property
    def lwr_sim_performed(self):
        """ Duration of the view factor computation."""
        return self._lwr_sim_performed

    @property
    def vf_comp_duration(self):
        """ Duration of the view factor computation."""
        return self._vf_comp_duration

    @property
    def lwr_sim_duration(self):
        """ Duration of the LWR simulation."""
        return self._lwr_sim_duration

    def reset(self,lwr_only=False):
        """ Reset the RadiativeSurfaceManager object."""
        self.init_radiative_surface_manager()
        self._building_id_list = []
        self._building_outdoor_surface_id_table = []
        self._vf_sim_performed = False
        self._vf_comp_duration = None

        if lwr_only:
            self.init_ep_lwr_simulation_manager()
            self._lwr_sim_performed = False
            self._lwr_sim_duration = None

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
        if self._radiative_surface_manager.is_empty:
            logging.warning(
                "The radiative surface manager is empty, the visibility check cannot be performed.")
            return
        if self._vf_sim_performed:
            logging.warning(
                "The view factor computation has already been performed, the computation will be skipped.")
            return

        dur = time()

        # Run the simulation
        path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz = self._radiative_surface_manager.run_view_factor_computation_in_subprocess(
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

        self._vf_sim_performed = True
        self._vf_comp_duration = time() - dur

        return path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz

    def get_matrices_paths(self,path_vf_results_dir):
        """
        """

        path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz = self._radiative_surface_manager.save_vf_eps_rho_and_tau_matrices_to_npz(
            path_dir=path_vf_results_dir,return_path_npz_only=True
        )
        """ The simulation are performed in a subprocess and are not saved within the object, but the function
         only returns the paths based on the path_dir, the simulation does not need to be run for that """

        return path_vf_mtx_crs_npz, path_eps_mtx_crs_npz, path_rho_mtx_crs_npz, path_tau_mtx_crs_npz




    def initialize_ep_coupled_lwr_simulation(self, path_dir_lwr_sim: str, path_epw_file: str,
                                             path_energyplus_dir: str, path_idf_file_dict: Dict[str, str],
                                             path_vf_mtx_crs_npz: str, path_eps_mtx_crs_npz: str,
                                             path_rho_mtx_crs_npz: str, path_tau_mtx_crs_npz: str,
                                             time_step: float,
                                             tol: float = 1e-6,
                                             maxiter: int = 150, rtol=1e-5, precondition=False, num_workers=0,
                                             to_pkl=False):
        """


        """
        # Check
        if not self._vf_sim_performed:
            raise Exception(
                "The view factor computation has not been performed yet, the LWR simulation cannot be run")
        # Generate the configuration dictionary
        config_dict = self._make_config_dict_for_ep_coupled_lwr_simulation(path_dir_lwr_sim,
                                                                           path_epw_file,
                                                                           path_energyplus_dir,
                                                                           path_idf_file_dict,
                                                                           path_vf_mtx_crs_npz,
                                                                           path_eps_mtx_crs_npz,
                                                                           path_rho_mtx_crs_npz,
                                                                           path_tau_mtx_crs_npz,
                                                                           time_step=time_step,
                                                                           tol=tol,
                                                                           maxiter=maxiter, rtol=rtol,
                                                                           precondition=precondition,
                                                                           num_workers=num_workers)
        # Initialize the EP coupled LWR simulation manager and generartes the configuration file
        """
        This initialization includes some preprocessing, generating additional strings for IDF files to 
        include the LWR computation, and finally generating the adjusted idf files.
        """
        self._ep_lwr_simulation_manager, _ = self._ep_lwr_simulation_manager.set_up_coupled_lwr_simulation_from_config_dict(
            config_dict, to_pkl=to_pkl)

    def _make_config_dict_for_ep_coupled_lwr_simulation(self, path_dir_lwr_sim: str,
                                                        path_epw_file: str,
                                                        path_energyplus_dir: str,
                                                        path_idf_file_dict: Dict[str, str],
                                                        path_vf_mtx_crs_npz: str, path_eps_mtx_crs_npz: str,
                                                        path_rho_mtx_crs_npz: str, path_tau_mtx_crs_npz: str,
                                                        time_step:float,
                                                        tol: float = 1e-6,
                                                        maxiter: int = 150, rtol=1e-5, precondition=False,
                                                        num_workers=0):
        """
        Generate the configuration dictionary for the EP coupled LWR simulation.
        It is put in a separate function to generate the configuration dict and then debug the
        EpLwrSimulationManager separately.
        :param path_dir_lwr_sim: str, path to the directory where the LWR simulation will be run
        :param path_epw_file: str, path to the weather file in EPW format
        :param path_energyplus_dir: str, path to the EnergyPlus installation directory
        :param path_idf_file_dict: dict, dictionary of building_id: path_to_idf_file
         :param path_vf_mtx_crs_npz: Path to the view factor matrix in compressed sparse format.
        :param path_eps_mtx_crs_npz: Path to the emissivity matrix in compressed sparse format.
        :param path_rho_mtx_crs_npz: Path to the reflectivity matrix in compressed sparse format.
        :param path_tau_mtx_crs_npz: Path to the transmissivity matrix in compressed sparse format.
        :param time_step: int, time step in hours for the LWR simulation (e.g., 1/20 for 20 timesteps per hour)
        :param : Optional parameters for the GMRES-based matrix inversion method.
            - **tol** (float, optional): Overall inverse tolerance (default: 1e-5, valid range: 1e-10 to 1e-2).
            - **maxiter** (int, optional): Maximum number of iterations (default: 150, valid range: 1 to 1000).
            - **rtol** (float, optional): Relative tolerance within iterations on columns  (default: 5e-7, valid range: 1e-10 to 1e-5).
            - **precondition** (bool, optional): Whether to apply preconditioning (default: False).
            - **num_workerss** (int, optional): Number of parallel workers (default: 0, valid range: 0 to 64).

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
            time_step=time_step,
            tol=tol,
            maxiter=maxiter, rtol=rtol,
            precondition=precondition,
            num_workers=num_workers
        )
        return config_dict

    def run_ep_coupled_lwr_simulation(self):
        """

        """

        dur = time()
        self._ep_lwr_simulation_manager.run_lwr_coupled_simulation_in_subprocess()
        self._lwr_sim_performed = True
        self._lwr_sim_duration = time() - dur
