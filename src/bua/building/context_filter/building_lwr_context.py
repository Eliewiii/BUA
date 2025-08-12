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
        self.first_pass_done = False

    def overwrite_filtering(self, overwrite_first_pass=False, overwrite_second_pass=False):
        """
        Overwrite the filtering of the BuildingShadingContext object
        :param overwrite_first_pass: boolean to overwrite the first pass of the context filtering. If the first pass is
        overwritten, it automatically overwrites the second pass
        :param overwrite_second_pass: boolean to overwrite the second pass of the context filtering
        """
        if overwrite_first_pass:
            self.selected_context_building_id_list = []
            self.first_pass_done = False



