##################################################################################
#                            Author: Anas ESSOUNAINI                             #
#                       File Name: abstract_derivative.py                        #
#                    Creation Date: December 4, 2020 09:10 PM                    #
#                    Last Updated: December 7, 2020 09:57 PM                     #
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
    def __init__(self):
        self.name = "abstract"
        self.params = {}

    @abc.abstractmethod
    def price_monte_carlo(self):
        raise NotImplementedError

    @abc.abstractmethod
    def greeks_difference_method(self):
        raise NotImplementedError

    @abc.abstractmethod
    def greeks_exact(self):
        raise NotImplementedError

    @abc.abstractmethod
    def greeks_malliavin(self, N, param__, order):
        raise NotImplementedError


if __name__ == "__main__":
    pass

###############
# end-of-code #
###############