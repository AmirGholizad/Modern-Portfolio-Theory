# import necessary packages
import math
import numpy as np
import pandas as pd

# pass the address
Address = "C://Users/user/Desktop/Ghorbani_Finance/Ghorbani_Finance/Records"

# take the csv files and save them as Dataframes
Agas = pd.DataFrame(pd.read_csv(Address + "/Agas.csv"))
Agas = Agas[150::].reset_index(drop=True)
Agas = Agas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Agas"})

Almas = pd.DataFrame(pd.read_csv(Address + "/Almas.csv"))
Almas = Almas[150::].reset_index(drop=True)
Almas = Almas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Almas"})

Aminyekom = pd.DataFrame(pd.read_csv(Address + "/Aminyekom.csv"))
Aminyekom = Aminyekom[150::].reset_index(drop=True)
Aminyekom = Aminyekom[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Aminyekom"})

Asam = pd.DataFrame(pd.read_csv(Address + "/Asam.csv"))
Asam = Asam[150::].reset_index(drop=True)
Asam = Asam[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Asam"})

Asas = pd.DataFrame(pd.read_csv(Address + "/Asas.csv"))
Asas = Asas[150::].reset_index(drop=True)
Asas = Asas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Asas"})

Atimes = pd.DataFrame(pd.read_csv(Address + "/Atimes.csv"))
Atimes = Atimes[150::].reset_index(drop=True)
Atimes = Atimes[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Atimes"})

Atlas = pd.DataFrame(pd.read_csv(Address + "/Atlas.csv"))
Atlas = Atlas[150::].reset_index(drop=True)
Atlas = Atlas[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Atlas"})

Bazr = pd.DataFrame(pd.read_csv(Address + "/Bazr.csv"))
Bazr = Bazr[::].reset_index(drop=True)
Bazr = Bazr[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Bazr"})

Firouze = pd.DataFrame(pd.read_csv(Address + "/Firouze.csv"))
Firouze = Firouze[150::].reset_index(drop=True)
Firouze = Firouze[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Firouze"})

Ofogmellat = pd.DataFrame(pd.read_csv(Address + "/Ofogmellat.csv"))
Ofogmellat = Ofogmellat[150::].reset_index(drop=True)
Ofogmellat = Ofogmellat[["<COL14>", "<CLOSE>"]].rename(columns={"<COL14>": "Date", "<CLOSE>": "Ofogmellat"})

Total = pd.merge(Agas, Almas, on="Date")
Total = pd.merge(Total, Aminyekom, on="Date")
Total = pd.merge(Total, Asam, on="Date")
Total = pd.merge(Total, Asas, on="Date")
Total = pd.merge(Total, Atimes, on="Date")
Total = pd.merge(Total, Atlas, on="Date")
Total = pd.merge(Total, Bazr, on="Date")
Total = pd.merge(Total, Firouze, on="Date")
Total = pd.merge(Total, Ofogmellat, on="Date")

Total.to_csv(Address + "/Total.csv")


# Now we define the Functions

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
    Sigma = COV_Matrix(number, Portfolio(Total, t))
    w = np.dot(np.linalg.inv(Sigma) , L) / np.dot(np.dot(L, Sigma), L)

    return w

# define the Target function
def Portfo_STD(number, t):

    Sigma = COV_Matrix(number, Portfolio(Total, t))
    return np.dot(W(number, t), (np.dot(Sigma, W(number, t))))


# this dunction calculates the Portfolio Return
def Portfolio_Return(number, t):

    portfolio = Portfolio(Total, t)
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



# finally we define the CPPI (Constant proportion portfolio insurance) function
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


# And now we start to see the results!

# before everything we should upload our dataset
# you can change the address to whatever you whant
DataSet = Total
Address = "C://Users/user/Desktop/Ghorbani_Finance/Ghorbani_Finance/Results Folder"

# our assets are:
Assets = DataSet.columns
Assets = Assets[1::]

# first we calculate daily rates
Rates = Portfolio(DataSet, 1)
Rates.to_csv(Address + "/Rates.csv")

# now we can calculate the Semi STD for each asset
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
SemiVar = {}
SemiVar = {Assets[0]: Semi_Var(Symbol=Agas["Agas"], t=1)}
semivar = pd.DataFrame(SemiVar, index=[0])
semivar.to_csv(Address + "/semivar.csv")


# now we can calculate the Value At Risk for each asset and for given Z_alpha values(1.65 , 2.33)
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
ValueAtRisk1 = {}
ValueAtRisk2 = {}
ValueAtRisk1 = {Assets[0]: VAR(Symbol=Agas["Agas"], t=1, z=1.65)}
ValueAtRisk2 = {Assets[0]: VAR(Symbol=Agas["Agas"], t=1, z=2.33)}
VAR = pd.DataFrame([ValueAtRisk1, ValueAtRisk2])
VAR.to_csv(Address + "/VAR.csv")


# we can get the Z~ value for each asset and for given Z_alpha values(1.65 , 2.33)
# (the values for S and K will be calculated automatically)
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
Z1 = {}
Z2 = {}
Z1 = {Assets[0]: Z_alpha(Agas["Agas"], t=1, z=1.65)}
Z2 = {Assets[0]: Z_alpha(Agas["Agas"], t=1, z=2.33)}
Z12 = pd.DataFrame([Z1,Z2])
Z12.to_csv(Address + "/Z12.csv")


# and finally for the first part, we can get the VARmod
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
VARmod1 = {}
VARmod2 = {}
VARmod1 = {Assets[0]: VARmod(Agas["Agas"], t=1, z=1.65)}
VARmod2 = {Assets[0]: VARmod(Agas["Agas"], t=1, z=2.33)}
VARmod12 = pd.DataFrame([VARmod1,VARmod2])
VARmod12.to_csv(Address + "/VARmod12.csv")


# for the second part, we should create a Covariance Matrix
# in order to do that we must have the covariance between different assets in a given portfolio
SIGMA = COV_Matrix(10, DataSet)
sigma = pd.DataFrame(SIGMA)
sigma.to_csv(Address + "/sigma.csv")


# now we can find the Wheight Vector
W = W(10, 1)
w = pd.DataFrame(W)
w.to_csv(Address + "/w.csv")


# finally we can find the Rate of our Portfolio and the Sharp Ratio
# we must find the Standard Deviation of our Portfolio first
sigma_2 = Portfo_STD(10, 1)
R = Portfolio_Return(10, 1)
SR = Sharp_Ratio(10,1)


# eventually we can find the new CPPI value (Constant proportion portfolio insurance)
CPPInew = CPPI(Portfolio(Total, t=1))
CPPInew = pd.DataFrame(CPPInew, index=Total.columns[1::])
CPPInew.to_csv(Address + "/CPPInew.csv")