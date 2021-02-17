# Malliavin Calculus and Applications to Mathematical Finance : Greeks computation 

Authors : [Anas ESSOUNAINI](https://www.linkedin.com/in/anas-essounaini-b7514014a/) | [Rida LAARACH](https://www.linkedin.com/in/rida-laarach/?originalSubdomain=fr)

Supervisor : [Prof. Noufel Frikha](https://www.lpsm.paris/pageperso/frikha/) | [M2MO - Université de Paris VII](https://masterfinance.math.univ-paris-diderot.fr/) 

## Table of Contents

- [About](#about)
- [Repository structure](#repo)
- [Experiments](#res)
- [References](#ref)

## About <a name = "about"></a>

The Malliavin calculus, also referred to as stochastic calculus of variations, allows to establish
integration by parts formulas on the Wiener space that write : for some smooth function <a href="https://www.codecogs.com/eqnedit.php?latex=f" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f" title="f" /></a>,
<a href="https://www.codecogs.com/eqnedit.php?latex=\partial_xE[f(X_T&space;)G]&space;=&space;E[f(X_T&space;)H(X_T&space;,&space;G)]" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\partial_xE[f(X_T&space;)G]&space;=&space;E[f(X_T&space;)H(X_T&space;,&space;G)]" title="\partial_xE[f(X_T )G] = E[f(X_T )H(X_T , G)]" /></a> for some explicit
weight <a href="https://www.codecogs.com/eqnedit.php?latex=H(X_T&space;,&space;G)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?H(X_T&space;,&space;G)" title="H(X_T , G)" /></a>, where <a href="https://www.codecogs.com/eqnedit.php?latex=X_T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?X_T" title="X_T" /></a> is the solution taken at time <a href="https://www.codecogs.com/eqnedit.php?latex=T" target="_blank"><img src="https://latex.codecogs.com/gif.latex?T" title="T" /></a> of some non-degenerate stochastic
differential equation. It has many applications, notably in mathematical finance for the computation of Greeks for Delta hedging purpose.
The aims of this project are : 

    • to understand the basic principle of Malliavin calculus,

    • to implement the method in some simple examples related to the computation of Greeks
    of financial derivatives.

## Repository structure <a name = "repo"></a>

```
Malliavin-Calculus-Greeks-Monte-Carlo
|---Readme.md
|---.gitignore
|---.gitattributes
|---figures ==> Results of the simulations
|---scripts
|   |---abstract_derivative.py ==> Abstract derivative class
|   |---european_derivative.py ==> Representation of 
|                                  european derivatives
|   |---european_call.py ==> European call class (to run)
|                            with simulations for euopean call
|   |---digital_option.py ==> digital option class (to run)
|                              with simulation for digital  
|                                options
|   
|   |---corridor_option.py ==> corridor option class 
|                                    (to run) with simulations
|
|---doc
    |---report.pdf
    |---slides.pdf
```

## Experiments <a name = "res"></a>

### Figures : 

| ![european_call.png](figures/european_call.png) | 
|:--:| 
| *European call greeks : Finite Difference Vs. Malliavin* |

| ![digital_call.png](figures/digital_option.png) | 
|:--:| 
| *Digital option greeks : Finite Difference Vs. Malliavin* |

| ![european_call.png](figures/corridor_option.png) | 
|:--:| 
| *Corridor option greeks : Finite Difference Vs. Malliavin* |



### Numerical results



| <a href="https://www.codecogs.com/eqnedit.php?latex=\frac{Var_{finite&space;difference}}{Var_{malliavin}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\frac{Var_{finite&space;difference}}{Var_{malliavin}}" title="\frac{Var_{finite-difference}}{Var_{malliavin}}" /></a>| <a href="https://www.codecogs.com/eqnedit.php?latex=\Delta" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\Delta" title="\Delta" /></a> | <a href="https://www.codecogs.com/eqnedit.php?latex=\Gamma" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\Gamma" title="\Gamma" /></a>| <a href="https://www.codecogs.com/eqnedit.php?latex=\nu" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\nu" title="\nu" /></a> |
|---------------------------------------------|----------|-------------------|---------|
| Vanilla option                              | 0.40     | 13.21             | 3.93    |
| Binary option                               | 41.49    | 14740486587957.42 | 5.92    |
| Corridor option                             | 88.39    | 61324868176022.72 | 152.49  |

## References <a name = "ref"></a>

[1] Fournié, E. and Lasry, J.-M. and Lebuchoux, J. and Lions, P.-L. and Touzi, N, Applications
of Malliavin calculus to Monte Carlo methods in finance, Finance and Stochastics, Volume 3,
Number 4 (1999), 391–412.

[2] Fournié, E. and Lasry, J.-M. and Lebuchoux, J. and Lions, P.-L. Applications of Malliavin
calculus to Monte-Carlo methods in finance. II, Finance and Stochastics, Volume 5, Number 2
(2001), 201–236.
