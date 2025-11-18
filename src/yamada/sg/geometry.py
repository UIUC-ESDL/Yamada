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

    # assert isinstance(positions, np.ndarray)
    # assert isinstance(rotation, np.ndarray)
    # assert positions.shape[1] == 3
    # assert rotation.shape == (1, 3)

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
        return np.hypot(v[0], v[1])

    def dot_product(v, w):
        return v[0] * w[0] + v[1] * w[1]

    def determinant(v, w):
        return v[0] * w[1] - v[1] * w[0]

    # Basic values
    dot = dot_product(vector_a, vector_b)
    det = determinant(vector_a, vector_b)

    # Lengths
    la = length(vector_a)
    lb = length(vector_b)

    # Perfectly collinear
    if det == 0:

        # In the same direction
        if dot > 0:
            return 0.0

        # In the opposite direction
        else:
            return 180.0

    # Compute generic angle
    cosx = dot / (la * lb)

    # Clamp for floating-point safety
    cosx = max(min(cosx, 1.0), -1.0)

    angle = np.degrees(np.arccos(cosx))

    # If the determinant is < 0, then B is clockwise of A
    if det > 0:
        return angle

    # If the determinant is > 0, then A is clockwise of B, so return the reflex angle
    else:
        return 360.0 - angle


def compute_counter_clockwise_angles(reference_vector, vectors):
    ccw_angles = []
    for vector in vectors:
        ccw_angle = compute_counter_clockwise_angle(reference_vector, vector)
        ccw_angles.append(ccw_angle)
    return ccw_angles


def identify_overlapping_edges(pos, edge_pairs):

    # Validate Inputs
    assert isinstance(pos, dict)
    assert all(isinstance(v, np.ndarray) and v.shape == (3,) for v in pos.values())
    assert all(isinstance(edge, tuple) and len(edge) == 2 for edge in edge_pairs)

    # Initialize outputs
    crossings = {}
    invalid   = False

    for edge_1, edge_2 in edge_pairs:

        # Unpack edges
        a, b = edge_1
        c, d = edge_2

        # 3D positions in this projection
        pos_a_3D = pos[a]
        pos_b_3D = pos[b]
        pos_c_3D = pos[c]
        pos_d_3D = pos[d]

        # 2D projections to XZ plane
        pos_a_2D = pos_a_3D[[0, 2]]
        pos_b_2D = pos_b_3D[[0, 2]]
        pos_c_2D = pos_c_3D[[0, 2]]
        pos_d_2D = pos_d_3D[[0, 2]]

        # Compute 2D segment intersection
        min_dist, min_dist_pos, _ = compute_line_segment_intersection(pos_a_2D, pos_b_2D, pos_c_2D, pos_d_2D)

        # Early reject if they don't intersect (in 2D)
        if not np.isclose(min_dist, 0.0):
            continue

        # Ensure the crossing is not at an endpoint
        intersects_at_endpoint = any([np.allclose(min_dist_pos, pos_a_2D),
                                      np.allclose(min_dist_pos, pos_b_2D),
                                      np.allclose(min_dist_pos, pos_c_2D),
                                      np.allclose(min_dist_pos, pos_d_2D)])

        # If edges intersect at an endpoint, mark as invalid and try another projection plane
        if intersects_at_endpoint:
            invalid = True
            break

        # Given a pair of 3D edges that intersect when projected onto a 2D plane,
        # find the 3D point along each edge that corresponds to this intersection.
        x_intersect, z_intersect = min_dist_pos
        y_ab     = compute_intermediate_y_position(pos_a_3D, pos_b_3D, x_int=x_intersect, z_int=z_intersect)
        y_cd     = compute_intermediate_y_position(pos_c_3D, pos_d_3D, x_int=x_intersect, z_int=z_intersect)
        pos_x_ab = np.array([x_intersect, y_ab, z_intersect])
        pos_x_cd = np.array([x_intersect, y_cd, z_intersect])

        # Define label and store crossing
        label = f"crossing_{len(crossings)}"

        # Define which strand is in front of the other
        # Left-handed convention (+y pointing away from the viewer)
        # Probably should switch to right-handed convention later, but some tests are hard-coded.
        edge_order = ["over", "under"] if pos_x_ab[1] < pos_x_cd[1] else ["under", "over"]

        crossings[label] = {
                            "edges":       (edge_1, edge_2),
                            "edge_order":  edge_order,
                            "pos_2D":      np.array([x_intersect, z_intersect]),
                            "pos_3D":      [pos_x_ab, pos_x_cd],
                            }

    return crossings, invalid