#!/usr/bin/env python
# coding: utf-8

# 

# In[5]:


import numpy as np
from yamada import LinearAlgebra


# ## Test calculate_counter_clockwise_angle
# 
# ![Unit Circle](./images/unit_circle.png)

# In[6]:


def test_calculate_counter_clockwise_angle():

    la = LinearAlgebra()

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
    angle_0   = la.calculate_counter_clockwise_angle(reference_vector, degree_0)
    angle_30  = la.calculate_counter_clockwise_angle(reference_vector, degree_30)
    angle_90  = la.calculate_counter_clockwise_angle(reference_vector, degree_90)
    angle_135 = la.calculate_counter_clockwise_angle(reference_vector, degree_135)
    angle_180 = la.calculate_counter_clockwise_angle(reference_vector, degree_180)
    angle_240 = la.calculate_counter_clockwise_angle(reference_vector, degree_240)
    angle_270 = la.calculate_counter_clockwise_angle(reference_vector, degree_270)
    angle_300 = la.calculate_counter_clockwise_angle(reference_vector, degree_300)

    assert np.isclose(angle_0, 0) or np.isclose(angle_0, 360)
    assert np.isclose(angle_30, 30)
    assert np.isclose(angle_90, 90)
    assert np.isclose(angle_135, 135)
    assert np.isclose(angle_180, 180)
    assert np.isclose(angle_240, 240)
    assert np.isclose(angle_270, 270)
    assert np.isclose(angle_300, 300)


# ## Test Rotation

# Rotate 90 degrees

# In[ ]:


def test_rotation_at_origin():

    la = LinearAlgebra()

    rotation = np.array([0,0,np.pi/2])

    # Define a unit cube

    component_positions = np.array([[0, 0, 0],  # a
                                    [1, 0, 0],  # b
                                    [1, 1, 0],  # c
                                    [0, 1, 0],  # d
                                    [0, 0, 1],  # e
                                    [1, 0, 1],  # f
                                    [1, 1, 1],  # g
                                    [0, 1, 1]])  # h

    # Rotate the cube

    rotated_component_positions = la.rotate(component_positions, rotation)


# In[ ]:




