
from asian_option import AsianDerivative

#############################
# Corridor Asian Derivative #
#############################

class CorridorOption(AsianDerivative):

    #####################
    # Super Constructor #
    #####################

    def __init__(self, S0, r, sigma, T, K1, K2, m=365):
        AsianDerivative.__init__(self, S0, r, sigma, T, [K1, K2], lambda x: 1 if (x >= K1 and x <= K2) else 0, "corridor", m)
    

    def __delta__malliavin(self,N):
        sum = 0
        params__ = self.params.copy()
        r, T, S0, sigma, = (
            self.params["interest_rate"],
            self.params["maturity"],
            self.params["price_0"],
            self.params["vol"],
        )
        T = np.linspace(0, self.params['maturity'], self.integration_nb)
        for i in range(N):
            W = brownian_motion(self.params['maturity'], self.integration_nb)
            S_T = S0*np.exp((r-(sigma**2)/2)*T+sigma*W)
            
            integral_S_T = np.sum(S_T[1:])/self.integration_nb

            #TODO Derivative formula
            if self.payoff_cum(integral_S_T) ==1:





if __name__ == "__main__":

    T = 1
    S0 = 100
    sigma = 0.20
    r = 0.05
    K1, K2 = 50,100

    asian_option = CorridorOption(
        S0, r, sigma, T, K1,K2)
    #print(asian_option.price_monte_carlo(200))
    print(asian_option.greeks_difference_method(20000, 0.01, 'price_0', 1))