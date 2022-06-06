from math import sqrt

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LinearRegression
import sklearn.metrics as metrics

def plot_residuals(y, yhat):
    residual = y - yhat
    plt.figure(figsize = (11,11))
    plt.scatter(y, residual)
    plt.axhline(y = 0, ls = ':')
    plt.xlabel('y')
    plt.ylabel('Residual')
    plt.title('Baseline Residuals')

def regression_errors(y, yhat):
    reg_errors = {
        'SSE': yhat.shape[0]*metrics.mean_squared_error(y, yhat),
        'ESS': ((yhat-y.mean())**2).sum(),
        'TSS': ((y - y.mean())**2).sum(),
        'MSE': metrics.mean_squared_error(y, yhat),
        'RMSE': metrics.mean_squared_error(y, yhat)**(0.5),
        'R2':metrics.explained_variance_score(y, yhat)
    }
    return reg_errors

def baseline_mean_errors(y):
    df = pd.DataFrame(y)
    df['yhat'] = y.mean()
    baseline_err = {
        'SSE': y.size*metrics.mean_squared_error(df['taxvaluedollarcnt'], df['yhat']),
        'ESS': (((df['yhat'])-df['taxvaluedollarcnt'].mean())**2).sum(),
        'TSS': ((df['taxvaluedollarcnt'] - df['yhat'])**2).sum(),
        'MSE': metrics.mean_squared_error(df['taxvaluedollarcnt'], df['yhat']),
        'RMSE': metrics.mean_squared_error(df['taxvaluedollarcnt'], df['yhat'])**(0.5),
        'R2':metrics.explained_variance_score(df['taxvaluedollarcnt'], df['yhat'])
    }
    return baseline_err

def better_than_baseline(y, yhat):
    model_errors = regression_errors(y, yhat)
    model_errors['name'] = 'model'
    baseline_errors = baseline_mean_errors(y)
    baseline_errors['name'] = 'baseline'
    errors = [model_errors, baseline_errors]
    df = pd.DataFrame(errors).T
    df['model < baseline'] = df[0] < df[1]
    return df
