# Importing NumPy as "np"
import numpy as np

class Multiplication:
    """
    Instantiate a multiplication operation.
    Numbers will be multiplied by the given multiplier.

    :param multiplier: The multiplier.
    :type multiplier: int
    """

    def __init__(self, multiplier):
        if not isinstance(multiplier, int):
            raise TypeError("param 'multiplier' must be an integer!")
        self.multiplier = multiplier

    def multiply(self, number):
        """
        Multiply a given number by the multiplier.

        :param number: The number to multiply.
        :type number: int

        :return: The result of the multiplication.
        :rtype: int
        """
        if not isinstance(number, int):
            raise TypeError("param 'number' must be an integer!")

        # Using NumPy .dot() to multiply the numbers
        return np.dot(number, self.multiplier)


if __name__ == "__main__":
    # Call the function
    multiplication =Multiplication(2)
    print(multiplication.multiply(1))
