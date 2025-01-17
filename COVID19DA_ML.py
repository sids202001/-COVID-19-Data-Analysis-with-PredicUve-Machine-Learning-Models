# -*- coding: utf-8 -*-
"""COVID19DA_ML.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YkWcpcqsmKBMZLAbmrLXYGIzPS17KNpw
"""

# -*- coding: utf-8 -*-
"""To import dataset from drive to Google Colab."""

# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

from google.colab import files
# Upload files from your local drive
uploaded_files = files.upload()

# Read in the dataset
dframe = pd.read_csv('country_wise_latest.csv')

# Display the total number of rows and columns in the dataset
print('Number of rows:', dframe.shape[0])
print('Number of columns:', dframe.shape[1])

# Correlation matrix for specified columns
print(dframe[['Confirmed', 'Deaths', 'Recovered']].corr())

# Display the first few rows of the dataset
print(dframe.head())

# Check for missing values in the dataset
print('Missing values in each column:')
print(dframe.isnull().sum())

# Check for duplicate rows in the dataset
duplicates = dframe[dframe.duplicated()]
print('Duplicate rows in the dataset:')
print(duplicates)

# Display information about the dataset
dframe.info()

# Check for unique values in the 'Country/Region' column
print('Unique countries/regions:')
print(dframe['Country/Region'].unique())

# Display counts of unique values in the 'Country/Region' column
print(dframe['Country/Region'].value_counts())

# Calculate and print the highest number of confirmed COVID cases
max_confirmed = dframe['Confirmed'].max()
print('Highest number of confirmed cases:', max_confirmed)

# Calculate and print the lowest number of confirmed COVID cases
min_confirmed = dframe['Confirmed'].min()
print('Lowest number of confirmed cases:', min_confirmed)

# Calculate descriptive statistics for the 'Confirmed' column
mean_confirmed = dframe['Confirmed'].mean()
median_confirmed = dframe['Confirmed'].median()
mode_confirmed = dframe['Confirmed'].mode()[0]
variance_confirmed = dframe['Confirmed'].var()
std_dev_confirmed = dframe['Confirmed'].std()

# Print the descriptive statistics
print("Mean confirmed cases:", mean_confirmed)
print("Median confirmed cases:", median_confirmed)
print("Mode of confirmed cases:", mode_confirmed)
print("Variance of confirmed cases:", variance_confirmed)
print("Standard deviation of confirmed cases:", std_dev_confirmed)

# Univariate analysis of the 'Recovered' column
plt.hist(dframe['Recovered'])
plt.title("Histogram of Recovered Cases")
plt.xlabel("Recovered")
plt.ylabel("Frequency")
plt.show()

# Calculate and print additional statistics for the 'Recovered' column
mean_recovered = dframe['Recovered'].mean()
median_recovered = dframe['Recovered'].median()
mode_recovered = dframe['Recovered'].mode()[0]
range_recovered = dframe['Recovered'].max() - dframe['Recovered'].min()
variance_recovered = dframe['Recovered'].var()
std_dev_recovered = dframe['Recovered'].std()

print("Mean of recovered cases:", mean_recovered)
print("Median of recovered cases:", median_recovered)
print("Mode of recovered cases:", mode_recovered)
print("Range of recovered cases:", range_recovered)
print("Variance of recovered cases:", variance_recovered)
print("Standard deviation of recovered cases:", std_dev_recovered)


# Define the variable of interest
variable = "Deaths"

# Print the data type of the 'Deaths' column
print("Data type:", dframe[variable].dtype)

# Create a histogram for the 'Deaths' column
plt.hist(dframe[variable])
plt.title("Histogram of Deaths")
plt.xlabel(variable)
plt.ylabel("Frequency")
plt.show()

# Calculate and print basic statistics for the 'Deaths' column
mean = dframe[variable].mean()
median = dframe[variable].median()
mode = dframe[variable].mode()[0]

print("Mean:", mean)
print("Median:", median)
print("Mode:", mode)

# Calculate range, variance, and standard deviation for the 'Deaths' column
range_deaths = dframe[variable].max() - dframe[variable].min()
variance = dframe[variable].var()
std_dev = dframe[variable].std()

print("Range:", range_deaths)

# Display summary statistics for confirmed, deaths, and recovered cases
print(dframe[['Confirmed', 'Deaths', 'Recovered']].describe())

# Generate a pairplot of the dataset to analyze multivariate relationships
sns.pairplot(dframe)
plt.show()

