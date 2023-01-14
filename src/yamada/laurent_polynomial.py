
class LaurentPolynomial:
    def __init__(self, coeff, order):
        self.coeff = coeff
        self.order = order

    @property
    def polynomial(self):

        polynomial = ""

        for i, j in zip(self.coeff, self.order):
            polynomial += str(i) + "A^" + str(j) + " + "
        
        # Remove trailing " + "
        polynomial = polynomial.rstrip(" + ")
             
        return polynomial

    def __repr__(self):  
        return self.polynomial

    def __add__(self, polynomial):

        # TODO If same order then increment coeff
        
        coeffs = self.coeff + polynomial.coeff
        orders = self.order + polynomial.order

        return LaurentPolynomial(coeffs, orders)
        

aa = LaurentPolynomial([1,2,3], [1,2,3])

bb = LaurentPolynomial([1,2,3], [1,2,3])

print("AA", aa)

print(type(aa))

cc = aa + bb

print("CC", cc)
print(type(cc))

# print(cc.coeff)