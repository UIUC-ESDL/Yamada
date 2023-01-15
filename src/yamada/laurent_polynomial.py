
class LaurentPolynomial:

    def __init__(self, term_tuples):

        self.term_tuples = term_tuples
    
        # Unpack tuples into coeff and order lists
        self.coeff, self.order = list(zip(*self.term_tuples))

    def __repr__(self):

        polynomial_expression = ""

        for coeff_i, order_i in zip(self.coeff, self.order):
            polynomial_expression += str(coeff_i) + "A^" + str(order_i) + " + "
        
        # Remove trailing " + "
        polynomial_expression = polynomial_expression.rstrip(" + ")
             
        return polynomial_expression

    def __add__(self, polynomial):

        new_term_tuples = []
    
        for term_coeff, term_order in self.term_tuples:

            if term_order in polynomial.order:

                # Get the index of the term in the polynomial
                term_index = polynomial.order.index(term_order)

                # Increment the corresponding coeff
                combined_coeff = term_coeff + polynomial.coeff[term_index]
                new_term_tuples.append((combined_coeff, term_order))
            else:
                new_term_tuples.append((term_coeff, term_order))

        return LaurentPolynomial(new_term_tuples)
    
    # TODO Implement __iadd__ method?
    # TODO Implement __isub__ method?

    def __mul__(self, polynomial):
        # TODO Implement __mul__ method
        pass

    # TODO Implement __truediv__ method?
    # TODO Implement __floordiv__ method?
    # TODO Implement _normalize method?


        

aa = LaurentPolynomial([(1,1), (1,2), (1,3)])

bb = LaurentPolynomial([(1,1), (1,2), (1,3)])

print(aa)

# print(type(aa))

cc = aa + bb

print(cc)
# print(type(cc))

# print(cc.coeff)