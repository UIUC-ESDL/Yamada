import math


def find_counter_clockwise_angle(a1, b1, a2, b2):
    length_1 = math.sqrt(a1**2 + b1**2)
    length_2 = math.sqrt(a2**2 + b2**2)
    return math.degrees(math.asin((a1 * b2 - b1 * a2)/(length_1 * length_2)))


reference_vector = (1, 0)

#             0             1               2
positions = [(0.33, 0.80), (-0.35, -1.95), (-0.02, -1.15)]

for position in positions:
    angle = find_counter_clockwise_angle(reference_vector[0], reference_vector[1], position[0], position[1])
    print('Angle:', angle, 'radians')



