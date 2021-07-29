import pandas as pd
import Funcs
import Take_Data

# before everything we should upload our dataset
# you can change the address to whatever you whant
DataSet = Take_Data.Total
Address = "C:\\Users\TheAMG\Desktop\Ghorbani_Finance\Results Folder"

# our assets are:
Assets = DataSet.columns
Assets = Assets[1::]

# first we calculate daily rates
Rates = Funcs.Portfolio(DataSet, 1)
Rates.to_csv(Address + "\Rates.csv")

# now we can calculate the Semi STD for each asset
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
SemiVar = {}
SemiVar = {Assets[0]: Funcs.Semi_Var(Symbol=Take_Data.Agas["Agas"], t=1)}
semivar = pd.DataFrame(SemiVar, index=[0])
semivar.to_csv(Address + "\semivar.csv")


# now we can calculate the Value At Risk for each asset and for given Z_alpha values(1.65 , 2.33)
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
ValueAtRisk1 = {}
ValueAtRisk2 = {}
ValueAtRisk1 = {Assets[0]: Funcs.VAR(Symbol=Take_Data.Agas["Agas"], t=1, z=1.65)}
ValueAtRisk2 = {Assets[0]: Funcs.VAR(Symbol=Take_Data.Agas["Agas"], t=1, z=2.33)}
VAR = pd.DataFrame([ValueAtRisk1, ValueAtRisk2])
VAR.to_csv(Address + "\VAR.csv")


# we can get the Z~ value for each asset and for given Z_alpha values(1.65 , 2.33)
# (the values for S and K will be calculated automatically)
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
Z1 = {}
Z2 = {}
Z1 = {Assets[0]: Funcs.Z_alpha(Take_Data.Agas["Agas"], t=1, z=1.65)}
Z2 = {Assets[0]: Funcs.Z_alpha(Take_Data.Agas["Agas"], t=1, z=2.33)}
Z12 = pd.DataFrame([Z1,Z2])
Z12.to_csv(Address + "\Z12.csv")


# and finally for the first part, we can get the VARmod
#       ******       You should pass the Symbol in this format: Symbol=Take_Data.Symbol["Symbol"]      ******
VARmod1 = {}
VARmod2 = {}
VARmod1 = {Assets[0]: Funcs.VARmod(Take_Data.Agas["Agas"], t=1, z=1.65)}
VARmod2 = {Assets[0]: Funcs.VARmod(Take_Data.Agas["Agas"], t=1, z=2.33)}
VARmod12 = pd.DataFrame([VARmod1,VARmod2])
VARmod12.to_csv(Address + "\VARmod12.csv")


# for the second part, we should create a Covariance Matrix
# in order to do that we must have the covariance between different assets in a given portfolio
SIGMA = Funcs.COV_Matrix(10, DataSet)
sigma = pd.DataFrame(SIGMA)
sigma.to_csv(Address + "\sigma.csv")


# now we can find the Wheight Vector
W = Funcs.W(10, 1)
w = pd.DataFrame(W)
w.to_csv(Address + "\w.csv")


# finally we can find the Rate of our Portfolio and the Sharp Ratio
# we must find the Standard Deviation of our Portfolio first
sigma_2 = Funcs.Portfo_STD(10, 1)
R = Funcs.Portfolio_Return(10, 1)
SR = Funcs.Sharp_Ratio(10,1)


# eventually we can find the new CPPI value (Constant proportion portfolio insurance)
CPPInew = Funcs.CPPI(Funcs.Portfolio(Take_Data.Total, t=1))
CPPInew = pd.DataFrame(CPPInew, index=Take_Data.Total.columns[1::])
CPPInew.to_csv(Address + "\CPPInew.csv")