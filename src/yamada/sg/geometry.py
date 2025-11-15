import numpy as np
from numpy import sin, cos


def rotate(positions: np.ndarray,
           rotation: np.ndarray) -> np.ndarray:
    """
    Rotates a set of points about the first 3D point in the array.

    :param positions: A numpy array of 3D points.
    :param rotation: A numpy array of 3 Euler angles in radians.

    :return: new_positions:
    """

    # Shift the object to origin
    reference_position = positions[0]
    origin_positions = positions - reference_position

    alpha, beta, gamma = rotation

    # Rotation matrix Euler angle convention r = r_z(gamma) @ r_y(beta) @ r_x(alpha)

    r_x = np.array([[1., 0., 0.],
                    [0., cos(alpha), -sin(alpha)],
                    [0., sin(alpha), cos(alpha)]])

    r_y = np.array([[cos(beta), 0., sin(beta)],
                    [0., 1., 0.],
                    [-sin(beta), 0., cos(beta)]])

    r_z = np.array([[cos(gamma), -sin(gamma), 0.],
                    [sin(gamma), cos(gamma), 0.],
                    [0., 0., 1.]])

    r = r_z @ r_y @ r_x

    # Transpose positions from [[x1,y1,z1],[x2... ] to [[x1,x2,x3],[y1,... ]
    rotated_origin_positions = (r @ origin_positions.T).T

    # Shift back from origin
    new_positions = rotated_origin_positions + reference_position

    rotated_node_positions = new_positions

    return rotated_node_positions


def compute_line_segment_intersection(a: np.ndarray,
                                      b: np.ndarray,
                                      c: np.ndarray,
                                      d: np.ndarray) -> tuple[float, np.ndarray]:
    """
    Returns the minimum Euclidean distance between two line segments and its position.

    This function also works for calculating the distance between a line segment and a point and a point and point.

    Based on the algorithm described in:

    Vladimir J. Lumelsky,
    "On Fast Computation of Distance Between Line Segments",
    Information Processing Letters 21 (1985) 55-61
    https://doi.org/10.1016/0020-0190(85)90032-8

    Values 0 <= t <= 1 correspond to points being inside segment AB whereas values < 0  correspond to being 'left' of AB
    and values > 1 correspond to being 'right' of AB.

    Values 0 <= u <= 1 correspond to points being inside segment CD whereas values < 0  correspond to being 'left' of CD
    and values > 1 correspond to being 'right' of CD.

    Step 1: Check for special cases; compute D1, D2, and the denominator in (11)
        (a) If one of the two segments degenerates into a point, assume that this segment corresponds to the parameter
        u, take u=0, and go to Step 4.
        (b) If both segments degenerate into points, take t=u=0, and go to Step 5.
        (c) If neither of two segments degenerates into a point and the denominator in (11) is zero, take t=0 and go to
        Step 3.
        (d) If none of (a), (b), (c) takes place, go to Step 2.
    Step 2: Using (11) compute t. If t is not in the range [0,1], modify t using (12).
    Step 3: Using (10) compute u. If u is not in the range [0,1], modify u using (12); otherwise, go to Step 5.
    Step 4: Using (10) compute t. If t is not in the range [0,1], modify t using (12).
    Step 5: With current values of t and u, compute the actual MinD using (7).

    :param a: (1,3) numpy array
    :param b: (1,3) numpy array
    :param c: (1,3) numpy array
    :param d: (1,3) numpy array

    :return: Minimum distance between line segments, float
    :return: Position of minimum distance, (1,3) numpy array
    """

    # Validate inputs
    # assert all(isinstance(pt, np.ndarray) for pt in [a, b, c, d]), "All input points must be numpy arrays"
    # assert all(pt.shape == (1,3)          for pt in [a, b, c, d]), "All input points must be of shape (1,3)"
    # assert all(pt.dtype == np.float64     for pt in [a, b, c, d]), "All input points must be of type np.float64"

    def clamp_bound(num):
        """
        If the number is outside the range [0,1] then clamp it to the nearest boundary.
        """
        if num < 0.:
            return 0.
        elif num > 1.:
            return 1.
        else:
            return num

    d1  = b - a
    d2  = d - c
    d12 = c - a

    D1  = np.dot(d1, d1.T)
    D2  = np.dot(d2, d2.T)
    S1  = np.dot(d1, d12.T)
    S2  = np.dot(d2, d12.T)
    R   = np.dot(d1, d2.T)
    den = D1 * D2 - R**2

    # Check if one or both line segments are points
    if D1 == 0. or D2 == 0.:

        # Both AB and CD are points
        if D1 == 0. and D2 == 0.:
            t = 0.
            u = 0.

        # AB is a line segment and CD is a point
        elif D1 != 0.:
            u = 0.
            t = S1 / D1
            t = clamp_bound(t)

        # AB is a point and CD is a line segment
        elif D2 != 0.:
            t = 0.
            u = -S2 / D2
            u = clamp_bound(u)

    # Check if line segments are parallel
    elif den == 0.:
        t = 0.
        u = -S2 / D2
        uf = clamp_bound(u)

        if uf != u:
            t = (uf * R + S1) / D1
            t = clamp_bound(t)
            u = uf

    # General case for calculating the minimum distance between two line segments
    else:

        t = (S1 * D2 - S2 * R) / den

        t = clamp_bound(t)

        u = (t * R - S2) / D2
        uf = clamp_bound(u)

        if uf != u:
            t = (uf * R + S1) / D1
            t = clamp_bound(t)

            u = uf

    min_dist = np.linalg.norm(d1 * t - d2 * u - d12)

    pos_ab = a + d1 * t
    pos_cd = c + d2 * u

    return min_dist, pos_ab, pos_cd


