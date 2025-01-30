import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data'))
    
    # Best fit line
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    y_pred = model.predict(x.reshape(-1, 1))
    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    coef = model.coef_[0]
    y_int = model.intercept_
    title = f"R-squared = {r2_value:.4f}; MAE = {mae:.4f}; MSE = {mse:.4f}; RMSE = {rmse:.4f} <br><sup>Equation: y = {coef:.4f} * x + {y_int:.4f}</sup>"
    
    fig.add_trace(go.Scatter(x=x, y=y_pred, mode='lines', name='Line of Best Fit'))
    
    # Adding R-squared annotation
    fig.add_annotation(text=f'R-squared: {r2_value:.4f}',
                       xref="paper", yref="paper", showarrow=False,
                       x=0.50, y=0.95, bordercolor="black", borderwidth=2)
    
    #fig.update_layout(title=dict(text=title, subtitle=dict(text="test")), xaxis_title='X', yaxis_title='Y')
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

#%% Anscombie's Quartet
st.title("Anscombie's Quartet")
aq_df = sns.load_dataset("anscombe")
# Summary statistics
def summary_stats(group):
    model = sm.OLS(group["y"], sm.add_constant(group["x"])).fit()
    return pd.DataFrame({
        "X Mean": group["x"].mean(),
        "Y Mean": group["y"].mean(),
        "X Variance": group["x"].var(),
        "Y Variance": group["y"].var(),
        "Correlation": group["x"].corr(group["y"]),
        "Regression Slope": model.params[1],
        "R-squared": model.rsquared
    }, index=[group.name])

stats = aq_df.groupby("dataset").apply(summary_stats).reset_index(drop=True)
st.write(stats)

#%% Experiment
st.title("Experiment with your own line of best fit")

pickCol1, pickCol2 = st.columns(2)
coeff_pick = pickCol1.slider("Pick coefficient (slope)",-10.0,10.0,2.0,step=0.05)
int_pick = pickCol2.slider("Pick y-intercept",-10.0,10.0,1.0,step=0.05)

# Dataset with R^2 = 0.8
x = np.random.rand(100) * 10
y = 2 * x + 1 + np.random.normal(0, 2, 100)
y_pick = coeff_pick * x + int_pick
model = LinearRegression().fit(x.reshape(-1, 1), y)
y_pred = model.predict(x.reshape(-1, 1))
r2 = r2_score(y, y_pred)
r2_pick = r2_score(y, y_pick)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='markers', name='Data'))
fig.add_trace(go.Scatter(x=x, y=y_pred, mode='lines', name='Line of Best Fit'))
fig.add_trace(go.Scatter(x=x, y=y_pick, mode='lines', name='Picked Line of Best Fit'))

# Adding R-squared annotation
fig.add_annotation(text=f'R-squared: {r2:.4f}',
                       xref="paper", yref="paper", showarrow=False,
                       x=0.50, y=0.95, bordercolor="black", borderwidth=2)
mae = mean_absolute_error(y, y_pred)
mse = mean_squared_error(y, y_pred)
rmse = np.sqrt(mse)

mae_pick = mean_absolute_error(y, y_pick)
mse_pick = mean_squared_error(y, y_pick)
rmse_pick = np.sqrt(mse_pick)

coef = model.coef_[0]
y_int = model.intercept_

col1, col2, col3, col4 = st.columns(4)
col1.metric("R-Squared - best", f"{r2:.4f}")
col1.metric("R-Squared - pick", f"{r2_pick:.4f}")
col2.metric("MAE - best", f"{mae:.4f}")
col2.metric("MAE - pick", f"{mae_pick:.4f}")
col3.metric("MSE - best", f"{mse:.4f}")
col3.metric("MSE - pick", f"{mse_pick:.4f}")
col4.metric("RMSE - best", f"{rmse:.4f}")
col4.metric("RMSE - pick", f"{rmse_pick:.4f}")

title = f"Best Fit Equation: y = {coef:.4f} * x + {y_int:.4f} <br><sup>Picked Line Equation: y = {coeff_pick:.4f} * x + {int_pick:.4f}</sup>"

fig.update_layout(title=title, xaxis_title='X', yaxis_title='Y')
st.plotly_chart(fig)

df = pd.DataFrame({'X':x,'Y':y,'Y-Pred':y_pred,'Y-Pick':y_pick})
df['Residuals - Best Fit'] = df['Y'] - df['Y-Pred']
df['Residuals - Pick'] = df['Y'] - df['Y-Pick']
df['Res^2 - Best'] = df['Residuals - Best Fit'] ** 2
df['Res^2 - Pick'] = df['Residuals - Pick'] ** 2
df['Res Abs - Best'] = df['Residuals - Best Fit'].abs()
df['Res Abs - Pick'] = df['Residuals - Pick'].abs()
SSE_best = df['Res^2 - Best'].sum()
SSE_pick = df['Res^2 - Pick'].sum()
MSE_best = df['Res^2 - Best'].mean()
MSE_pick = df['Res^2 - Pick'].mean()
MAE_best = df['Res Abs - Best'].mean()
MAE_pick = df['Res Abs - Pick'].mean()

