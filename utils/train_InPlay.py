# OS, misc.
import os
from pathlib import Path
import pickle 
from tqdm import tqdm

# Data analysis
import pandas as pd
# import modin.pandas as pd
import numpy as np
# import scipy.stats as stats
# import statsmodels.api as sm

# Bayesian inference
import pymc as pm
import arviz as az
import xarray as xr

import matplotlib.pyplot as plt

def main():

    # Get the data
    X, y = get_train_data()

    # Get model
    model = get_model(X, y)

    with model: 
        idata = pm.sample(1000,chains=4,return_inferencedata=True, idata_kwargs=dict(log_likelihood=False))

    # If trace exsits then delete it
    trace_file = Path("models/trace_InPlay.nc")
    if trace_file.exists():
        os.remove(trace_file)
    
    idata.to_netcdf(trace_file)

    # with open(Path("model/model.pkl"), 'wb') as fl:
    #     temp = {'model': model}
    #     pickle.dump(temp,fl)    

def get_train_data():
    # Load data
    print("Loading data...")
    X = pd.read_csv(Path("data/InPlay/x_train.csv")).drop(["Unnamed: 0"],axis=1)
    y = pd.read_csv(Path("data/InPlay/y_train.csv")).drop(["Unnamed: 0"],axis=1)
    return X, y

def get_validation_data():
    # Load data
    print("Loading data...")
    X = pd.read_csv(Path("data/InPlay/x_validation.csv")).drop(["Unnamed: 0"],axis=1)
    y = pd.read_csv(Path("data/InPlay/y_validation.csv")).drop(["Unnamed: 0"],axis=1)
    return X, y

def get_model(X_train, y_train):
    
    # pymc model
    print("Building model...")
    coords={'index': X_train.index, 'columns': X_train.columns}

    with pm.Model(coords=coords) as model:

        # Define priors 
        beta0 = pm.Normal("beta0", mu=0, sigma=100)
        beta1 = pm.Normal("beta1", mu=0, sigma=100)
        beta2 = pm.Normal("beta2", mu=0, sigma=100)
        beta3 = pm.Normal("beta3", mu=0, sigma=100)
        beta4 = pm.Normal("beta4", mu=0, sigma=100)
        # beta = pm.Normal("beta",mu=0,sigma=100,dims='columns')
        
        # Define data - not pretty but kind of how it has to be done
        velo = pm.Data("velo",X_train["Velo"],mutable=True)
        spin = pm.Data("spin",X_train["SpinRate"],mutable=True)
        horz = pm.Data("horz",X_train["HorzBreak"],mutable=True)
        vert = pm.Data("vert",X_train["InducedVertBreak"],mutable=True)

        # Likelihood
        # formula = beta0 + beta1*X_train["Velo"].to_numpy() + beta2*X_train["SpinRate"].to_numpy() + beta3*X_train["HorzBreak"].to_numpy() + beta4*X_train["InducedVertBreak"].to_numpy()
        # formula = beta0 + beta1*X_train["Velo"] + beta2*X_train["SpinRate"] + beta3*X_train["HorzBreak"] + beta4*X_train["InducedVertBreak"]
        formula = beta0 + beta1*velo + beta2*spin + beta3*horz + beta4*vert
        
        # formula = pm.
        p = pm.Deterministic("p",pm.math.invlogit(formula))

        # Outcome
        outcome = pm.Bernoulli("outcome",p=p,observed=y_train["InPlay"])
        # p = pm.Bernoulli("p",p=likelihood,observed=y_train.to_numpy().astype("int"))

    # --> This can help with dimensions and multiplying coeffs and data: https://www.pymc.io/projects/docs/en/stable/learn/core_notebooks/posterior_predictive.html
    # with pm.Model(coords=coords) as model:
    #     beta = pm.Normal("beta",mu=0,sigma=100,dims='columns')
    #     shared = pm.Data("shared", X_train, dims=("index","columns"))
    #     # formula = pm.math.dot(beta,shared)
    #     p = pm.Deterministic("p",pm.math.invlogit(pm.math.dot(beta,shared)))

    #     #     # Outcome
    #     outcome = pm.Bernoulli("outcome",p=p,observed=y_train["InPlay"])

    return model


if __name__ == '__main__':
    main()