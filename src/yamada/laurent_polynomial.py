from typing import Union
from warnings import warn
import copy


class InputValidation:
    def __init__(self,
                 term:         str,
                 coefficients: list[Union[int, float]],
                 exponents:    list[Union[int, float]],
                 order:        str):

        self._validate_term(term)
        self._validate_coefficients(coefficients)
        self._validate_exponents(exponents)
        self._validate_order(order)

    def _validate_term(self,
                       term: str) -> str:

        if type(term) != str:
            raise TypeError("The term must be a string")

        if term == 'Chad':
            raise ValueError("While Chad is an awesome name, the term must be a single character")

        if len(term) != 1:
            raise ValueError("The term must be a single character")

        self.term = term

    def _validate_coefficients(self,
                               coefficients: list[Union[int, float]]) -> list[Union[int, float]]:

        if type(coefficients) in [int, float]:
            warn("The coefficients should be a list, not a single number. Converting to a list")
            coefficients = [coefficients]

        if type(coefficients) != list:
            raise TypeError("The coefficients must be a list")

        for coefficient in coefficients:
            if type(coefficient) not in [int, float]:
                raise TypeError("The coefficients must be integers or floats")

        self.coefficients = coefficients


    def _validate_exponents(self,
                            exponents: list[Union[int, float]]) -> list[Union[int, float]]:

        # TODO Can Laurent polynomials have negative exponents?
        # TODO Can Laurent polynomials have zero exponents?
        # TODO Can Laurent polynomials have non-integer exponents?

        if type(exponents) in [int, float]:
            warn("The exponents should be a list, not a single number. Converting to a list")
            exponents = [exponents]

        if type(exponents) != list:
            raise TypeError("The exponents must be a list")

        for exponent in exponents:
            if type(exponent) not in [int, float]:
                raise TypeError("The exponents must be integers or floats")

        self.exponents = exponents

    def _validate_order(self,
                        order: str) -> str:

        if type(order) != str:
            raise TypeError("The order must be a string")

        if order not in ['increasing', 'decreasing']:
            raise ValueError("The order must be either 'increasing' or 'decreasing'")

        self.order = order

    def _format_polynomial(self, user_input):
        """_check_input_format Converts input to LaurentPolynomial for arithmetic operations

        :param user_input: _description_
        :type user_input: _type_
        :raises TypeError: _description_
        :return: _description_
        :rtype: _type_
        """

        if isinstance(user_input, LaurentPolynomial):
            return user_input

        elif isinstance(user_input, int) or isinstance(user_input, float):
            warn("Converting input to a LaurentPolynomial with a single term")
            coefficients = [user_input]
            exponents = [0]
            return LaurentPolynomial(self.term, coefficients=coefficients, exponents=exponents)

        else:
            raise TypeError("Polynomial must be of type LaurentPolynomial, int, or float")