df_summary = pd.DataFrame( {'SSE':[SSE_best,SSE_pick], 'MSE':[MSE_best,MSE_pick], 'MAE':[MAE_best,MAE_pick]}, index=['Best fit','Picked line'])

st.write(f"Sum of squared errors (line of best fit): {SSE_best:.4f}")
st.write(f"Sum of squared errors (picked line): {SSE_pick:.4f}")
st.write(df_summary)
st.write(df)

latext2=r"""
### Mean Squared Error (MSE)

Mean Squared Error is the average of the squared differences between the observed actual outcomes and the outcomes predicted by the model. It's useful because it gives a larger penalty to larger errors.

The formula for MSE is:

$$
MSE = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y_i})^2
$$

Where:
- $y_i$ are the observed values,
- $\hat{y_i}$ are the predicted values.

### Root Mean Squared Error (RMSE)

RMSE is the square root of MSE. It brings the unit back to the original scale of the target variable, making it easier to interpret.

The formula for RMSE is:

$$
RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y_i})^2}
$$

### Mean Absolute Error (MAE)

MAE is the average of the absolute differences between the observed actual outcomes and the outcomes predicted by the model. It's a more robust metric compared to MSE as it doesn't exaggerate the effect of large errors.

The formula for MAE is:

$$
MAE = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y_i}|
$$
"""
st.markdown(latext2)


### Logistic Regression
# Streamlit dashboard
st.title("Understanding Logistic Regression")

st.markdown(r"""
### What is Logistic Regression?

Logistic regression is a type of regression analysis used to predict the probability of a binary outcome (1 or 0) 
based on one or more independent variables. It models the probability that a given input belongs to the class '1', 
using the logistic (sigmoid) function.

The model predicts the probability as follows:

$$
P(y=1 | x) = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \dots + \beta_n x_n)}}
$$

Where:
- $ \beta_0 $ is the intercept (bias term),
- $ \beta_1, \dots, \beta_n $ are the coefficients for the features $ x_1, \dots, x_n $,
- $ z = \beta_0 + \beta_1 x_1 + \dots + \beta_n x_n $ is the linear combination of input features,
- $ \sigma(z) = \frac{1}{1 + e^{-z}} $ is the sigmoid function.

The output of the sigmoid function is a probability between 0 and 1, which can be interpreted as the likelihood that the input belongs to the positive class (1).

""")


# Function to calculate sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Generate data for sigmoid function
z_values = np.linspace(-10, 10, 500)  # Values for z = beta_0 + beta_1 * x
sigmoid_values = sigmoid(z_values)

# Example coefficients for logistic regression (beta_0 and beta_1)
st.header("Draw your own sigmoid")
c1, c2 = st.columns(2)
beta_0 = c1.slider("Enter beta_0 (intercept):",-50.0,50.0,0.0,step=0.5)  # Intercept
beta_1 = c2.slider("Enter beta_1 (coefficient):",-10.0,10.0,1.0,step=0.5)  # Coefficient for feature x

# sigTextEq = rf"""
# $$
# P(y=1 | x) = \frac{1}{1 + e^{-({beta_0} + {beta_1} x_1)}}
# $$
# """



# st.write(sigTextEq)

# Linear combination: z = beta_0 + beta_1 * x
x_values = np.linspace(-10, 10, 500)
z_comb = beta_0 + beta_1 * x_values
sigmoid_comb = sigmoid(z_comb)

# Create a plot for the sigmoid function
fig = go.Figure()
fig.add_trace(go.Scatter(x=z_values, y=sigmoid_values, mode='lines', name='Sigmoid Function'))
fig.add_trace(go.Scatter(x=x_values, y=sigmoid_comb, mode='lines', name='Sigmoid with Coefficients'))

# Adding labels and title
fig.update_layout(title="Sigmoid Function for Logistic Regression",
                  xaxis_title="z = β₀ + β₁x",
                  yaxis_title="σ(z) = 1 / (1 + exp(-z))")

st.plotly_chart(fig)

#%% Sample Data
hours = [1.1, 1.5, 1.9, 2.5, 2.5, 2.5, 2.7, 2.7, 3.2, 3.3, 3.5, 3.8, 4.5, 4.5, 4.8, 5.1, 5.5, 5.9, 6.1, 6.9, 7.4, 7.7, 7.8, 8.3, 8.5, 8.9, 9.2]
passFail = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
examDF = pd.DataFrame({'Hours':hours, 'Outcome':passFail})
st.write(examDF)                      
clf = LogisticRegression()
clf.fit(examDF[['Hours']],examDF['Outcome'])
model_int = clf.intercept_
model_coef = clf.coef_
st.write(f"Model Intercept: {model_int}, Model Coefficient: {model_coef}")

st.sidebar.title("Sections")
linksViews = """
- [**R-Squared**](#understanding-r-squared)
    - [**What is R-squared**](#what-is-r-squared)
- [**Experiment Line of Best Fit**](#experiment-with-your-own-line-of-best-fit)
    - [**Mean Squared Error (MSE)**](#mean-squared-error-mse)
    - [**Root Mean Squared Error (RMSE)**](#root-mean-squared-error-rmse)
    - [**Mean Absolute Error (MAE)**](#mean-absolute-error-mae)
- [**Logistic Regression**](#understanding-logistic-regression)"""

st.sidebar.write(linksViews)


