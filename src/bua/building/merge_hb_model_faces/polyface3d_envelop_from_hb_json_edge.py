"""
merge_faces_to_hbroom.py

Merge coplanar Ladybug Face3D objects sharing a common edge by traversing vertices
around the missing edge. Ensures correct vertex ordering and no extra stripes.

Includes:
  - merge_coplanar_faces(...)  : merge Face3D surfaces
  - merge_model_envelope(...)  : extract and merge outdoor + ground faces from HB Model

Exports HBJSONs in the parent folder of the script.

Requirements:
 - ladybug-geometry
 - honeybee-core
"""

import os
import numpy as np
from ladybug_geometry.geometry3d import Point3D, Face3D
from ladybug_geometry.geometry3d.polyface import Polyface3D
from honeybee.room import Room
from honeybee.model import Model

# -----------------------
# Geometry helper functions
# -----------------------

def _plane_key(face, tol=1e-6):
    n = face.normal
    d = -n.dot(face.vertices[0])
    return tuple(np.round(np.array([n.x, n.y, n.z, d]) / tol).astype(int))

def _edge_key(p1, p2, tol=1e-6):
    """Order-independent edge key for hashing"""
    def snap(p): return tuple(np.round(np.array([p.x, p.y, p.z]) / tol).astype(int))
    return tuple(sorted((snap(p1), snap(p2))))

def _shared_edge(f1, f2, tol=1e-6):
    """Return the first full edge shared by both faces (order-independent), else None"""
    edges_f1 = [ (f1.vertices[i], f1.vertices[(i+1)%len(f1.vertices)]) for i in range(len(f1.vertices)) ]
    edges_f2 = [ (f2.vertices[i], f2.vertices[(i+1)%len(f2.vertices)]) for i in range(len(f2.vertices)) ]
    for e1 in edges_f1:
        for e2 in edges_f2:
            if (_edge_key(e1[0], e1[1], tol) == _edge_key(e2[0], e2[1], tol)):
                return e1
    return None

# -----------------------
# Merge two faces
# -----------------------

def _merge_two_faces(f1, f2, tol=1e-6):
    """Merge two coplanar faces along a shared edge by traversing perimeter"""
    shared = _shared_edge(f1, f2, tol)
    if not shared:
        return None

    # Helper: find edge indices in a face
    def find_edge_indices(face, edge):
        n = len(face.vertices)
        for i in range(n):
            if _edge_key(face.vertices[i], face.vertices[(i+1)%n], tol) == _edge_key(edge[0], edge[1], tol):
                return i, (i+1)%n
        return None, None

        i1_start, i1_end = find_edge_indices(f1, shared)
    i2_start, i2_end = find_edge_indices(f2, shared)
    if i1_start is None or i2_start is None:
        return None

    # Determine traversal direction on f2 based on shared edge orientation
    vA, vB = shared
    if (f2.vertices[i2_start].distance_to_point(vA) < tol and f2.vertices[i2_end].distance_to_point(vB) < tol):
        # same order: traverse from i2_end + 1
        idx2 = (i2_end + 1) % len(f2.vertices)
        step2 = 1
        count2 = len(f2.vertices)
    else:
        # opposite order: traverse from i2_start - 1
        idx2 = (i2_start - 1 + len(f2.vertices)) % len(f2.vertices)
        step2 = -1
        count2 = len(f2.vertices)

    # Build merged vertex list
    new_vertices = []

    # Traverse f1 until start of shared edge
    idx = i1_start
    n1 = len(f1.vertices)
    for _ in range(n1):
        new_vertices.append(f1.vertices[idx])
        if idx == i1_start and len(new_vertices) > 1:
            break
        idx = (idx + 1) % n1
        if idx == i1_start:
            break
        if idx == i1_end:
            break

    # Traverse f2 along perimeter, skipping shared edge
    for _ in range(count2-1):
        new_vertices.append(f2.vertices[idx2])
        idx2 = (idx2 + step2) % len(f2.vertices)

    # Continue f1 after shared edge
    idx = (i1_end + 1) % n1
    while idx != i1_start:
        new_vertices.append(f1.vertices[idx])
        idx = (idx + 1) % n1

    # Remove consecutive duplicates
    merged_vertices = [new_vertices[0]]
    for v in new_vertices[1:]:
        if v.distance_to_point(merged_vertices[-1]) > tol:
            merged_vertices.append(v)

    try:
        return Face3D(merged_vertices)
    except Exception:
        return None

