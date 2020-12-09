##################################################################################
#                            Author: Anas ESSOUNAINI                             #
#                         File Name: corridor_option.py                          #
#                    Creation Date: December 7, 2020 08:33 PM                    #
#                    Last Updated: December 9, 2020 11:51 PM                     #
#                            Source Language: python                             #
#Repository: https://github.com/AnasEss/malliavin-calculus-greeks-monte-carlo.git#
#                                                                                #
#                            --- Code Description ---                            #
#                             corridor option class                              #
##################################################################################

############
# packages #
############

from european_derivative import EuropeanDerivative
import numpy as np
import matplotlib.pyplot as plt
import datetime


#######################
# European Call Class #
#######################


class CorridorOption(EuropeanDerivative):
    """Corridor option class
    """

    ###############
    # Constructor #
    ###############

    def __init__(self, S0, K1,K2, r, sigma, T):
        """Constructor of corridor option

        Args:
            S0 (float): price of asset at t=0
            K1 (float): lower bound in the payoff of corridor option's payoff
            K2 (float): upper bound in the payoff of corridor option's payoff
            r (float): interest rate
            sigma (float): volatility
            T (float): maturity in years
        """

        EuropeanDerivative.__init__(
            self, S0, (K1,K2), r, sigma, T, lambda x: 1 if (x >= K1 and x<=K2) else 0, "Corridor"
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
 
    N_max,step = 10_000,10
    eps_vega, epse_delta, eps_gamma = 0.01,1, 0.01
    NB_mc = np.linspace(0,N_max,int(N_max/step))

    ############################
    # Defining our call option #
    ############################

    T = 1
    S0 = 100
    sigma = 0.20
    r = 0.05
    K1, K2 = 75,85

    Corridor_option = CorridorOption(S0, K1,K2, r, sigma, T)

    ###########################################################
    # Greeks : exact vs finite difference method vs malliavin #
    ###########################################################

    start_time = datetime.datetime.now()

    VEGA_epsilon = np.array([
        Corridor_option.greeks_difference_method(
            N=i, epsilon=eps_vega, param__="vol", order=1
        )
        for i in range(1,N_max,step)
    ])
    DELTA_epsilon = np.array([
        Corridor_option.greeks_difference_method(
            N=i, epsilon=epse_delta, param__="price_0", order=1
        )
        for i in range(1,N_max,step)
    ])
    GAMMA_epsilon = np.array([
        Corridor_option.greeks_difference_method(
            N=i, epsilon=eps_gamma, param__="price_0", order=2
        )
        for i in range(1,N_max,step)
    ])

    VEGA_malliavin = np.array([
        Corridor_option.greeks_malliavin(N=i, param__="vol", order=1) for i in range(1,N_max,step)
    ])
    DELTA_malliavin = np.array([
        Corridor_option.greeks_malliavin(N=i, param__="price_0", order=1)
        for i in range(1,N_max,step)
    ])
    GAMMA_malliavin = np.array([
        Corridor_option.greeks_malliavin(N=i, param__="price_0", order=2)
        for i in range(1,N_max,step)
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
    print("ratio_finite_diference_to_malliavin Corridor option : ")
    print(f"- delta : {DELTA_epsilon.var()/DELTA_malliavin.var()}")
    print(f"- gamma : {GAMMA_epsilon.var()/GAMMA_malliavin.var()}")
    print(f"- vega : {VEGA_epsilon.var()/VEGA_malliavin.var()}")

    ########
    # plot #
    ########

    # Note that for plot adjustments I use VScode IDE ! 

    fig, ax = plt.subplots(1, 3, sharey=False, figsize=(24, 7))

    ax[0].plot(NB_mc,DELTA_epsilon, label="finite difference method", color="blue")
    ax[0].plot(NB_mc,DELTA_malliavin, label="maliavin method", color="red")
    ax[0].set_xlabel(r"Number of iterations")
    ax[0].set_ylabel(r"$\Delta$", fontsize=15)
    ax[0].grid()
    ax[0].legend()

    ax[1].plot(NB_mc,GAMMA_epsilon, label="finite difference method", color="blue")
    ax[1].plot(NB_mc,GAMMA_malliavin, label="maliavin method", color="red")
    ax[1].set_xlabel(r"Number of iterations")
    ax[1].set_ylabel(r"$\Gamma$", fontsize=15)
    ax[1].grid()
    ax[1].legend()

    ax[2].plot(NB_mc,VEGA_epsilon, label="finite difference method", color="blue")
    ax[2].plot(NB_mc,VEGA_malliavin, label="maliavin method", color="red")
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