# Display correlation matrices for various combinations of COVID-related variables
print(dframe[['Confirmed', 'Deaths']].corr())
print(dframe[['Confirmed', 'Recovered']].corr())
print(dframe[['New cases', 'New deaths', 'New recovered']].corr())
print(dframe[['Confirmed', 'Active']].corr())

# Additional descriptive statistics for the entire dataframe
print(dframe.describe())

# Generate boxplots to check for outliers in the dataset
dframe.boxplot(column=['Deaths', 'Confirmed'])
plt.title("Boxplot for Deaths and Confirmed COVID Cases")
plt.show()

dframe.boxplot(column=['Confirmed', 'Recovered'])
plt.title("Boxplot for Recovered and Confirmed COVID Cases")
plt.show()

dframe.boxplot(column=['Confirmed', 'Deaths'])
plt.title("Boxplot for Active and Confirmed COVID Cases")
plt.show()

# Scatter plot to examine the relationship between confirmed cases and deaths
plt.scatter(dframe['Confirmed'], dframe['Deaths'])
plt.xlabel('Confirmed')
plt.ylabel('Deaths')
plt.title('Relationship between Confirmed Cases and Deaths')
plt.show()

# Scatter plot showing the relationship between Recovered and Confirmed cases
plt.scatter(dframe['Recovered'], dframe['Confirmed'])
plt.xlabel('Recovered')
plt.ylabel('Confirmed')
plt.title('Relationship between Recovered cases and Confirmed cases')
plt.show()

# Create a pairplot for new cases, new deaths, and new recovered to explore 2D projections
sns.pairplot(dframe[['New cases', 'New deaths', 'New recovered']])
plt.suptitle('Pairplot for 2D Projections of New cases, New deaths, and New recovered', y=1.02)
plt.show()

# Group data by WHO Region and calculate the sum of confirmed and active cases
grouped = dframe.groupby('WHO Region').agg({'Confirmed': 'sum', 'Active': 'sum'}).sort_values('Active', ascending=False)
print(grouped)

# Bar chart showing COVID-19 Deaths by Country using Plotly Express
fig_deaths = px.bar(dframe, x='Country/Region', y='Deaths', title='COVID-19 Deaths by Country')
fig_deaths.show()

# Bar chart showing COVID-19 Confirmed Cases by Country using Plotly Express
fig_confirmed = px.bar(dframe, x='Country/Region', y='Confirmed', title='COVID-19 Confirmed by Country')
fig_confirmed.show()

# Choropleth map showing COVID-19 Deaths by Country
fig_choropleth_deaths = px.choropleth(dframe, locations='Country/Region', locationmode='country names', color='Deaths',
                                      color_continuous_scale='viridis', title='COVID-19 Deaths by Country')
fig_choropleth_deaths.update_layout(geo=dict(showframe=False, projection_scale=40), coloraxis_colorbar=dict(title=''))
fig_choropleth_deaths.show()

# Choropleth map showing COVID-19 Confirmed Cases by Country
fig_choropleth_confirmed = px.choropleth(dframe, locations='Country/Region', locationmode='country names', color='Confirmed',
                                         color_continuous_scale='viridis', title='COVID-19 Confirmed cases by Country')
fig_choropleth_confirmed.update_layout(geo=dict(showframe=False, projection_scale=40), coloraxis_colorbar=dict(title=''))
fig_choropleth_confirmed.show()

# Line chart showing trends in deaths over days
fig_line_deaths = px.line(dframe, x=dframe.index, y=['Deaths'], labels={'value': 'Count', 'variable': 'Metric'},
                          title='Trends Deaths Over Days', line_shape='linear')
fig_line_deaths.update_layout(xaxis_title='Days', yaxis_title='Count')
fig_line_deaths.show()

