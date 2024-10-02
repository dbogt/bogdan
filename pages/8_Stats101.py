import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import streamlit as st

# Generating data for different R^2 values
np.random.seed(42)

# Dataset with R^2 = 1
x1 = np.array([1, 2, 3, 4, 5])
y1 = 2 * x1 + 1
r2_1 = r2_score(y1, y1)  # Perfect R-squared

# Dataset with R^2 = 1 Negatively correlated
x1_neg = np.array([1, 2, 3, 4, 5])
y1_neg = -2 * x1 + 1
r2_1_neg = r2_score(y1_neg, y1_neg)  # Perfect R-squared

# Dataset with R^2 = 0.8
x2 = np.random.rand(100) * 10
y2 = 2 * x2 + 1 + np.random.normal(0, 2, 100)
model_2 = LinearRegression().fit(x2.reshape(-1, 1), y2)
y2_pred = model_2.predict(x2.reshape(-1, 1))
r2_08 = r2_score(y2, y2_pred)

# Dataset with R^2 = 0
x3 = np.random.rand(100)
y3 = np.random.rand(100)
model_3 = LinearRegression().fit(x3.reshape(-1, 1), y3)
y3_pred = model_3.predict(x3.reshape(-1, 1))
r2_0 = r2_score(y3, y3_pred)

# Function to create scatter plot and line of best fit
def plot_r2_data(x, y, r2_value):
    title = f"R-squared = {r2_value:.4f}"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data'))
    
    # Best fit line
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    y_pred = model.predict(x.reshape(-1, 1))
    
    fig.add_trace(go.Scatter(x=x, y=y_pred, mode='lines', name='Line of Best Fit'))
    
    # Adding R-squared annotation
    fig.add_annotation(text=f'R-squared: {r2_value:.4f}',
                       xref="paper", yref="paper", showarrow=False,
                       x=0.50, y=0.95, bordercolor="black", borderwidth=2)
    
    fig.update_layout(title=title, xaxis_title='X', yaxis_title='Y')
    return fig

# Streamlit dashboard
st.title("Understanding R-Squared")

latext = r"""
### What is R-squared?

R-squared (R²) is a statistical measure that represents the proportion of the variance for a dependent variable 
that's explained by an independent variable or variables in a regression model. It provides an indication of 
goodness of fit and ranges from 0 to 1.

The formula for R-squared is:
$$
R^2 = 1 - \frac{\sum (y_i - \hat{y_i})^2}{\sum (y_i - \bar{y})^2}
$$

Where:
- $y_i$ are the observed values,
- $\hat{y_i}$ are the predicted values, and
- $\bar{y}$ is the mean of observed values.

- An R-squared of 1 means the model explains all variability of the target variable.
- An R-squared of 0.8 means the model explains 80% of the variance.
- An R-squared of 0 means the model explains none of the variance.
"""
st.markdown(latext)

st.plotly_chart(plot_r2_data(x1, y1, r2_1))
st.plotly_chart(plot_r2_data(x1_neg, y1_neg, r2_1))
st.plotly_chart(plot_r2_data(x2, y2, r2_08))
st.plotly_chart(plot_r2_data(x3, y3, r2_0))
