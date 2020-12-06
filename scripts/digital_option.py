############
# packages #
############

from european_derivative import EuropeanDerivative
import numpy as np
import scipy.stats as si
import matplotlib.pyplot as plt
import datetime


#######################
# European Call Class #
#######################


class DigitalOption(EuropeanDerivative):

    ###############
    # Constructor #
    ###############

    def __init__(self, S0, K, r, sigma, T):

        EuropeanDerivative.__init__(
            self, S0, K, r, sigma, T, lambda x: 1 if x >= K else 0, "digital"
        )


########
#-Main-#
########
if __name__ == "__main__":

    ############
    # fix seed #
    ############

    np.random.seed(0)

    #####################
    # General Variables #
    #####################

    N_max = 10
    eps_vega, epse_delta, eps_gamma = 0.04, 8, 8

    ############################
    # Defining our call option #
    ############################

    T = 1
    S0 = 100
    sigma = 0.20
    r = 0.05
    K = 75

    digital_option = DigitalOption(S0, K, r, sigma, T)

    ###########################################################
    # Greeks : exact vs finite difference method vs malliavin #
    ###########################################################

    start_time = datetime.datetime.now()

    VEGA_epsilon = np.array([
        digital_option.greeks_difference_method(
            N=i, epsilon=eps_vega, param__="vol", order=1
        )
        for i in range(1,N_max)
    ])
    DELTA_epsilon = np.array([
        digital_option.greeks_difference_method(
            N=i, epsilon=epse_delta, param__="price_0", order=1
        )
        for i in range(1,N_max)
    ])
    GAMMA_epsilon = np.array([
        digital_option.greeks_difference_method(
            N=i, epsilon=eps_gamma, param__="price_0", order=2
        )
        for i in range(1,N_max)
    ])

    VEGA_malliavin = np.array([
        digital_option.greeks_malliavin(N=i, param__="vol", order=1) for i in range(1,N_max)
    ])
    DELTA_malliavin = np.array([
        digital_option.greeks_malliavin(N=i, param__="price_0", order=1)
        for i in range(1,N_max)
    ])
    GAMMA_malliavin = np.array([
        digital_option.greeks_malliavin(N=i, param__="price_0", order=2)
        for i in range(1,N_max)
    ])

    end_time = datetime.datetime.now()

    monte_carlo_simulation = end_time - start_time
    monte_carlo_simulation_hours = int(
        monte_carlo_simulation.total_seconds() // 3600)
    monte_carlo_simulation_minutes = int(
        (monte_carlo_simulation.total_seconds() -
         monte_carlo_simulation_hours * 3600) // 60
    )
    monte_carlo_simulation_seconds = int(
        monte_carlo_simulation.total_seconds()
        - monte_carlo_simulation_hours * 3600
        - monte_carlo_simulation_minutes * 60
    )

    print(
        "Monte Carlo simulation overall Time: {:02d}:{:02d}:{:02d}".format(
            monte_carlo_simulation_hours, monte_carlo_simulation_minutes, monte_carlo_simulation_seconds
        )
    )

    print("*"*50)
    print("ratio_finite_diference_to_malliavin : ")
    print(f"- delta : {DELTA_epsilon.var()/DELTA_malliavin.var()}")
    print(f"- gamma : {GAMMA_epsilon.var()/GAMMA_malliavin.var()}")
    print(f"- vega : {VEGA_epsilon.var()/VEGA_malliavin.var()}")

    ########
    # plot #
    ########

    fig, ax = plt.subplots(1, 3, sharey=False, figsize=(24, 7))

    ax[0].plot(DELTA_epsilon, label="finite difference method", color="blue")
    ax[0].plot(DELTA_malliavin, label="maliavin method", color="red")
    ax[0].set_xlabel(r"Number of iterations")
    ax[0].set_ylabel(r"$\Delta$", fontsize=15)
    ax[0].grid()
    ax[0].legend()

    ax[1].plot(GAMMA_epsilon, label="finite difference method", color="blue")
    ax[1].plot(GAMMA_malliavin, label="maliavin method", color="red")
    ax[1].set_xlabel(r"Number of iterations")
    ax[1].set_ylabel(r"$\Gamma$", fontsize=15)
    ax[1].grid()
    ax[1].legend()

    ax[2].plot(VEGA_epsilon, label="finite difference method", color="blue")
    ax[2].plot(VEGA_malliavin, label="maliavin method", color="red")
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
