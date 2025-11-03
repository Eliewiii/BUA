"""
merge_faces_to_hbroom.py

Simple edge-based merging of coplanar Ladybug Face3D objects.
Includes:
  - merge_coplanar_faces(...)  : merge Face3D surfaces
  - merge_model_envelope(...)  : extract and merge Outdoor+Ground faces from HB Model

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


# ===============================================================
# === CORE GEOMETRY MERGING =====================================
# ===============================================================

def _plane_key(face, tol=1e-6):
    n = face.normal
    d = -n.dot(face.vertices[0])
    return tuple(np.round(np.array([n.x, n.y, n.z, d]) / tol).astype(int))


def _edge_key(p1, p2, tol=1e-6):
    def snap(p): return tuple(np.round(np.array([p.x, p.y, p.z]) / tol).astype(int))
    return tuple(sorted((snap(p1), snap(p2))))


def _merge_two_faces(f1, f2, tol=1e-6):
    """Try to merge two coplanar faces that share a full edge (with direction + proximity checks)."""
    v1, v2 = list(f1.vertices), list(f2.vertices)
    shared = None

    for i in range(len(v1)):
        p1a, p1b = v1[i], v1[(i + 1) % len(v1)]
        e1_vec = p1b - p1a
        e1_mid = Point3D((p1a.x + p1b.x) / 2, (p1a.y + p1b.y) / 2, (p1a.z + p1b.z) / 2)

        for j in range(len(v2)):
            p2a, p2b = v2[j], v2[(j + 1) % len(v2)]
            e2_vec = p2b - p2a
            e2_mid = Point3D((p2a.x + p2b.x) / 2, (p2a.y + p2b.y) / 2, (p2a.z + p2b.z) / 2)

            # 1️⃣ edge endpoints must match within tol
            same_endpoints = (
                (p1a.distance_to_point(p2a) < tol and p1b.distance_to_point(p2b) < tol) or
                (p1a.distance_to_point(p2b) < tol and p1b.distance_to_point(p2a) < tol)
            )
            if not same_endpoints:
                continue

            # 2️⃣ midpoint proximity (avoid merging distant edges)
            if e1_mid.distance_to_point(e2_mid) > tol:
                continue

            # 3️⃣ normals must be parallel (not necessarily same direction)
            n1, n2 = f1.normal, f2.normal
            if abs(n1.dot(n2)) < 1 - 1e-3:
                continue

            # 4️⃣ edge direction opposite (faces should face opposite along edge)
            e1n = e1_vec.normalize()
            e2n = e2_vec.normalize()
            if abs(e1n.dot(e2n) + 1) > 1e-3:
                continue

            shared = (p1a, p1b)
            break
        if shared:
            break

    if not shared:
        return None

    # Remove the shared edge from both faces
    def remove_edge(verts, e):
        res = []
        for k in range(len(verts)):
            ek = _edge_key(verts[k], verts[(k + 1) % len(verts)], tol)
            if ek != _edge_key(e[0], e[1], tol):
                res.append(verts[k])
        return res

    verts_combined = remove_edge(v1, shared) + remove_edge(v2, shared)

    # Order vertices around plane
    plane = f1.plane
    origin, x_axis, y_axis = plane.o, plane.x, plane.y
    pts_2d = np.array([[(p - origin).dot(x_axis), (p - origin).dot(y_axis)] for p in verts_combined])
    centroid = np.mean(pts_2d, axis=0)
    angles = np.arctan2(pts_2d[:, 1] - centroid[1], pts_2d[:, 0] - centroid[0])
    ordered = [verts_combined[i] for i in np.argsort(angles)]

    try:
        return Face3D(ordered)
    except Exception as e:
        print(f"⚠️  Could not create merged face: {e}")
        return None


def merge_coplanar_faces(faces, tol=1e-6, iterative=True):
    """Merge coplanar Face3D objects that share a full edge."""
    def single_pass(faces_list):
        plane_groups = {}
        for f in faces_list:
            plane_groups.setdefault(_plane_key(f, tol), []).append(f)

        result = []
        for group in plane_groups.values():
            edge_map, merged_ids, new_faces = {}, set(), []
            for i, f in enumerate(group):
                for j in range(len(f.vertices)):
                    ek = _edge_key(f.vertices[j], f.vertices[(j + 1) % len(f.vertices)], tol)
                    edge_map.setdefault(ek, []).append(i)

            for ek, fids in edge_map.items():
                if len(fids) == 2:
                    a, b = fids
                    if a in merged_ids or b in merged_ids:
                        continue
                    merged = _merge_two_faces(group[a], group[b], tol)
                    if merged:
                        new_faces.append(merged)
                        merged_ids.update([a, b])

            for i, f in enumerate(group):
                if i not in merged_ids:
                    new_faces.append(f)
            result.extend(new_faces)
        return result

    result = single_pass(faces)
    if iterative:
        while True:
            next_result = single_pass(result)
            if len(next_result) == len(result):
                break
            result = next_result
    return result


# ===============================================================
# === MERGE ENVELOPE FROM HONEYBEE MODEL ========================
# ===============================================================

def merge_model_envelope(hb_model, tol=1e-6, iterative=True):
    """
    Merge all outdoor + ground faces of a Honeybee Model to form an envelope.
    Returns a new Honeybee Model with a single Room made of merged faces.
    """
    faces = []
    for room in hb_model.rooms:
        for face in room.faces:
            bc = face.boundary_condition.name.lower()
            if bc in ("outdoors", "ground"):
                faces.append(face.geometry)

    if not faces:
        raise ValueError("No outdoor or ground faces found in the model.")

    print(f"Found {len(faces)} outdoor/ground faces; merging...")

    merged_faces = merge_coplanar_faces(faces, tol=tol, iterative=iterative)
    print(f"Reduced to {len(merged_faces)} merged envelope faces.")

    poly = Polyface3D.from_faces(merged_faces, tolerance=tol)
    room = Room.from_polyface3d("building_envelope", poly)
    return Model("merged_envelope_model", [room])


# ===============================================================
# === MAIN TEST =================================================
# ===============================================================

if __name__ == "__main__":
    # Simple test with a few adjacent rectangles
    f1 = Face3D([
        Point3D(0, 0, 0), Point3D(2, 0, 0),
        Point3D(2, 2, 0), Point3D(0, 2, 0)
    ])
    f2 = Face3D([
        Point3D(2, 0, 0), Point3D(4, 0, 0),
        Point3D(4, 2, 0), Point3D(2, 2, 0)
    ])
    f3 = Face3D([
        Point3D(4, 0, 0), Point3D(6, 0, 0),
        Point3D(6, 2, 0), Point3D(4, 2, 0)
    ])
    input_faces = [f1, f2, f3]

    merged_faces = merge_coplanar_faces(input_faces, tol=1e-6)

    poly_input = Polyface3D.from_faces(input_faces, tolerance=1e-6)
    poly_merged = Polyface3D.from_faces(merged_faces, tolerance=1e-6)
    room_input = Room.from_polyface3d("input_room", poly_input)
    room_merged = Room.from_polyface3d("merged_room", poly_merged)

    model_input = Model("input_model", [room_input])
    model_merged = Model("merged_model", [room_merged])

    # === NEW: Test the merge_model_envelope() function ===
    # Pretend model_input is a building with outdoor faces
    envelope_model = merge_model_envelope(model_input, tol=1e-6)

    # Save all models to parent folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_input.to_hbjson(os.path.join(script_dir, "input_model.hbjson"))
    model_merged.to_hbjson(os.path.join(script_dir, "merged_model.hbjson"))
    envelope_model.to_hbjson(os.path.join(script_dir, "envelope_model.hbjson"))

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
