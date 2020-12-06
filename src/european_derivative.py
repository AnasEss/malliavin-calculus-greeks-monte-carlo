############
# packages #
############

from abstract_derivative import Derivative
import numpy as np

#############################
# European Class Derivative #
#############################


class EuropeanDerivative(Derivative):

    #################
    # Class Builder #
    #################

    def __init__(self, S0, K, r, sigma, T, payoff, name):
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

    def __delta__malliavin(self, N):

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

        T, S0, sigma = (
            self.params["maturity"],
            self.params["price_0"],
            self.params["vol"],
        )

        return self.__vega__malliavin(N) / (S0 * S0 * sigma * T)

    def greeks_malliavin(self, N, param__, order):

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
