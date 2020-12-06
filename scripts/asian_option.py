############
# packages #
############

import numpy as np
from utils import brownian_motion
from abstract_derivative import Derivative

##########################
# Asian Derivative class #
##########################

class AsianDerivative(Derivative):

    #################
    # Class Builder #
    #################

    def __init__(self, S0, r, sigma, T, asian_params, payoff_cum, name, m=365):
        self.name = "_".join(["asian", name])
        self.params = {
            "price_0": S0,
            "interest_rate": r,
            "vol": sigma,
            "maturity": T,
            "asian_params": asian_params
        }
        self.payoff_cum = payoff_cum
        self.integration_nb = m

    ######################
    # Monte-Carlo pricer #
    ######################  

    def price_monte_carlo(self, N, epsilon=0, param__=None):
        sum = 0
        params__ = self.params.copy()
        if param__:
            params__[param__] = self.params[param__] + epsilon
        T = np.linspace(0, self.params['maturity'], self.integration_nb)
        for i in range(N):
            W = brownian_motion(self.params['maturity'], self.integration_nb)
            S_T = self.params['price_0']*np.exp(
                (self.params['interest_rate']-(self.params['vol']**2)/2)*T+self.params['vol']*W)

            integral_S_T = np.sum(S_T[1:])/self.integration_nb

            sum += self.payoff_cum(integral_S_T)

        return sum * np.exp(-params__["interest_rate"] * params__["maturity"]) / N

    
    ########################################
    # Greeks with finite difference method #
    ######################################## 

    def greeks_difference_method(self, N, epsilon, param__, order):
        if order == 2:
            return (
                self.price_monte_carlo(N, epsilon, param__)
                + self.price_monte_carlo(N, -epsilon, param__)
                - 2 * self.price_monte_carlo(N)
            ) / (epsilon ** 2)
        if order == 1:
            return (
                self.price_monte_carlo(N, epsilon, param__)
                - self.price_monte_carlo(N, -epsilon, param__)
            ) / (epsilon * 2)

    ##########################
    # Exact values of greeks #
    ##########################

    def greeks_exact(self):
        raise Exception("No exact formula is available !")

    #############################
    # Malliavin Calculus greeks #
    #############################

    def greeks_malliavin(self, N, param__, order):
        raise NotImplementedError

if __name__ == "__main__":
    pass
