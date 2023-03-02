# import math
#
#
# def find_counter_clockwise_angle(a1, b1, a2, b2):
#     length_1 = math.sqrt(a1**2 + b1**2)
#     length_2 = math.sqrt(a2**2 + b2**2)
#
#     angle = math.degrees(math.asin((a1 * b2 - b1 * a2)/(length_1 * length_2)))
#
#     # if angle < 0:
#     #     angle = -angle
#     #     angle += 90
#
#     return angle
#
#
#
#
# reference_vector = (1, 0)
#
# #             0             1               2
# positions = [(0.33, 0.80), (-0.35, -1.95), (-0.02, -1.15)]
#
# for position in positions:
#     angle = find_counter_clockwise_angle(reference_vector[0], reference_vector[1], position[0], position[1])
#     print('Angle:', angle, 'degrees')



# def find_angle(a, b):
#
#     x_a, x_b = a[0][0], b[0][0]
#     y_a, y_b = a[0][1], b[0][1]
#
#     a_dot_b = np.dot(x_a, x_b) + np.dot(y_a, y_b)
#     norm_a = np.sqrt(x_a**2 + y_a**2)
#     norm_b = np.sqrt(x_b**2 + y_b**2)
#
#     theta = np.arccos(a_dot_b / (norm_a * norm_b))
#
#     return theta
#
#
# reference_vector = (1, 0)
#
# #             0             1               2
# positions = [(0.33, 0.80), (-0.35, -1.95), (-0.02, -1.15), (0.33, -0.80)]
#
# for position in positions:
#     a = np.array([[reference_vector[0], reference_vector[1]]])
#     b = np.array([[position[0], position[1]]])
#     angle = find_angle(a, b)
#     print('Angle:', angle, 'degrees')



from math import acos
from math import sqrt
from math import pi


def length(v):
    return sqrt(v[0]**2+v[1]**2)


def dot_product(v,w):
   return v[0]*w[0]+v[1]*w[1]


def determinant(v,w):
   return v[0]*w[1]-v[1]*w[0]


def inner_angle(v,w):
   cosx=dot_product(v,w)/(length(v)*length(w))
   rad=acos(cosx) # in radians
   return rad*180/pi # returns degrees


def angle_clockwise(A, B):
    inner=inner_angle(A,B)
    det = determinant(A,B)
    if det>0: #this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else: # if the det > 0 then A is immediately clockwise of B
        return 360-inner


reference_vector = (1, 0)

#             0             1               2
positions = [(0.33, 0.80), (-0.35, -1.95), (-0.02, -1.15)]