def compute_intermediate_y_position(a:     np.ndarray,
                                    b:     np.ndarray,
                                    x_int: float,
                                    z_int: float) -> float:
    """
    Calculates the intermediate y position given two points and the intermediate x and z position.
    """

    x1, y1, z1 = a
    x2, y2, z2 = b

    delta_x = x2 - x1
    delta_y = y2 - y1
    delta_z = z2 - z1

    if delta_x == 0 and delta_z == 0:
        raise ValueError("The XZ projection of these two points overlap. This projection is not valid.")

    elif delta_x != 0:
        ratio_x = (x_int - x1) / delta_x
        y_int = y1 + ratio_x * delta_y

    elif delta_z != 0:
        ratio_z = (z_int - z1) / delta_z
        y_int = y1 + ratio_z * delta_y

    else:
        raise ValueError("This should not happen.")

    return y_int


def compute_3D_intersection(a0_position, a1_position, a2_position, a3_position, x0z_coords):
    """
    If two 3D lines are projected onto the XZ plane and their projections intersect, then
    calculate the corresponding 3D coordinates of that intersection point for the two lines.
    """

    # Unpack the coordinates
    x0, y0, z0 = a0_position
    x1, y1, z1 = a1_position
    x2, y2, z2 = a2_position
    x3, y3, z3 = a3_position
    xc, yc, zc = x0z_coords

    # Changes in position
    dx02 = x2 - x0
    dy02 = y2 - y0
    dz02 = z2 - z0
    dx13 = x3 - x1
    dy13 = y3 - y1
    dz13 = z3 - z1

    # Relative position of the crossing
    if dx02 != 0:
        t02 = (xc - x0) / dx02
    elif dy02 != 0:
        t02 = (yc - y0) / dy02
    elif dz02 != 0:
        t02 = (zc - z0) / dz02
    else:
        raise ValueError("The start and stop nodes have the same position")

    if dx13 != 0:
        t13 = (xc - x1) / dx13
    elif dy13 != 0:
        t13 = (yc - y1) / dy13
    elif dz13 != 0:
        t13 = (zc - z1) / dz13
    else:
        raise ValueError("The start and stop nodes have the same position")

    # Calculate the 3D position of the crossing
    y_c_02 = y0 + t02 * dy02
    y_c_13 = y1 + t13 * dy13

    position_c_02 = np.array([xc, y_c_02, zc])
    position_c_13 = np.array([xc, y_c_13, zc])

    return position_c_02, position_c_13


def compute_counter_clockwise_angle(vector_a, vector_b):
    """
    Returns the counter-clockwise angle (in degrees) between the two vectors.
    """

    # Validate inputs
    assert isinstance(vector_a, np.ndarray)
    assert isinstance(vector_b, np.ndarray)
    assert vector_a.shape == (2,)
    assert vector_b.shape == (2,)

    def length(v):
        return np.sqrt(v[0] ** 2 + v[1] ** 2)

    def dot_product(v, w):
        return v[0] * w[0] + v[1] * w[1]

    def determinant(v, w):
        return v[0] * w[1] - v[1] * w[0]

    def inner_angle(v, w):
        cosx = dot_product(v, w) / (length(v) * length(w))
        rad = np.arccos(cosx)     # in radians
        return rad * 180 / np.pi  # returns degrees

    inner = inner_angle(vector_a, vector_b)
    det   = determinant(vector_a, vector_b)

    # If the determinant is < 0, then B is clockwise of A
    if det > 0:
        return inner
    # If the determinant is > 0, then A is clockwise of B
    else:
        return 360 - inner

def compute_counter_clockwise_angles(reference_vector, vectors):
    ccw_angles = []
    for vector in vectors:
        ccw_angle = compute_counter_clockwise_angle(reference_vector, vector)
        ccw_angles.append(ccw_angle)
    return ccw_angles


def identify_overlapping_edges(pos3D_rot, nonadjacent_edge_pairs, atol=1e-4):
    crossings = {}
    invalid = False

    for edge_1, edge_2 in nonadjacent_edge_pairs:
        # Unpack edges
        a, b = edge_1
        c, d = edge_2

        # 3D positions in this projection
        pos_a_3D = pos3D_rot[a]
        pos_b_3D = pos3D_rot[b]
        pos_c_3D = pos3D_rot[c]
        pos_d_3D = pos3D_rot[d]

        # 2D projections to XZ plane
        pos_a_2D = pos_a_3D[[0, 2]]
        pos_b_2D = pos_b_3D[[0, 2]]
        pos_c_2D = pos_c_3D[[0, 2]]
        pos_d_2D = pos_d_3D[[0, 2]]

        # Compute 2D segment intersection
        min_dist, min_dist_pos, _ = compute_line_segment_intersection(
            pos_a_2D, pos_b_2D, pos_c_2D, pos_d_2D
        )

        # Early reject if they don't intersect (in 2D)
        if not np.isclose(min_dist, 0.0, atol=atol):
            continue

        # Ensure the crossing is not at an endpoint
        at_endpoint = any([
            np.allclose(min_dist_pos, pos_a_2D, atol=atol),
            np.allclose(min_dist_pos, pos_b_2D, atol=atol),
            np.allclose(min_dist_pos, pos_c_2D, atol=atol),
            np.allclose(min_dist_pos, pos_d_2D, atol=atol),
        ])
        if at_endpoint:
            # This projection is “bad” (you were printing and rejecting in project())
            invalid = True
            break

        # Compute y-coordinates at the intersection for each 3D segment
        x_int, z_int = min_dist_pos
        y_ab = compute_intermediate_y_position(pos_a_3D, pos_b_3D, x_int=x_int, z_int=z_int)
        y_cd = compute_intermediate_y_position(pos_c_3D, pos_d_3D, x_int=x_int, z_int=z_int)

        pos_x_ab = np.array([x_int, y_ab, z_int])
        pos_x_cd = np.array([x_int, y_cd, z_int])

        # Define label and store crossing
        edges = (edge_1, edge_2)
        label = f"crossing_{len(crossings)}"

        # Define over/under based on y position
        # (keep your existing convention)
        orientation = ["over", "under"] if pos_x_ab[1] < pos_x_cd[1] else ["under", "over"]

        crossings[label] = {
            "edges": edges,
            "pos_3D": [pos_x_ab, pos_x_cd],
            "orientation": orientation,
            "pos_2D": np.array([x_int, z_int]),
        }

    return crossings, invalid