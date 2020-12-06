############
# packages #
############

from european_derivative import EuropeanDerivative
import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt


#######################
# European Call Class #
#######################


class EuropeanCall(EuropeanDerivative):

    ###############
    # Constructor #
    ###############

    def __init__(self, S0, K, r, sigma, T):

        EuropeanDerivative.__init__(
            self, S0, K, r, sigma, T, lambda x: max(x - K, 0), "call"
        )

    ###############################################
    # Exact greeks values with Black&Scoles Model #
    ###############################################

    def __black_scholes_params(self):

        r, T, S, sigma, K = (
            self.params["interest_rate"],
            self.params["maturity"],
            self.params["price_0"],
            self.params["vol"],
            self.params["strike"],
        )

        d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = (np.log(S / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

        return d1, d2

    def __exact_delta(self):

        d1, d2 = self.__black_scholes_params()

        delta = si.norm.cdf(d1, 0.0, 1.0)

        return delta

    def __exact_vega(self):

        d1, d2 = self.__black_scholes_params()

        prob_density = 1 / np.sqrt(2 * np.pi) * np.exp(-(d1 ** 2) * 0.5)

        vega = S0 * prob_density * np.sqrt(self.params["maturity"])

        return vega

    def __exact_gamma(self):

        d1, d2 = self.__black_scholes_params()

        prob_density = 1 / np.sqrt(2 * np.pi) * np.exp(-(d1 ** 2) * 0.5)

        gamma = prob_density / (
            self.params["price_0"]
            * self.params["vol"]
            * np.sqrt(self.params["maturity"])
        )

        return gamma

    def greeks_exact(self):

        delta = self.__exact_delta()
        vega = self.__exact_vega()
        gamma = self.__exact_gamma()

        return delta, vega, gamma


########
# Main #
########

if __name__ == "__main__":

    #####################
    # General Variables #
    #####################

    N_max = 10_000
    eps_vega, epse_delta, eps_gamma = 0.04, 8, 8

    ############################
    # Defining our call option #
    ############################

    T = 1
    S0 = 100
    sigma = 0.20
    r = 0.05
    K = 75

    call_option = EuropeanCall(S0, K, r, sigma, T)

    ###########################################################
    # Greeks : exact vs finite difference method vs malliavin #
    ###########################################################

    delta, vega, gamma = call_option.greeks_exact()

    VEGA_epsilon = [
        call_option.greeks_difference_method(
            N=i, epsilon=eps_vega, param__="vol", order=1
        )
        for i in range(N_max)
    ]
    DELTA_epsilon = [
        call_option.greeks_difference_method(
            N=i, epsilon=epse_delta, param__="price_0", order=1
        )
        for i in range(N_max)
    ]
    GAMMA_epsilon = [
        call_option.greeks_difference_method(
            N=i, epsilon=eps_gamma, param__="price_0", order=2
        )
        for i in range(N_max)
    ]

    VEGA_malliavin = [
        call_option.greeks_malliavin(N=i, param__="vol", order=1) for i in range(N_max)
    ]
    DELTA_malliavin = [
        call_option.greeks_malliavin(N=i, param__="price_0", order=1)
        for i in range(N_max)
    ]
    GAMMA_malliavin = [
        call_option.greeks_malliavin(N=i, param__="price_0", order=2)
        for i in range(N_max)
    ]

    fig, ax = plt.subplots(1, 3, sharey=False, figsize=(24, 7))

    ax[0].plot(DELTA_epsilon, label="finite difference method", color="blue")
    ax[0].plot(DELTA_malliavin, label="maliavin method", color="red")
    ax[0].axhline(y=delta, color="g", linestyle="--", label=f"exact value {delta:.2f}")
    ax[0].set_xlabel(r"Number of iterations")
    ax[0].set_ylabel(r"$\Delta$", fontsize=15)
    ax[0].grid()
    ax[0].legend()

    ax[1].plot(GAMMA_epsilon, label="finite difference method", color="blue")
    ax[1].plot(GAMMA_malliavin, label="maliavin method", color="red")
    ax[1].axhline(y=gamma, color="g", linestyle="--", label=f"exact value {gamma:.3f}")
    ax[1].set_xlabel(r"Number of iterations")
    ax[1].set_ylabel(r"$\Gamma$", fontsize=15)
    ax[1].grid()
    ax[1].legend()

    ax[2].plot(VEGA_epsilon, label="finite difference method", color="blue")
    ax[2].plot(VEGA_malliavin, label="maliavin method", color="red")
    ax[2].axhline(y=vega, color="g", linestyle="--", label=f"exact value {vega:.2f}")
    ax[2].set_xlabel(r"Number of iterations")
    ax[2].set_ylabel(r"$\nu$", fontsize=15)
    ax[2].grid()
    ax[2].legend()

    plt.legend()
    plt.tight_layout()
    plt.show()

###############
# end-of-code #
###############
