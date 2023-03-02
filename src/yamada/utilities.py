import math


def find_counter_clockwise_angle(a1, b1, a2, b2):
    length_1 = math.sqrt(a1**2 + b1**2)
    length_2 = math.sqrt(a2**2 + b2**2)
    return math.degrees(math.asin((a1 * b2 - b1 * a2)/(length_1 * length_2)))


N = 12
theta = [i * 2 * math.pi / N for i in range(N)]
result = []
for t in theta:
    vector2 = (math.cos(t), math.sin(t))
    angle = find_counter_clockwise_angle(2, 0, vector2[0], vector2[1])
    result.append((math.degrees(t), angle))

print('t')
for t in theta:
    print(t)
