import numpy as np
from yamada.sg.geometry import compute_counter_clockwise_angle

def test_calculate_counter_clockwise_angle():

    # Reference vector; zero Radians
    reference_vector = np.array([1, 0])

    # Test vectors
    degree_0   = np.array([1, 0])  # Also degree_360
    degree_30  = np.array([np.sqrt(3) / 2, 0.5])
    degree_90  = np.array([0, 1])
    degree_135 = np.array([-np.sqrt(2)/2, np.sqrt(2)/2])
    degree_180 = np.array([-1, 0])
    degree_240 = np.array([-0.5, -np.sqrt(3)/2])
    degree_270 = np.array([0, -1])
    degree_300 = np.array([0.5, -np.sqrt(3)/2])

    # Calculate angles
    angle_0   = compute_counter_clockwise_angle(reference_vector, degree_0)
    angle_30  = compute_counter_clockwise_angle(reference_vector, degree_30)
    angle_90  = compute_counter_clockwise_angle(reference_vector, degree_90)
    angle_135 = compute_counter_clockwise_angle(reference_vector, degree_135)
    angle_180 = compute_counter_clockwise_angle(reference_vector, degree_180)
    angle_240 = compute_counter_clockwise_angle(reference_vector, degree_240)
    angle_270 = compute_counter_clockwise_angle(reference_vector, degree_270)
    angle_300 = compute_counter_clockwise_angle(reference_vector, degree_300)

    assert np.isclose(angle_0, 0) or np.isclose(angle_0, 360)
    assert np.isclose(angle_30, 30)
    assert np.isclose(angle_90, 90)
    assert np.isclose(angle_135, 135)
    assert np.isclose(angle_180, 180)
    assert np.isclose(angle_240, 240)
    assert np.isclose(angle_270, 270)
    assert np.isclose(angle_300, 300)