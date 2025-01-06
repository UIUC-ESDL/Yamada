import numpy as np
from yamada.geometry import rotate

def test_rotation_at_origin_zero():

    # Define a unit cube
    component_positions = np.array([[0, 0, 0],  # a
                                    [1, 0, 0],  # b
                                    [1, 1, 0],  # c
                                    [0, 1, 0],  # d

                                    [0, 0, 1],  # e
                                    [1, 0, 1],  # f
                                    [1, 1, 1],  # g
                                    [0, 1, 1]])  # h

    # Rotate about the origin by 0 degrees
    rotate_zero = np.array([0, 0, 0])

    # Rotate the cube

    rotated_component_positions = rotate(component_positions, rotate_zero)

    expected_rotated_component_positions_zero = np.array([[0, 0, 0],  # a
                                                          [1, 0, 0],  # b
                                                          [1, 1, 0],  # c
                                                          [0, 1, 0],  # d

                                                          [0, 0, 1],  # e
                                                          [1, 0, 1],  # f
                                                          [1, 1, 1],  # g
                                                          [0, 1, 1]])  # h

    assert np.allclose(rotated_component_positions, expected_rotated_component_positions_zero)


def test_rotation_at_origin_z_90():

    # Define a unit cube
    component_positions = np.array([[0, 0, 0],  # a
                                    [1, 0, 0],  # b
                                    [1, 1, 0],  # c
                                    [0, 1, 0],  # d

                                    [0, 0, 1],  # e
                                    [1, 0, 1],  # f
                                    [1, 1, 1],  # g
                                    [0, 1, 1]])  # h


    # Rotate about the z-axis by 90 degrees
    rotate_z_90 = np.array([0, 0, np.pi/2])


    # Rotate the cube

    rotated_component_positions = rotate(component_positions, rotate_z_90)

    expected_rotated_component_positions_z_90 = np.array([[0, 0, 0],  # a
                                                          [0, 1, 0],  # b
                                                          [-1, 1, 0],  # c
                                                          [-1, 0, 0],  # d

                                                          [0, 0, 1],  # e
                                                          [0, 1, 1],  # f
                                                          [-1, 1, 1],  # g
                                                          [-1, 0, 1]])  # h

    assert np.allclose(rotated_component_positions, expected_rotated_component_positions_z_90)

def test_rotation_at_origin_z_180():

    # Define a unit cube
    component_positions = np.array([[0, 0, 0],  # a
                                    [1, 0, 0],  # b
                                    [1, 1, 0],  # c
                                    [0, 1, 0],  # d

                                    [0, 0, 1],  # e
                                    [1, 0, 1],  # f
                                    [1, 1, 1],  # g
                                    [0, 1, 1]])  # h

    # Rotate about the z-axis by 180 degrees
    rotate_z_180 = np.array([0, 0, np.pi])


    # Rotate the cube

    rotated_component_positions = rotate(component_positions, rotate_z_180)

    expected_rotated_component_positions_z_180 = np.array([[0, 0, 0],  # a
                                                           [-1, 0, 0],  # b
                                                           [-1, -1, 0],  # c
                                                           [0, -1, 0],  # d

                                                           [0, 0, 1],  # e
                                                           [-1, 0, 1],  # f
                                                           [-1, -1, 1],  # g
                                                           [0, -1, 1]])  # h

    assert np.allclose(rotated_component_positions, expected_rotated_component_positions_z_180)


def test_rotation_at_origin_x_90():

    # Define a unit cube
    component_positions = np.array([[0, 0, 0],  # a
                                    [1, 0, 0],  # b
                                    [1, 1, 0],  # c
                                    [0, 1, 0],  # d

                                    [0, 0, 1],  # e
                                    [1, 0, 1],  # f
                                    [1, 1, 1],  # g
                                    [0, 1, 1]])  # h

    # Rotate about the x-axis by 90 degrees
    rotate_x_90 = np.array([np.pi/2, 0, 0])

    expected_rotated_component_positions_x_90 = np.array([[0, 0, 0],    # a
                                                          [1, 0, 0],    # b
                                                          [1, 0, 1],   # c
                                                          [0, 0, 1],   # d

                                                          [0, -1, 0],    # e
                                                          [1, -1, 0],    # f
                                                          [1, -1, 1],   # g
                                                          [0, -1, 1]])  # h

    # Rotate the cube
    rotated_component_positions = rotate(component_positions, rotate_x_90)


    assert np.allclose(rotated_component_positions, expected_rotated_component_positions_x_90)

def test_rotation_at_origin_z_90_x_90():

    # Define a unit cube
    component_positions = np.array([[0, 0, 0],  # a
                                    [1, 0, 0],  # b
                                    [1, 1, 0],  # c
                                    [0, 1, 0],  # d

                                    [0, 0, 1],  # e
                                    [1, 0, 1],  # f
                                    [1, 1, 1],  # g
                                    [0, 1, 1]])  # h


    rotate_x_90_z_90 = np.array([np.pi/2, 0, np.pi/2])

    # Rotate the cube
    rotated_component_positions = rotate(component_positions, rotate_x_90_z_90)

    expected_rotated_component_positions_z_90_x_90 = np.array([[0, 0, 0],    # a
                                                               [0, 1, 0],    # b
                                                               [0, 1, 1],   # c
                                                               [0, 0, 1],   # d

                                                               [1, 0, 0],    # e
                                                               [1, 1, 0],    # f
                                                               [1, 1, 1],   # g
                                                               [1, 0, 1]])  # h

    assert np.allclose(rotated_component_positions, expected_rotated_component_positions_z_90_x_90)
