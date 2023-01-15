
class LaurentPolynomial:
    def __init__(self, coeff, order):
        self.coeff = coeff
        self.order = order

    @property
    def laurent_polynomial(self):

        laurent_polynomial = ""

        for i, j in zip(self.coeff, self.order):
            laurent_polynomial += str(i) + "A^" + str(j) + " + "
        
        # Remove trailing " + "
        laurent_polynomial = laurent_polynomial.rstrip(" + ")
             
        return laurent_polynomial

    def __repr__(self):  
        return self.laurent_polynomial

    def __add__(self, polynomial):

        # TODO If same order then increment coeff
        
        coeffs = self.coeff + polynomial.coeff
        orders = self.order + polynomial.order

        return LaurentPolynomial(coeffs, orders)
    
    # TODO Implement __iadd__ method?
    # TODO Implement __isub__ method?

    def __mul__(self, polynomial):
        pass

    # TODO Implement __truediv__ method?
    # TODO Implement __floordiv__ method?


        

aa = LaurentPolynomial([1,2,3], [1,2,3])

bb = LaurentPolynomial([1,2,3], [1,2,3])

print("AA", aa)

print(type(aa))

cc = aa + bb

print("CC", cc)
print(type(cc))

# print(cc.coeff)