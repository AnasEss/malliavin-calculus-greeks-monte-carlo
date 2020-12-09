##################################################################################
#                            Author: Anas ESSOUNAINI                             #
#                       File Name: abstract_derivative.py                        #
#                    Creation Date: December 4, 2020 09:10 PM                    #
#                    Last Updated: December 9, 2020 11:51 PM                     #
#                            Source Language: python                             #
#Repository: https://github.com/AnasEss/malliavin-calculus-greeks-monte-carlo.git#
#                                                                                #
#                            --- Code Description ---                            #
#                           abstract derivative class                            #
##################################################################################

############
# packages #
############

import abc
import numpy as np


#############################
# Abstract Class Derivative #
#############################


class Derivative(abc.ABC):
    """Abstract derivative class

    """

    def __init__(self):
        """Constructor
        """
        self.name = "abstract"
        self.params = {}


    @abc.abstractmethod
    def price_monte_carlo(self, N, epsilon=0, param__=None):
        """Prices derivative under Black&Scholes assumptions

        Args:
            N (int): number of Monte Carlo simulations
            epsilon (float, optional): used to offset a certain parameter, this is used 
                                       to compute greeks with finite difference method easily. Defaults to 0.
            param__ (str, optional): parameter of black & scholes model to offset with 
                                    espsilon if diffrent this None. Defaults to None.

        Raises:
            NotImplementedError: Not implemented yet
        """
        raise NotImplementedError


    @abc.abstractmethod
    def greeks_difference_method(self, N, epsilon, param__, order=1):
        """Computes greeks with finite difference method

        Args:
            N (int): number of iterations
            epsilon (float): epsilon used in finite diferent method for derivative estimation
            param__ (str): name of parameter to which we compute greek
            order (int, optional): order of derivative. Defaults to 1.

        Raises:
            NotImplementedError: not implemented yet
        """
        raise NotImplementedError


    @abc.abstractmethod
    def greeks_exact(self):
        """Computes exact values of greeks

        Raises:
            NotImplementedError: not implemented yet
        """
        raise NotImplementedError


    @abc.abstractmethod
    def greeks_malliavin(self, N, param__, order):
        """Computes greeks using Malliavin Calculus

        Args:
            N (int): number of iterations for MC
            param__ (str): name of parameter to which we compute our derivative (greek)
            order (int): order of derivative

        Raises:
            NotImplementedError: not implemented error
        """
        raise NotImplementedError


if __name__ == "__main__":
    pass

###############
# end-of-code #
###############