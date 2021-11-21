#Developing a Pairs Trading strategy for the Indian Banking sector
#Simple regression line plotting between scrips of Axis Bank and ICICI Bank
#Part of Capstone Project - for MOOC on Advanced Trading Algorithms, ISB on Coursera

#******************************************************************

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

datasets = pd.read_csv('AXIS.NS.csv')  #Importing the datasets
datasets = pd.read_csv('ICICI.NS.csv')

X = datasets.iloc[:, :-1].values
Y = datasets.iloc[:, 1].values

from sklearn.model_selection import train_test_split   #Splitting the dataset into the Training set and Test set
X_Train, X_Test, Y_Train, Y_Test = train_test_split(X, Y, test_size = 1/3, random_state = 0)

#Fitting simple Linear Regression to the training set
from sklearn.linear_model import LinearRegression
regressor = LinearRegression()
regressor.fit(X_Train, Y_Train)

Y_Pred = regressor.predict(X_Test)   #Predicting the Test set result

plt.scatter(X_Train, Y_Train, color = 'blue')   #Visualising the Training set results
plt.plot(X_Train, regressor.predict(X_Train), color = 'yellow')
plt.title('Price AXISBANK vs. ICICIBANK (Training Set)')
plt.xlabel('Price change')
plt.ylabel('Regression coefficient')
plt.show()

plt.scatter(X_Test, Y_Test, color = 'blue')   #Visualising the Test set results
plt.plot(X_Train, regressor.predict(X_Train), color = 'yellow')
plt.title('Price AXISBANK vs. ICICIBANK (Test Set)')
plt.xlabel('Price change')
plt.ylabel('Regression')
plt.show()
