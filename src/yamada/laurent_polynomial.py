
import copy


class LaurentPolynomial:

    def __init__(self, term, coefficients=[1], exponents=[1]):
        """
        LaurentPolynomial Class for representing Laurent polynomials
        
        TODO Implemennt input checking e.g., empty inputs or uneven order

        :param term: The character used to represent the polynomial
        :type term: str
        :param coefficients: The coefficients of the polynomial
        :type coefficients: list
        :param exponents: The orders of the polynomial
        :type exponents: list
        """
        
        self.term = term
        self.coefficients = coefficients
        self.exponents = exponents

    def __repr__(self):

        # Initialize the polynomial
        polynomial = ""

        for coefficient, exponent in zip(self.coefficients, self.exponents):

            # TODO Only show zero if it is the only term in the polynomial


            # If the coefficient is zero, it disappears
            # TODO Evaluate if this is the best way to handle zero coefficients
            if coefficient == 0:
                # pass
                polynomial += str(coefficient)

            else:

                # If the coefficient is one, don't show it
                if coefficient == 1:
                    pass
                else:
                    polynomial += str(coefficient)

                # However if coefficient is 1 and exponent is zero we should show it
                if coefficient == 1 and exponent == 0:
                    polynomial += str(coefficient)

                # If the exponent is zero, don't print the exponent
                if exponent == 0:
                    pass
                elif exponent == 1:
                    polynomial += self.term
                else:
                    polynomial += self.term + "^" + str(exponent)

                polynomial += " + "
        
        # Remove trailing " + "
        polynomial = polynomial.rstrip(" + ")
             
        return polynomial

    def __add__(self, addend):

        # Ensure the input being added (the addend) is a LaurentPolynomial or throw an error
        addend = self._format_polynomial(addend)
        
        sum_coeffs = self.coefficients.copy()
        sum_orders = self.exponents.copy()

        for addend_coeff, addend_order in zip(addend.coefficients, addend.exponents):

            if addend_order in sum_orders:

                # Get the index of the term in the polynomial
                term_index = sum_orders.index(addend_order)

                # Increment the corresponding coeff
                sum_coeffs[term_index] += addend_coeff 

            else:
                sum_coeffs.append(addend_coeff)
                sum_orders.append(addend_order)


        return LaurentPolynomial(self.term, coefficients= sum_coeffs, exponents= sum_orders)

    def __radd__(self, addend):
        return self.__add__(addend)

    def __sub__(self, subtrahend):
        
        return self.__add__(-1*subtrahend)

    def __rsub__(self, subtrahend):
        return self.__add__(-1*subtrahend)

    def __mul__(self, multiple):

        """
        (1+x) * (1+x) = (1+x)^2 = 1 + 2x + x^2

        TODO check if need to expand...
        TODO fix object creation statement
        
        """
        
        # Ensure the input being multipled (the multiple) is a LaurentPolynomial or throw an error
        multiple = self._format_polynomial(multiple)

        product_coeffs = []
        product_orders = []

    
        for multiple_coeff, multiple_order in zip(multiple.coefficients, multiple.exponents):


            for self_coeff, self_order in zip(self.coefficients, self.exponents):

                product_coeffs.append(multiple_coeff * self_coeff)
                product_orders.append(multiple_order + self_order)

        # Simplify like terms
        product_coeffs, product_orders = self._simplify_like_terms(product_coeffs, product_orders)

        return LaurentPolynomial(self.term, coefficients= product_coeffs, exponents= product_orders)


    def __imul__(self, multiple):
        return self.__mul__(multiple)

    def __rmul__(self, multiple):
        return self.__mul__(multiple)


    def __pow__(self, power):
        
        polynomial = copy.deepcopy(self)

        for i in range(power-1):
            polynomial = polynomial.__mul__(self)

        return polynomial

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
            return LaurentPolynomial(self.term, coefficients=coeff, exponents=order)

        else:
            raise TypeError("Polynomial must be of type LaurentPolynomial, int, or float")

    def _simplify_like_terms(self, coeffs, orders):
        
        new_coeffs = []
        new_orders = []

        for coeff, order in zip(coeffs, orders):
                
                if order in new_orders:
                    new_coeffs[new_orders.index(order)] += coeff
                else:
                    new_coeffs.append(coeff)
                    new_orders.append(order)

        return new_coeffs, new_orders

    def _sort(self):
        pass

    def _normalize(self):
        pass


A = LaurentPolynomial('A')  

print('A', A)

a = A+2

print('a', a)

a - A

print('a', a)

b = 2+A


print('b', b)

A**2

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