"""
We'll see, we need same first pass context filtering, with a different mvfc value, but the second filtering
will be much different
"""

from typing import List

from copy import deepcopy

from ladybug_geometry.geometry3d.pointvector import Point3D
from honeybee.face import Face
from honeybee.boundarycondition import Outdoors
from honeybee.model import Model
from honeybee.aperture import Aperture

from radiance_comp_vf import RadiativeSurface

from .building_context import BuildingContextFilter


class BuildingLWRContextFilter(BuildingContextFilter):
    """ todo """

    def __init__(self):
        """ todo """
        super().__init__()  # inherit from all the attributes of the super class
        # Parameters
        self._surface_id_list = []

    def select_context_surfaces_for_lwr_computation(self, building_surfaces_dict: dict,
                                                    urban_canopy_pyvista_mesh,
                                                    ray_arg):
        """ todo """

    def add_sky_and_ground_surface(self):
        """ todo """

    @property
    def outdoor_surface_id_list(self):
        return deepcopy(self._surface_id_list)

    def generate_radiative_surface_objects_from_hb_model(self, hb_model: Model,
                                                         include_windows: bool = True) -> List[
        RadiativeSurface]:
        """

        """

        radiative_surface_object_list, surface_if_list = self._generate_radiative_surface_objects_from_hb_model(
            hb_model, include_windows)
        self._surface_id_list = surface_if_list

        return radiative_surface_object_list

    @staticmethod
    def _generate_radiative_surface_objects_from_hb_model(hb_model: Model, include_windows: bool = True) -> \
            List[RadiativeSurface]:
        """ todo """

        def _get_hb_model_outdoor_surfaces(hb_model: Model) -> List[Face]:
            """
            Extract the outdoor face objects from the honeybee Model
            :param hb_model: honeybee Model
            :return: list of outdoor Face objects
            todo: to move to seperate module
            """
            outdoor_surfaces = []
            for surface in hb_model.faces:
                if isinstance(surface.boundary_condition, Outdoors):
                    outdoor_surfaces.append(surface)
            return outdoor_surfaces

        def _get_hb_model_outdoor_faces_and_apertures(hb_model: Model,
                                                      include_windows: bool = True) -> List:
            """

            todo: to move to seperate module
            """
            outdoor_hb_face_list = _get_hb_model_outdoor_surfaces(hb_model=hb_model)
            outdoor_hb_aperture_list = []
            if include_windows:
                outdoor_hb_aperture_list = [aperture for hb_face in outdoor_hb_face_list for aperture in
                                            list(hb_face.apertures)]
            hb_face_and_aperture_list = outdoor_hb_face_list + outdoor_hb_aperture_list

            return hb_face_and_aperture_list

        def _get_face_or_aperture_outdoor_lwr_properties(hb_face_or_aperture) -> (float, float, float):
            """

            :param hb_face:
            :return:
            todo: to move to seperate module
            """
            emissivity = hb_face_or_aperture.properties.energy.construction.outside_emissivity
            reflectance = 1 - emissivity

            return emissivity, reflectance

        def _from_point3d_to_list(point3d: Point3D):
            return [point3d.x, point3d.y, point3d.z]

        def _from_point3d_tuple_to_list(point3d_tuple):
            return [_from_point3d_to_list(point3d) for point3d in list(point3d_tuple)]

        hb_face_and_aperture_list = _get_hb_model_outdoor_faces_and_apertures(hb_model=hb_model,
                                                                              include_windows=include_windows)

        radiative_surface_object_list = []
        surface_if_list = []

        for surface in hb_face_and_aperture_list:
            if not (isinstance(surface, Face) or isinstance(surface, Aperture)):
                raise TypeError("The input surface is not a honeybee Face or Aperture object")

            if (isinstance(surface, Face) and not include_windows) or isinstance(surface, Aperture):
                vertex_list = _from_point3d_tuple_to_list(surface.vertices)
            else:
                vertex_list = _from_point3d_tuple_to_list(surface.punched_vertices)

            emissivity, reflectance = _get_face_or_aperture_outdoor_lwr_properties(surface)
            radiative_surface_object = RadiativeSurface.from_vertex_list_with_radiative_properties(
                identifier=surface.identifier,
                vertex_list=vertex_list, emissivity=emissivity,
                reflectance=reflectance, transmittance=0.)
            radiative_surface_object_list.append(radiative_surface_object)
            surface_if_list.append(surface.identifier)

        return radiative_surface_object_list, surface_if_list
