from typing import Union
from warnings import warn
import copy


class InputValidation:
    def __init__(self,
                 term:         str,
                 coefficients: list[Union[int, float]],
                 exponents:    list[Union[int, float]],
                 order:        str):

        self.term         = self._check_term(term)
        self.coefficients = self._check_coefficients(coefficients)
        self.exponents    = self._check_exponents(exponents)
        self.order        = self._check_order(order)

    def _check_term(self,
                    term: str) -> str:

        if type(self.term) != str:
            raise TypeError("The term must be a string")
        if len(self.term) != 1:
            raise ValueError("The term must be a single character")

        return term

    def _check_coefficients(self,
                            coefficients: list[Union[int, float]]) -> list[Union[int, float]]:
        if type(self.coefficients) != list:
            raise TypeError("The coefficients must be a list")
        for coefficient in self.coefficients:
            if type(coefficient) != int:
                raise TypeError("The coefficients must be integers")

        return coefficients

    def _check_exponents(self,
                         exponents: list[Union[int, float]]) -> list[Union[int, float]]:

        # TODO Can Laurent polynomials have negative exponents?
        # TODO Can Laurent polynomials have zero exponents?
        # TODO Can Laurent polynomials have non-integer exponents?

        if type(self.exponents) != list:
            raise TypeError("The exponents must be a list")
        for exponent in self.exponents:
            if type(exponent) != int:
                raise TypeError("The exponents must be integers")

        return exponents

    def _check_order(self,
                     order: str) -> str:

        if type(self.order) != str:
            raise TypeError("The order must be a string")
        if self.order not in ['increasing', 'decreasing']:
            raise ValueError("The order must be either 'increasing' or 'decreasing'")

        return order


class LaurentPolynomial:

    def __init__(self, term, coefficients=[1], exponents=[1], order='increasing'):
        """
        LaurentPolynomial Class for representing Laurent polynomials
        
        TODO Implement input checking e.g., empty inputs or uneven order

        :param term: The character used to represent the polynomial
        :type term: str
        :param coefficients: The coefficients of the polynomial
        :type coefficients: list
        :param exponents: The orders of the polynomial
        :type exponents: list
        param order: The order in which the polynomial is represented (i.e., "increasing" or "decreasing")
        :type order: str
        """
        
        self.term = term
        self.coefficients = coefficients
        self.exponents = exponents
        self.order = order

    def __repr__(self):

        # TODO Implement the self.order kwargs

        # If the polynomial only contains a single term with a coefficient of zero, then the polynomial is zero
        if self.coefficients == [0] and self.exponents == [0]:
            return "0"

        else:

            polynomial = ""

            for coefficient, exponent in zip(self.coefficients, self.exponents):

                # If the coefficient is zero, then the whole term is zero --> don't show it
                if coefficient == 0:
                    pass

                else:

                    # First, determine whether a leading + or - sign is needed

                    # If this is the first term, then don't show the addition sign (e.g., +1+x^2 --> 1+x^2)
                    # Note: It is okay to display a leading minus sign
                    if self.coefficients.index(coefficient) == 0 and coefficient >= 0:
                        pass
                    elif coefficient >= 0:
                        polynomial += "+"
                    elif coefficient < 0:
                        polynomial += "-"

                    # Next, determine how to show the coefficient and exponent

                    # Don't show a coefficient of one if the exponent is nonzero (e.g., 1x^1 --> x)
                    if coefficient == 1 and exponent == 1:
                        polynomial += str(self.term)

                    # But if a coefficient is nonzero and the exponent is zero, show it (e.g., 3x^0 --> 3)
                    elif coefficient != 0 and exponent == 0:
                        polynomial += str(coefficient)

                    else:
                        polynomial += str(coefficient) + str(self.term) + "^" + str(exponent)


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
        product_coeffs, product_orders = self._simplify_expression(product_coeffs, product_orders)

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

    def _simplify_expression(self, coeffs, orders):
        
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