# Display the correlation matrix using a heatmap
correlation_matrix = dframe[['Confirmed', 'Deaths']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Calculate and print total confirmed cases and deaths
total_confirmed_cases = dframe['Confirmed'].sum()
total_deaths = dframe['Deaths'].sum()
print('Total number of confirmed cases:', total_confirmed_cases)
print('Total number of deaths:', total_deaths)

# Calculation of the COVID-19 death rate
death_rate = (total_deaths / total_confirmed_cases) * 100
print('COVID-19 death rate:', f'{death_rate:.3f}%')


# Group data by country and calculate the sum of confirmed and deaths cases
grouped = dframe.groupby('Country/Region').agg({'Confirmed': 'sum', 'Deaths': 'sum'})
grouped = grouped.sort_values('Confirmed', ascending=False)
print(grouped)

# Prepare data for regression
X = dframe[['Confirmed']]
y = dframe['Deaths']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Set parameters for Random Forest regression
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

# Grid search to find best parameters
rf_model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_

# Train the model with the best parameters found
best_rf_model = RandomForestRegressor(**best_params, random_state=42)
best_rf_model.fit(X_train, y_train)
y_pred = best_rf_model.predict(X)

# Inflate predicted values
scaling_factor = 1.2
y_pred_inflated = y_pred * scaling_factor
y_pred_rounded_inflated = np.round(y_pred_inflated)

# Create DataFrame for actual and inflated predicted values
results_df_inflated_deaths = pd.DataFrame({'Actual': y, 'Inflated Rounded Predicted': y_pred_rounded_inflated})
print(results_df_inflated_deaths)

# Sum of actual and inflated predicted deaths
sum_actual_deaths = y.sum()
sum_inflated_predicted_deaths = y_pred_rounded_inflated.sum()
print(f'Sum of Actual Deaths: {sum_actual_deaths}')
print(f'Sum of Inflated Predicted Deaths: {sum_inflated_predicted_deaths}')

# Evaluate the model with inflated predicted values
mse_inflated_deaths = mean_squared_error(y, y_pred_inflated)
r2_inflated_deaths = r2_score(y, y_pred_inflated)
print(f'Mean Squared Error (Inflated Deaths): {mse_inflated_deaths}')
print(f'R-squared (Inflated Deaths): {r2_inflated_deaths}')

# Binary classification based on threshold
threshold = 5000
y_true_class = (y > threshold).astype(int)
y_pred_class = (y_pred_rounded_inflated > threshold).astype(int)
accuracy = accuracy_score(y_true_class, y_pred_class)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Plot actual deaths, inflated predicted deaths, and binary classification
plot_df = pd.DataFrame({'Actual Deaths': y, 'Inflated Predicted Deaths': y_pred_inflated, 'Binary Classification': y_pred_class})
plot_df = plot_df.sort_values(by='Actual Deaths')
fig, ax1 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=plot_df[['Actual Deaths', 'Inflated Predicted Deaths']], ax=ax1, marker='o')
ax2 = ax1.twinx()
sns.lineplot(data=plot_df[['Binary Classification']], ax=ax2, marker='o', color='r', linestyle='dashed')
ax1.set_xlabel('Observation Index')
ax1.set_ylabel('Deaths')
ax2.set_ylabel('Binary Classification', color='r')
plt.title('Actual Deaths, Inflated Predicted Deaths, and Binary Classification')
plt.show()

# Create visualizations with Plotly Express
fig_recovered = px.bar(dframe, x='Country/Region', y='Recovered', title='COVID-19 Recovered Cases by Country', color='Recovered', color_continuous_scale='Viridis')
fig_recovered.show()

fig_confirmed = px.bar(dframe, x='Country/Region', y='Confirmed', title='COVID-19 Confirmed by Country')
fig_confirmed.show()

fig_choropleth_recovered = px.choropleth(dframe, locations='Country/Region', locationmode='country names', color='Recovered', color_continuous_scale='Blues', title='COVID-19 Recovered cases by Country')
fig_choropleth_recovered.update_layout(geo=dict(showframe=False, projection_scale=40), coloraxis_colorbar=dict(title='Recovered'))
fig_choropleth_recovered.show()

fig_line_recovered = px.line(dframe, x=dframe.index, y=['Recovered'], labels={'value': 'Count', 'variable': 'Metric'}, title='Trends Recovered cases Over Days', line_shape='linear')
fig_line_recovered.update_layout(xaxis_title='Days', yaxis_title='Count')
fig_line_recovered.show()

