import math

class Vect:

   def __init__(self, a, b):
        self.a = a
        self.b = b

   def findCounterClockwiseAngle(self, other):
       # using cross-product formula
       return math.degrees(math.asin((self.a * other.b - self.b * other.a)/(self.length()*other.length())))
       # the dot-product formula, left here just for comparison (does not return angles in the desired range)
       # return math.degrees(math.acos((self.a * other.a + self.b * other.b)/(self.length()*other.length())))

   def length(self):
       return math.sqrt(self.a**2 + self.b**2)

vector1 = Vect(2,0)

N = 12
theta = [i * 2 * math.pi / N for i in range(N)]
result = []
for t in theta:
    vector2 = Vect(math.cos(t), math.sin(t))  ## a2*i + b2*j
    angle = vector1.findCounterClockwiseAngle(vector2)
    result.append((math.degrees(t), angle))

print('{:>10}{:>10}'.format('t', 'angle'))
print('\n'.join(['{:>10.2f}{:>10.2f}'.format(*pair) for pair in result]))