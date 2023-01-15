
class LaurentPolynomial:
    def __init__(self, term_tuples):

        self.term_tuples = term_tuples
    
        self.coeff, self.order = list(zip(*self.term_tuples))

    def __repr__(self):

        polynomial_expression = ""

        for coeff_i, order_i in zip(self.coeff, self.order):
            polynomial_expression += str(coeff_i) + "A^" + str(order_i) + " + "
        
        # Remove trailing " + "
        polynomial_expression = polynomial_expression.rstrip(" + ")
             
        return polynomial_expression

    def __add__(self, polynomial):

        # TODO If same order then increment coeff
        
        coeffs = self.coeff + polynomial.coeff
        orders = self.order + polynomial.order

        # Pack coeff and order into tuples
        term_tuples = list(zip(coeffs, orders))

        return LaurentPolynomial(term_tuples)
    
    # TODO Implement __iadd__ method?
    # TODO Implement __isub__ method?

    def __mul__(self, polynomial):
        pass

    # TODO Implement __truediv__ method?
    # TODO Implement __floordiv__ method?


        

aa = LaurentPolynomial([(1,1), (2,2), (3,3)])

bb = LaurentPolynomial([(1,1), (2,2), (3,3)])

print("AA", aa)

# print(type(aa))

cc = aa + bb

print("CC", cc)
# print(type(cc))

# print(cc.coeff)