# Correlation matrix
correlation_matrix = dframe[['Confirmed', 'Recovered']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Print the correlation matrix for all attributes
correlation_matrix_all = dframe.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix_all, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.show()

# Calculate and print total cases
total_new_cases = dframe['New cases'].sum()
print('Total New cases:', total_new_cases)
total_new_deaths = dframe['New deaths'].sum()
print('Total Recovered cases:', total_new_deaths)
total_new_recovered = dframe['New recovered'].sum()
print('Total confirmed cases:', total_new_recovered)

# Recovery rate calculation
recovery_rate = (total_new_recovered / total_new_cases) * 100
print(f'Recovery Rate: {recovery_rate:.2f}%')

# Random Forest regression to predict recoveries
X = dframe[['Confirmed']]
y = dframe['Recovered']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
param_grid = {'n_estimators': [50, 100, 150], 'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10], 'min_samples_leaf': [1, 2, 4]}
rf_model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_rf_model = RandomForestRegressor(**best_params, random_state=42)
best_rf_model.fit(X_train, y_train)
y_pred = best_rf_model.predict(X)

# Inflate and round predicted values
scaling_factor = 1.2
y_pred_inflated = y_pred * scaling_factor
y_pred_rounded_inflated = np.round(y_pred_inflated)
results_df_inflated_recovered = pd.DataFrame({'Actual': y, 'Inflated Rounded Predicted': y_pred_rounded_inflated})
print(results_df_inflated_recovered)

# Calculate sums and metrics
sum_actual_recovered = y.sum()
sum_inflated_predicted_recovered = y_pred_rounded_inflated.sum()
print(f'Sum of Actual Recovered: {sum_actual_recovered}')
print(f'Sum of Inflated Predicted Recovered: {sum_inflated_predicted_recovered}')
mse_inflated_recovered = mean_squared_error(y, y_pred_inflated)
r2_inflated_recovered = r2_score(y, y_pred_inflated)
print(f'Mean Squared Error (Inflated Recovered): {mse_inflated_recovered}')
print(f'R-squared (Inflated Recovered): {r2_inflated_recovered}')

# Binary classification based on a threshold
threshold_recovered = 5000
y_true_class_recovered = (y > threshold_recovered).astype(int)
y_pred_class_recovered = (y_pred_rounded_inflated > threshold_recovered).astype(int)
accuracy_recovered = accuracy_score(y_true_class_recovered, y_pred_class_recovered)
print(f'Accuracy (Recovered): {accuracy_recovered * 100:.2f}%')

# Load the dataset
dframe = pd.read_csv('country_wise_latest.csv')

# Create bar charts and choropleth maps using Plotly Express
fig_new_cases = px.bar(dframe, x='Country/Region', y='New cases', title='COVID-19 New Cases by Country')
fig_new_cases.show()

fig_new_deaths = px.bar(dframe, x='Country/Region', y='New deaths', title='COVID-19 New Deaths by Country')
fig_new_deaths.show()

fig_new_recovered = px.bar(dframe, x='Country/Region', y='New recovered', title='COVID-19 New Recovered by Country')
fig_new_recovered.show()

fig_choropleth_deaths = px.choropleth(dframe, locations='Country/Region', locationmode='country names', color='New deaths', color_continuous_scale='viridis', title='COVID-19 New Deaths by Country')
fig_choropleth_deaths.update_layout(geo=dict(showframe=False, projection_scale=40), coloraxis_colorbar=dict(title=''))
fig_choropleth_deaths.show()

# Create a line chart to observe trends
fig_trends = px.line(dframe, x=dframe.index, y=['New cases', 'New deaths', 'New recovered'], labels={'value': 'Count', 'variable': 'Metric'}, title='Trends in New Cases, Deaths, and Recoveries Over Days', line_shape='linear')
fig_trends.update_layout(xaxis_title='Days', yaxis_title='Count')
fig_trends.show()

# Visualize correlation matrix
correlation_matrix = dframe[['Confirmed', 'Recovered']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=dframe, x='Confirmed', y='Deaths', alpha=0.5)
plt.title('Relationship between Confirmed and Deaths')
plt.xlabel('Confirmed Cases')
plt.ylabel('Number of Deaths')
plt.show()

# Bar plot of New Deaths
plt.figure(figsize=(12, 6))
sns.countplot(data=dframe, x='New deaths')
plt.title('Number of New Deaths')
plt.xlabel('New deaths')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()


#To calculate  Sum of Predicted New Cases

# Correlation matrix visualization
correlation_matrix = dframe[['New cases', 'New deaths', 'New recovered']].corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Print sum of new cases, deaths, and recoveries
print(f"Sum of 'New cases': {dframe['New cases'].sum()}")
print(f"Sum of 'New deaths': {dframe['New deaths'].sum()}")
print(f"Sum of 'New recovered': {dframe['New recovered'].sum()}")

# Prepare data for regression
X = dframe[['Deaths', 'Recovered', 'Active', 'Confirmed']]
y = dframe['New cases']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Hyperparameter tuning and model training
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf_model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_rf_model = RandomForestRegressor(**best_params, random_state=42)
best_rf_model.fit(X_train, y_train)
y_pred = best_rf_model.predict(X)

# Create DataFrame for actual vs. predicted values and calculate statistics
results_df_rounded = pd.DataFrame({'Actual': y, 'Rounded Predicted': np.round(y_pred)})
print(results_df_rounded)
print(f'Sum of Actual New Cases: {y.sum()}')
print(f'Sum of Predicted New Cases: {np.round(y_pred).sum()}')

mse_test = mean_squared_error(y_test, best_rf_model.predict(X_test))
print(f'Mean Squared Error (Test Set): {mse_test}')

threshold_cases = 50
y_true_class = (y_test > threshold_cases).astype(int)
y_pred_class = (np.round(best_rf_model.predict(X_test)) > threshold_cases).astype(int)
accuracy_test = accuracy_score(y_true_class, y_pred_class)
print(f'Accuracy (Test Set): {accuracy_test * 100:.2f}%')

# Scatter plot for actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y, best_rf_model.predict(X), alpha=0.5)
plt.title("New Cases: Actual vs Predicted")
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.grid(True)
plt.show()


#To calculate Sum of Predicted New Deaths

# Define the variables for prediction
X = dframe[['Deaths', 'Recovered', 'Active', 'Confirmed']]
y_deaths = dframe['New deaths']

# Making predictions on the entire dataset for New Deaths
y_pred_deaths = best_rf_model.predict(X)
y_pred_rounded_deaths = np.round(y_pred_deaths)

# Evaluate the model for New Deaths
mse_deaths = mean_squared_error(y_deaths, y_pred_deaths)
mae_deaths = mean_absolute_error(y_deaths, y_pred_deaths)
r2_deaths = r2_score(y_deaths, y_pred_deaths)
print(f'Mean Squared Error (New Deaths): {mse_deaths}')
print(f'Mean Absolute Error (New Deaths): {mae_deaths}')
print(f'R-squared (New Deaths): {r2_deaths}')

# Create a DataFrame with actual, predicted, and rounded predicted values for New Deaths
results_df_deaths = pd.DataFrame({'Actual': y_deaths, 'Predicted': y_pred_deaths, 'Rounded Predicted': y_pred_rounded_deaths})
print(results_df_deaths)

# Calculate the sum of all actual, predicted, and rounded predicted new deaths
sum_actual_deaths = y_deaths.sum()
sum_predicted_deaths = y_pred_deaths.sum()
sum_rounded_predicted_deaths = y_pred_rounded_deaths.sum()
print(f'Sum of Actual New Deaths: {sum_actual_deaths}')
print(f'Sum of Predicted New Deaths: {sum_predicted_deaths}')
print(f'Sum of Rounded Predicted New Deaths: {sum_rounded_predicted_deaths}')

# Define a threshold for classifying deaths and calculate accuracy
threshold_deaths = 50
y_true_class_deaths = (y_deaths > threshold_deaths).astype(int)
y_pred_class_deaths = (y_pred_rounded_deaths > threshold_deaths).astype(int)
accuracy_deaths = accuracy_score(y_true_class_deaths, y_pred_class_deaths)
print(f'Accuracy (New Deaths): {accuracy_deaths * 100:.2f}%')

# Scaling features for another prediction task
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X_scaled, dframe['New recovered'], test_size=0.2, random_state=42)

# Creating a Random Forest regression model with hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf_model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_rf_model = RandomForestRegressor(**best_params, random_state=42)
best_rf_model.fit(X_train, y_train)

# Evaluate model performance function
def evaluate_model_performance(model, X, y, threshold=50):
    y_pred = model.predict(X)
    y_pred_rounded = np.round(y_pred)
    results_df = pd.DataFrame({'Actual': y, 'Rounded Predicted': y_pred_rounded})
    print(results_df)
    print(f'Sum of Actual: {y.sum()}')
    print(f'Sum of Predicted: {np.round(y_pred).sum()}')
    mse_test = mean_squared_error(y, y_pred)
    print(f'Mean Squared Error (Test Set): {mse_test}')
    y_true_class = (y > threshold).astype(int)
    y_pred_class = (y_pred_rounded > threshold).astype(int)
    accuracy_test = accuracy_score(y_true_class, y_pred_class)
    print(f'Accuracy (Test Set): {accuracy_test * 100:.2f}%')

# Call the function to evaluate the model
evaluate_model_performance(best_rf_model, X_test, y_test)


#To calculate sum of Predicted New Recovered Cases

# Load your DataFrame 'dframe' is assumed to be defined
X = dframe[['Deaths', 'Recovered', 'Active', 'Confirmed']]
y_recovered = dframe['New recovered']

# Feature scaling using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_recovered, test_size=0.2, random_state=42)

# Create and train the Random Forest regression model with hyperparameter tuning
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf_model = RandomForestRegressor(random_state=42)
grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error')
grid_search.fit(X_train, y_train)
best_params = grid_search.best_params_
best_rf_model = RandomForestRegressor(**best_params, random_state=42)
best_rf_model.fit(X_train, y_train)

# Define a function to evaluate model performance
def evaluate_model_performance(model, X, y, threshold=50):
    y_pred = model.predict(X)
    y_pred_rounded = np.round(y_pred)
    results_df = pd.DataFrame({'Actual': y, 'Rounded Predicted': y_pred_rounded})
    print(results_df)
    print(f'Sum of Actual: {y.sum()}')
    print(f'Sum of Predicted: {np.round(y_pred).sum()}')
    mse_test = mean_squared_error(y, y_pred)
    print(f'Mean Squared Error (Test Set): {mse_test}')
    y_true_class = (y > threshold).astype(int)
    y_pred_class = (y_pred_rounded > threshold).astype(int)
    accuracy_test = accuracy_score(y_true_class, y_pred_class)
    print(f'Accuracy (Test Set): {accuracy_test * 100:.2f}%')

# Evaluate the model's performance
evaluate_model_performance(best_rf_model, X_scaled, y_recovered)

# Function to plot actual vs predicted values
def plot_actual_vs_predicted(model, X, y, title="Actual vs Predicted"):
    y_pred = model.predict(X)
    plt.figure(figsize=(10, 6))
    plt.scatter(y, y_pred, alpha=0.5)
    plt.title(title)
    plt.xlabel("Actual Values")
    plt.ylabel("Predicted Values")
    plt.grid(True)
    plt.show()

# Plot for Recovered
plot_actual_vs_predicted(best_rf_model, X_scaled, y_recovered, title="Recovered: Actual vs Predicted")


# Define features and target
X = dframe[['Deaths', 'Recovered', 'Active', 'Confirmed']]
y = dframe['New recovered']

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Model training and hyperparameter tuning for Gradient Boosting
param_grid_gb = {
    'n_estimators': [50, 100, 150],
    'max_depth': [3, 5, 7],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
gb_model = GradientBoostingRegressor(random_state=42)
grid_search_gb = GridSearchCV(gb_model, param_grid_gb, cv=3, scoring='neg_mean_squared_error')
grid_search_gb.fit(X_train, y_train)
best_gb_model = GradientBoostingRegressor(**grid_search_gb.best_params_, random_state=42)
best_gb_model.fit(X_train, y_train)

# Evaluate model performance function
def evaluate_model_performance(model, X, y, X_test, y_test, threshold=50):
    y_pred = model.predict(X)
    y_pred_rounded = np.round(y_pred)
    results_df = pd.DataFrame({'Actual': y, 'Rounded Predicted': y_pred_rounded})
    print(results_df)
    print(f'Sum of Actual: {y.sum()}')
    print(f'Sum of Predicted: {np.round(y_pred).sum()}')
    y_test_pred = model.predict(X_test)
    y_test_pred_rounded = np.round(y_test_pred)
    mse_test = mean_squared_error(y_test, y_test_pred)
    print(f'Mean Squared Error (Test Set): {mse_test}')
    y_true_class = (y_test > threshold).astype(int)
    y_pred_class = (y_test_pred_rounded > threshold).astype(int)
    accuracy_test = accuracy_score(y_true_class, y_pred_class)
    print(f'Accuracy (Test Set): {accuracy_test * 100:.2f}%')

# Evaluate Gradient Boosting model
evaluate_model_performance(best_gb_model, X_scaled, y, X_test, y_test)

# XGBoost Model
param_grid_xgb = {
    'n_estimators': [50, 100, 150],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}
xgb_model = XGBRegressor(random_state=42)
grid_search_xgb = GridSearchCV(xgb_model, param_grid_xgb, cv=3, scoring='neg_mean_squared_error')
grid_search_xgb.fit(X_train, y_train)
best_xgb_model = XGBRegressor(**grid_search_xgb.best_params_, random_state=42)
best_xgb_model.fit(X_train, y_train)

# Evaluate XGBoost model
evaluate_model_performance(best_xgb_model, X_scaled, y, X_test, y_test)