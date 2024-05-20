#!/usr/bin/env python
# coding: utf-8

# 

# In[5]:


import numpy as np
from yamada.geometry import rotate, get_line_segment_intersection, calculate_intermediate_y_position, calculate_counter_clockwise_angle


# ## Test calculate_counter_clockwise_angle
# 
# ![Unit Circle](./images/unit_circle.png)

# In[6]:


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
    angle_0   = calculate_counter_clockwise_angle(reference_vector, degree_0)
    angle_30  = calculate_counter_clockwise_angle(reference_vector, degree_30)
    angle_90  = calculate_counter_clockwise_angle(reference_vector, degree_90)
    angle_135 = calculate_counter_clockwise_angle(reference_vector, degree_135)
    angle_180 = calculate_counter_clockwise_angle(reference_vector, degree_180)
    angle_240 = calculate_counter_clockwise_angle(reference_vector, degree_240)
    angle_270 = calculate_counter_clockwise_angle(reference_vector, degree_270)
    angle_300 = calculate_counter_clockwise_angle(reference_vector, degree_300)

    assert np.isclose(angle_0, 0) or np.isclose(angle_0, 360)
    assert np.isclose(angle_30, 30)
    assert np.isclose(angle_90, 90)
    assert np.isclose(angle_135, 135)
    assert np.isclose(angle_180, 180)
    assert np.isclose(angle_240, 240)
    assert np.isclose(angle_270, 270)
    assert np.isclose(angle_300, 300)


# ## Test Rotation

# 

# In[ ]:


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


# Rotate 90 degrees

# In[ ]:


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



# In[ ]:


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


# In[ ]:


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


# In[ ]:


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


