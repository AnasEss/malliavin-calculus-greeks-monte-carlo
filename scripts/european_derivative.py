##################################################################################
#                            Author: Anas ESSOUNAINI                             #
#                       File Name: european_derivative.py                        #
#                    Creation Date: December 6, 2020 05:40 PM                    #
#                    Last Updated: December 7, 2020 09:58 PM                     #
#                            Source Language: python                             #
#Repository: https://github.com/AnasEss/malliavin-calculus-greeks-monte-carlo.git#
#                                                                                #
#                            --- Code Description ---                            #
#                           European derivative class                            #
##################################################################################

############
# packages #
############

from abstract_derivative import Derivative
import numpy as np

#############################
# European Class Derivative #
#############################


class EuropeanDerivative(Derivative):
    """European style derivatives
    """
    #################
    # Class Builder #
    #################

    def __init__(self, S0, K, r, sigma, T, payoff, name):
        """Constructor of european derivative

        Args:
            S0 (float): price of asset at t=0
            K (float or tuple of strikes): strike or strikes eventually
            r (float): interest rate
            sigma (float): volatility
            T (float): maturity
            payoff (function): payoff of the option
            name (str): name of the option
        """
        self.name = "_".join(["euro", name])
        self.params = {
            "price_0": S0,
            "strike": K,
            "interest_rate": r,
            "vol": sigma,
            "maturity": T,
        }
        self.payoff = payoff

    ######################
    # Monte-Carlo pricer #
    ######################

    def price_monte_carlo(self, N, epsilon=0, param__=None):
        """Prices derivative under Black&Scholes assumptions

        Args:
            N (int): number of Monte Carlo simulations
            epsilon (float, optional): used to offset a certain parameter, this is used 
                                       to compute greeks with finite difference method easily. Defaults to 0.
            param__ (str, optional): parameter of black & scholes model to offset with 
                                    espsilon if diffrent this None. Defaults to None.

        Returns:
            float : price of the derivative
        """
        G = np.random.normal(size=N)
        sum = 0
        params__ = self.params.copy()
        if param__:
            params__[param__] = self.params[param__] + epsilon
        for i in range(N):
            sum += self.payoff(
                params__["price_0"]
                * np.exp(
                    (params__["interest_rate"] - params__["vol"] ** 2 / 2)
                    * params__["maturity"]
                    + params__["vol"] * (params__["maturity"] ** 0.5) * G[i]
                )
            )

        return sum * np.exp(-params__["interest_rate"] * params__["maturity"]) / N

    ########################################
    # Greeks with finite difference method #
    ########################################

    def greeks_difference_method(self, N, epsilon, param__, order=1):
        """Computes greeks with finite difference method

        Args:
            N (int): number of iterations
            epsilon (float): epsilon used in finite diferent method for derivative estimation
            param__ (str): name of parameter to which we compute greek
            order (int, optional): order of derivative. Defaults to 1.

        Returns:
            float: value of the greek
        """
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
        """Computes exact values of the greeks for the derivative

        Raises:
            Exception: no formula is available !
        """
        raise Exception("No exact formula is available !")

    #############################
    # Malliavin Calculus greeks #
    #############################

    def __delta__malliavin(self, N):
        """Computes delta of the option using Malliavin Calculus

        Args:
            N (int): number of iterations

        Returns:
            float: delta of the option
        """

        G = np.random.normal(size=N)
        sum = 0
        params__ = self.params.copy()
        r, T, S0, sigma = (
            params__["interest_rate"],
            params__["maturity"],
            params__["price_0"],
            params__["vol"],
        )

        sum = 0

        for x in G:
            S_T = S0 * np.exp((r - (sigma ** 2) / 2) * T + sigma * (T ** 0.5) * x)
            sum += self.payoff(S_T) * (x / (sigma * T ** 0.5))

        delta = np.exp(-r * T) * sum / S0
        delta = delta / N

        return delta

    def __vega__malliavin(self, N):
        """Computes vega of the option using Malliavin Calculus

        Args:
            N (int): number of iterations

        Returns:
            float: vega of the option
        """

        G = np.random.normal(size=N)
        sum = 0
        params__ = self.params.copy()
        r, T, S0, sigma = (
            params__["interest_rate"],
            params__["maturity"],
            params__["price_0"],
            params__["vol"],
        )

        sum = 0

        for x in G:
            S_T = S0 * np.exp((r - (sigma ** 2) / 2) * T + sigma * (T ** 0.5) * x)
            sum += self.payoff(S_T) * ((x ** 2 / sigma) - x * (T ** 0.5) - (1 / sigma))

        vega = np.exp(-r * T) * sum
        vega = vega / N

        return vega

    def __gamma__malliavin(self, N):
        """Computes gamma of the option using Malliavin Calculus

        Args:
            N (int): number of iterations

        Returns:
            float: gamma of the option
        """

        T, S0, sigma = (
            self.params["maturity"],
            self.params["price_0"],
            self.params["vol"],
        )

        return self.__vega__malliavin(N) / (S0 * S0 * sigma * T)

    def greeks_malliavin(self, N, param__, order):
        """Computes greeks using Malliavin Calculus

        Args:
            N (int): number of iterations for MC
            param__ (str): name of parameter to which we compute our derivative (greek)
            order (int): order of derivative

        Raises:
            Exception: parame__ should be in ["vol", "price_0"]
            Exception: order should be in [1,2]
            Exception: if order2, pram__ should be "price_0"

        Returns:
            float: corresponding greeks
        """

        if param__ not in ["vol", "price_0"]:
            raise Exception(f"Invalid param__ {param__} not in ['vol','price_0']")
            return

        if order not in [1, 2]:
            raise Exception(f"Invalid order {order} not in [1,2]")
            return

        if order == 1:
            if param__ == "vol":
                return self.__vega__malliavin(N)

            if param__ == "price_0":
                return self.__delta__malliavin(N)

        if order == 2 and param__ == "price_0":
            return self.__gamma__malliavin(N)

        raise Exception("Incompatible order and param__")


if __name__ == "__main__":
    pass

###############
# end-of-code #
###############
