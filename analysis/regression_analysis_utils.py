# a python file with lots of helper functions for regression analysis
import pandas as pd
import numpy as np
import os
import re
from datetime import date, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
import statsmodels.api as sm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


def log_reg(log_data):
    X = log_data.loc[:, log_data.columns != 'gender']
    y = log_data.loc[:, log_data.columns == 'gender']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

    logreg = LogisticRegression(solver='lbfgs',max_iter=500)

    logreg.fit(X_train,y_train.values.ravel())

    # Predict the labels of the test set:
    y_pred = logreg.predict(X_test)

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    logit_model=sm.Logit(y,X)
    result=logit_model.fit()
    print(result.summary2())

def linear_regression(dfx, dfy):
    x = dfx
    y = dfy

    regression_model = LinearRegression()
    # Fit
    regression_model.fit(x, y)
    # Predict
    y_predicted = regression_model.predict(x)

    # model evaluation
    rmse = mean_squared_error(y, y_predicted)
    r2 = r2_score(y, y_predicted)

    # printing values
    print('Coefficient:' ,regression_model.coef_)
    print('Intercept:', regression_model.intercept_)
    print('Root mean squared error: ', rmse)
    print('R2 score: ', r2)

    # adding intercept constant (sm doesn't)
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    predictions = model.predict(x) 

    print_model = model.summary()
    print(print_model)