# -----------------------
# Merge coplanar faces
# -----------------------

def merge_coplanar_faces(faces, tol=1e-6, iterative=True):
    """Merge coplanar Face3D objects sharing a full edge"""
    def single_pass(faces_list):
        plane_groups = {}
        for f in faces_list:
            plane_groups.setdefault(_plane_key(f, tol), []).append(f)
        merged_out = []
        for group in plane_groups.values():
            merged_flags = set()
            new_faces = []
            n = len(group)
            for i in range(n):
                if i in merged_flags: continue
                f1 = group[i]
                merged = False
                for j in range(i+1, n):
                    if j in merged_flags: continue
                    f2 = group[j]
                    f = _merge_two_faces(f1, f2, tol)
                    if f:
                        new_faces.append(f)
                        merged_flags.update([i,j])
                        merged = True
                        break
                if not merged:
                    new_faces.append(f1)
            merged_out.extend(new_faces)
        return merged_out

    result = single_pass(faces)
    if iterative:
        while True:
            next_result = single_pass(result)
            if len(next_result) == len(result):
                break
            result = next_result
    return result

# -----------------------
# Merge building envelope
# -----------------------

def merge_model_envelope(hb_model, tol=1e-6, iterative=True):
    """Merge all outdoor + ground faces of a Honeybee Model to get building envelope"""
    faces = []
    for room in hb_model.rooms:
        for face in room.faces:
            bc = face.boundary_condition.name.lower()
            if bc in ("outdoors","ground"):
                faces.append(face.geometry)
    if not faces:
        raise ValueError("No outdoor/ground faces found in the model")

    print(f"Found {len(faces)} outdoor/ground faces; merging...")
    merged_faces = merge_coplanar_faces(faces, tol=tol, iterative=iterative)
    print(f"Reduced to {len(merged_faces)} merged envelope faces")

    poly = Polyface3D.from_faces(merged_faces, tolerance=tol)
    room = Room.from_polyface3d("building_envelope", poly)
    return Model("merged_envelope_model", [room])

# -----------------------
# Main test
# -----------------------

if __name__ == "__main__":
    # Example adjacent rectangles
    f1 = Face3D([Point3D(0,0,0), Point3D(2,0,0), Point3D(2,2,0), Point3D(0,2,0)])
    f2 = Face3D([Point3D(2,0,0), Point3D(4,0,0), Point3D(4,2,0), Point3D(2,2,0)])
    f3 = Face3D([Point3D(4,0,0), Point3D(6,0,0), Point3D(6,2,0), Point3D(4,2,0)])
    input_faces = [f1,f2,f3]

    merged_faces = merge_coplanar_faces(input_faces, tol=1e-6)
    print(f"Input faces: {len(input_faces)}, Merged faces: {len(merged_faces)}")

    # Polyface3D and Honeybee Rooms
    poly_input = Polyface3D.from_faces(input_faces, tolerance=1e-6)
    poly_merged = Polyface3D.from_faces(merged_faces, tolerance=1e-6)
    room_input = Room.from_polyface3d("input_room", poly_input)
    room_merged = Room.from_polyface3d("merged_room", poly_merged)
    model_input = Model("input_model", [room_input])
    model_merged = Model("merged_model", [room_merged])

    # Merge envelope from model_input
    envelope_model = merge_model_envelope(model_input, tol=1e-6)

    # Export HBJSONs to parent folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_input.to_hbjson(os.path.join(script_dir,"input_model.hbjson"))
    model_merged.to_hbjson(os.path.join(script_dir,"merged_model.hbjson"))
    envelope_model.to_hbjson(os.path.join(script_dir,"envelope_model.hbjson"))

    print("\n✅ Exported HBJSON files to parent folder:")
    print(" - input_model.hbjson")
    print(" - merged_model.hbjson")
    print(" - envelope_model.hbjson")
    print("\n👉 Load them in Honeybee Grasshopper to visualize before/after/envelope.")

    path_hbjson = r"C:\Users\elie-medioni\OneDrive\OneDrive - Technion\Ministry of Energy Research\Papers\CheckContext\LWR\Debug_context\context_building_111.hbjson"
    model =Model.from_hbjson(path_hbjson)
    envelope_model = merge_model_envelope(model, tol=1e-6)
    path_save_envelope = os.path.join(os.path.dirname(path_hbjson),"context_building_111_envelope.hbjson")
    envelope_model.to_hbjson(path_save_envelope)
