# import necessary packages
import math
import numpy as np
import pandas as pd
import Take_Data



# define a simple normalization function
def Normalization(data):

    data_min = np.min(data)
    data_max = np.max(data)
    data_normalized = np.zeros(len(data))

    for k in range(0,len(data)):
        data_normalized[k] = (data[k]-data_min)/(data_max-data_min)

    return data_normalized

# define the third moment function for a data distribution
def Skewness(data):

    skew = np.average( ( (data-np.average(data)) / np.std(data) )**3 )

    return skew

# define the fourth moment function for a data distribution
def Kurtosis(data):

    kurtosis = np.average( ( (data-np.average(data)) / np.std(data) )**4 )

    return kurtosis

# define the Rate function ('Symbol' is the given time serie and 't' is called the period)
def R(Symbol, t):

    r = np.zeros(len(Symbol) - t)
    p = Symbol

    for i in range(0,len(p)-1):
        r[i] = (p[i+1]/p[i])-1

    r_percent = (item*100 for item in r)
    r_normal = Normalization(r)
    rates_frame = pd.DataFrame({"Rates":r, "Rates%":r_percent, "Normalized Rates": r_normal})

    return rates_frame


# define a function which gives the portfolio(names and rates)
def Portfolio(Dataset, t):

    Dataset_Columns = Dataset.columns[1::]

    Rates = {}

    for symbol in Dataset_Columns:
        Rates[symbol] = R(Dataset[symbol], t)["Rates"]

    portfolio = pd.DataFrame(Rates)

    return portfolio

# define the Semi Variance function ('Symbol' is the given time serie and 't' is called the period)
def Semi_Var(Symbol, t):

    Rates = R(Symbol, t)["Rates"]
    Avg_R = np.average(Rates)

    R_I = []
    for rate in Rates:
        if rate < Avg_R:
            R_I.append(rate)
    semi_var =math.sqrt( ( np.sum( ( R_I - Avg_R )**2 )/( len( R_I ) ) ) )

    return semi_var


# define the Value At Risk function
def VAR(Symbol, t, z):

    value_at_risk = - np.average(R(Symbol, t)["Normalized Rates"]) + np.std(R(Symbol, t)["Normalized Rates"]) + z

    return value_at_risk

# define the Z~ function
def Z_alpha(Symbol, t, z):

    S = Skewness(R(Symbol, t)["Rates"])
    K = Kurtosis(R(Symbol, t)["Rates"])

    z_alpha = z + S*(z**2 - 1)/6 + (K-3)*(z**3 - 3*z)/24 - (S**2)*(2*(z**3)-5*z)/36

    return z_alpha

# define the VARmod function
def VARmod(Symbol, t, z):

    r = R(Symbol, t)["Rates"]
    Z = Z_alpha(Symbol, t, z)
    varmod = np.average(r) + Z + np.std(r)

    return varmod

# define the Covariance function
def COV(rate1, rate2):

    cov = 0
    Avg_rate1 = np.average(rate1)
    Avg_rate2 = np.average(rate2)
    for i in range(0,len(rate1)):
        cov = cov + (rate1[i] - Avg_rate1) * (rate2[i] - Avg_rate2)
    cov = cov / len(rate1)

    return cov

# define a function which creates the Covariance Matrix
def COV_Matrix(number, portfolio):

    cov_matrix = np.zeros((number,number))
    portfolio_names = portfolio.columns

    for i in range(0,number):
        for j in range(0,number):
            cov_matrix[i][j] = COV(portfolio[portfolio_names[i]],portfolio[portfolio_names[j]])

    return cov_matrix

# define Wheight function
def W(number, t):

    L = np.ones(number)
    Sigma = COV_Matrix(number, Portfolio(Take_Data.Total, t))
    w = np.dot(np.linalg.inv(Sigma) , L) / np.dot(np.dot(L, Sigma), L)

    return w

# define the Target function
def Portfo_STD(number, t):

    Sigma = COV_Matrix(number, Portfolio(Take_Data.Total, t))
    return np.dot(W(number, t), (np.dot(Sigma, W(number, t))))


# this dunction calculates the Portfolio Return
def Portfolio_Return(number, t):

    portfolio = Portfolio(Take_Data.Total, t)
    Assets = portfolio.columns

    Avg_Total_Rate = []

    for asset in Assets:
        Avg_Total_Rate.append(np.average(portfolio[asset]))

    return np.dot(W(number, t), Avg_Total_Rate)


# this function calculates the Sharp Ratio
def Sharp_Ratio(number, t):

    R_P = Portfolio_Return(number, t)
    R_F = 0.0005
    sigma_p = Portfo_STD(number, t)
    sigma_f = 0

    return (R_P - R_F)/(sigma_p - sigma_f)



#
def CPPI(Portfo):

    Asset_Rate_list = Portfo.columns
    CPPI = 1000
    F = 800
    M = 3
    r_f = 0.0125
    I = M * (CPPI - F)
    H = CPPI - I
    CPPInew = np.zeros((len(Asset_Rate_list), len(Portfo)))

    j=0
    for asset in Asset_Rate_list:
        for i in range(0,len(Portfo)):
            CPPInew[j][i] = (1 + Portfo[asset][i]) * I + H * (1 + r_f)
        j = j + 1

    return CPPInew



VAR(Agas['Agas'], t=1, z=1.66)