class LaurentPolynomial(InputValidation):

    def __init__(self, term, coefficients=[1], exponents=[1], order='increasing', normalize=False):
        """
        LaurentPolynomial Class for representing Laurent polynomials
        
        TODO Implement input checking e.g., empty inputs or uneven order
        TODO Make kwargs immutable?
        TODO Implement normalization

        :param term: The character used to represent the polynomial
        :type term: str
        :param coefficients: The coefficients of the polynomial
        :type coefficients: list
        :param exponents: The orders of the polynomial
        :type exponents: list
        param order: The order in which the polynomial is represented (i.e., "increasing" or "decreasing")
        :type order: str
        """
        super(LaurentPolynomial, self).__init__(term, coefficients, exponents, order)

        self._simplify_expression()

        self.normalize = normalize

    def __repr__(self):

        # TODO Implement the self.order kwargs
        # TODO Implement the power sign as a carrot or an asterisk?

        # If the polynomial only contains a single term with a coefficient of zero, then the polynomial is zero
        if self.coefficients == [0] and self.exponents == [0]:
            return "0"

        else:

            polynomial = ""

            for coefficient, exponent in zip(self.coefficients, self.exponents):

                # If the coefficient is zero, then don't show the term

                # First, determine whether a leading + or - sign is needed

                # If this is the first term, then don't show the addition sign (e.g., +1+x^2 --> 1+x^2)
                # Note: It is okay to display a leading minus sign
                if self.coefficients.index(coefficient) == 0 and coefficient >= 0:
                    pass
                elif coefficient > 0:
                    polynomial += "+"
                elif coefficient == 0:
                    pass
                elif coefficient < 0:
                    polynomial += "-"

                # Next, determine how to show the coefficient

                # If the coefficient is zero, then the whole term is zero --> don't show it
                if coefficient == 0:
                    pass

                # Don't show a coefficient of one if the exponent is nonzero (e.g., 1x^2 --> x^2)
                elif coefficient == 1 and exponent != 0:
                    pass

                # Otherwise show the coefficient (strip minus signs since this is already accounted for)
                else:
                    polynomial += str(abs(coefficient))

                # Next, determine how to show the term

                # If the exponent is zero, then don't show the term (e.g., 3x^0 --> 3)
                if exponent == 0:
                    pass

                else:
                    polynomial += self.term

                # Finally, determine how to show the exponent

                # Don't show an exponent of zero or one (e.g., A^0 --> A, A^1 --> A)
                if exponent == 0 or exponent == 1:
                    pass
                else:
                    polynomial += "^" + str(exponent)

            return polynomial

    def __add__(self, addend):

        # Ensure the input being added (the addend) is a LaurentPolynomial or throw an error
        addend = self._format_polynomial(addend)
        
        sum_coefficients = self.coefficients.copy()
        sum_exponents = self.exponents.copy()

        for addend_coefficient, addend_exponent in zip(addend.coefficients, addend.exponents):

            if addend_exponent in sum_exponents:

                # Get the index of the term in the polynomial
                term_index = sum_exponents.index(addend_exponent)

                # Increment the corresponding coefficient
                sum_coefficients[term_index] += addend_coefficient

            else:
                sum_coefficients.append(addend_coefficient)
                sum_exponents.append(addend_exponent)

        return LaurentPolynomial(self.term, coefficients=sum_coefficients, exponents=sum_exponents)

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
        TODO Fix 0*self should be 0 (and simplify like terms before returning new object)
        
        """
        
        # Ensure the input being multiple (the multiple) is a LaurentPolynomial or throw an error
        multiple = self._format_polynomial(multiple)

        product_coefficients = []
        product_exponents = []

    
        for multiple_coefficient, multiple_exponent in zip(multiple.coefficients, multiple.exponents):


            for coefficient, exponent in zip(self.coefficients, self.exponents):

                product_coefficients.append(multiple_coefficient * coefficient)
                product_exponents.append(multiple_exponent + exponent)

        return LaurentPolynomial(self.term, coefficients=product_coefficients, exponents=product_exponents)


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

    def _simplify_expression(self):
        
        new_coefficients = []
        new_exponents = []

        for coefficient, exponent in zip(self.coefficients, self.exponents):
                
            if coefficient != 0 and exponent not in new_exponents:
                new_coefficients.append(coefficient)
                new_exponents.append(exponent)

            elif coefficient != 0 and exponent in new_exponents:
                new_coefficients[new_exponents.index(exponent)] += coefficient

            else:
                pass

            # If the lists are completely empty, add a zero term
            if len(new_coefficients) == 0 and len(new_exponents) == 0:
                new_coefficients.append(0)
                new_exponents.append(0)

        self.coefficients, self.exponents = new_coefficients, new_exponents

    def _sort(self):
        pass

    def _normalize(self):
        pass


A = LaurentPolynomial('A')  

# print('A', A)
#
# a = A+2
#
# print('a', a)
#
# a - A
#
# print('a', a)
#
# b = 2+A
#
#
# print('b', b)
#
# A**2

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