
class LaurentPolynomial:

    def __init__(self, term_tuples):

        self.term_tuples = term_tuples
    
        # Unpack tuples into coeff and order lists
        self.coeff, self.order = list(zip(*self.term_tuples))

    def __repr__(self):

        polynomial_expression = ""

        for coeff_i, order_i in zip(self.coeff, self.order):

            # If the coefficient is zero, skip the term
            if coeff_i == 0:
                pass
            # If the coefficient is not zero
            else:

                # If the coefficient is one, don't print it
                if coeff_i == 1:
                    pass
                else:
                    polynomial_expression += str(coeff_i)

                # If the order is zero, don't print the order
                if order_i == 0:
                    pass
                elif order_i == 1:
                    polynomial_expression += "A"
                else:
                    polynomial_expression += "A^" + str(order_i)

                polynomial_expression += " + "
            # If the coefficient is one, don't print it


            # If the order is zero, don't print the order

            # polynomial_expression += str(coeff_i) + "A^" + str(order_i) + " + "
        
        # Remove trailing " + "
        polynomial_expression = polynomial_expression.rstrip(" + ")
             
        return polynomial_expression

    def __add__(self, polynomial):

        # If the added term is not a LaurentPolynomial, convert it to one
        if isinstance(polynomial, LaurentPolynomial):
            pass
        elif isinstance(polynomial, int) or isinstance(polynomial, float):
            coeff = polynomial
            order = 0
            polynomial = LaurentPolynomial([(coeff, order)])
        else:
            raise TypeError("Polynomial must be of type LaurentPolynomial, int, or float")

        # Now add the two polynomials
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
    
    def __iadd__(self, polynomial):
        return self.__add__(polynomial)

    def __sub__(self, polynomial):
        return self.__add__(-1*polynomial)

    def __isub__(self, polynomial):
        return self.__add__(-1*polynomial)

    def __mul__(self, polynomial):
        
        new_term_tuples = []
    
        for term_coeff, term_order in self.term_tuples:

            if term_order in polynomial.order:

                # Get the index of the term in the polynomial
                term_index = polynomial.order.index(term_order)

                # Increment the corresponding coeff
                product_coeff = term_coeff * polynomial.coeff[term_index]
                combined_order = term_order + polynomial.order[term_index]
                new_term_tuples.append((product_coeff, combined_order))
            else:
                new_term_tuples.append((term_coeff, term_order))

        return LaurentPolynomial(new_term_tuples)

    # TODO Implement __truediv__ method?
    # TODO Implement __floordiv__ method?
    # TODO Implement _normalize method?
    # TODO Implement _sort method?


        

aa = LaurentPolynomial([(1,1), (1,2), (1,3)])

bb = LaurentPolynomial([(1,1), (1,2), (1,3)])

print('polynomial', aa)

# print(type(aa))

cc = aa + bb

print('add self  ',cc)
# print(type(cc))

# print(cc.coeff)

dd = aa * bb

print('mult self ',dd)