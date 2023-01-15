
class LaurentPolynomial:

    def __init__(self, term, coeffs = [1], orders = [1]):

        # TODO switch from difining tuple to defining string and moving...
        # TODO Implemennt input checking e.g., empty inputs or uneven order
        # Must be type string
        self.term = term
        self.coeffs = coeffs
        self.orders = orders

        self.term_tuples = list(zip(self.coeffs, self.orders))
    
        # Unpack tuples into coeff and order lists
        # self.coeff, self.order = list(zip(*self.term_tuples))

    def __repr__(self):

        polynomial_expression = ""

        for coeff, order in zip(self.coeffs, self.orders):

            # If the coefficient is zero, skip the term
            if coeff == 0:
                pass
            # If the coefficient is not zero
            else:

                # If the coefficient is one, don't print it
                if coeff == 1:
                    pass
                else:
                    polynomial_expression += str(coeff)

                # If the order is zero, don't print the order
                if order == 0:
                    pass
                elif order == 1:
                    polynomial_expression += self.term
                else:
                    polynomial_expression += self.term + "^" + str(order)

                polynomial_expression += " + "
            # If the coefficient is one, don't print it


            # If the order is zero, don't print the order

            # polynomial_expression += str(coeff_i) + "A^" + str(order_i) + " + "
        
        # Remove trailing " + "
        polynomial_expression = polynomial_expression.rstrip(" + ")
             
        return polynomial_expression

    # TODO Make arithmetic operations work with both orders

    def __add__(self, addend):

        # Ensure the input being added (the addend) is a LaurentPolynomial or throw an error
        polynomial = self._format_polynomial(addend)
        
        result_coeffs = []
        result_orders = []

        for term_coeff, term_order in self.term_tuples:

            if term_order in polynomial.orders:

                # Get the index of the term in the polynomial
                term_index = polynomial.orders.index(term_order)

                # Increment the corresponding coeff
                added_coeff = term_coeff + polynomial.coeffs[term_index]

                result_coeffs.append(added_coeff)
                result_orders.append(term_order)

            else:
                result_coeffs.append(term_coeff)
                result_orders.append(term_order)


        return LaurentPolynomial(self.term, coeffs = result_coeffs, orders = result_orders)

    def __iadd__(self, addend):
        return self.__add__(addend)

    def __radd__(self, addend):
        return self.__add__(addend)

    def __pow__(self, power):
        pass

    def __sub__(self, subtrahend):
        return self.__add__(-1*subtrahend)

    def __isub__(self, subtrahend):
        return self.__add__(-1*subtrahend)

    def __rsub__(self, subtrahend):
        return self.__add__(-1*subtrahend)

    def __mul__(self, multiple):
        
        # TODO check if need to expand...
        # TODO fix object creation statement

        # Ensure the input being multipled (the multiple) is a LaurentPolynomial or throw an error
        polynomial = self._format_polynomial(multiple)

        new_term_tuples = []
    
        for term_coeff, term_order in self.term_tuples:

            if term_order in polynomial.orders:

                # Get the index of the term in the polynomial
                term_index = polynomial.orders.index(term_order)

                # Increment the corresponding coeff
                product_coeff = term_coeff * polynomial.coeffs[term_index]
                combined_order = term_order + polynomial.orders[term_index]
                new_term_tuples.append((product_coeff, combined_order))
            else:
                new_term_tuples.append((term_coeff, term_order))

        return LaurentPolynomial(new_term_tuples)

    # TODO Implement __truediv__ method?
    # TODO Implement __floordiv__ method?
    # TODO Implement _normalize method?
    # TODO Implement _sort method?
    
    def _format_polynomial(self, input):
        """_check_input_format Converts input to LaurentPolynomial for arithmetic operations

        :param input: _description_
        :type input: _type_
        :raises TypeError: _description_
        :return: _description_
        :rtype: _type_
        """
        if isinstance(input, LaurentPolynomial):
            return input

        elif isinstance(input, int) or isinstance(input, float):
            coeff = [input]
            order = [0]
            return LaurentPolynomial(self.term, coeffs=coeff, orders=order)

        else:
            raise TypeError("Polynomial must be of type LaurentPolynomial, int, or float")

    def _simplify_like_terms(self):
        pass


A = LaurentPolynomial('A')  

a = A+2

b = 2+A

print('a', a)
print('b', b)



# b = 3*A

# aa = LaurentPolynomial([(1,1), (1,2), (1,3)])

# bb = LaurentPolynomial([(1,1), (1,2), (1,3)])

# print('polynomial', aa)

# print(type(aa))

# cc = aa + bb

# print('add self  ',cc)
# print(type(cc))

# print(cc.coeff)

# dd = aa * bb

# print('mult self ',dd)


print('Done')