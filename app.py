import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
import plotly.offline as py
import os
import warnings
warnings.filterwarnings('ignore')
# Define the path to the data directory dynamically
data_dir = os.path.join(os.getcwd(), 'data')

# Load the datasets
global_temp_country = pd.read_csv(os.path.join(data_dir, 'GlobalLandTemperaturesByCountry.csv'))
global_temp = pd.read_csv(os.path.join(data_dir, 'GlobalTemperatures.csv'))

# Clean and filter data
global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
    ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands', 'United Kingdom', 'Africa', 'South America'])]
global_temp_country_clear = global_temp_country_clear.replace(
    ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
    ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

# Calculate average temperature for each country
countries = np.unique(global_temp_country_clear['Country'])
mean_temp = [global_temp_country_clear[global_temp_country_clear['Country'] == country]['AverageTemperature'].mean() for country in countries]

# Plotly choropleth world map
data = [dict(
    type='choropleth',
    locations=countries,
    z=mean_temp,
    locationmode='country names',
    text=countries,
    marker=dict(line=dict(color='rgb(0,0,0)', width=1)),
    colorbar=dict(tickprefix='', title='# Average\nTemperature,\n°C')
)]
layout = dict(
    title='Average land temperature in countries',
    geo=dict(
        showframe=False,
        showocean=True,
        oceancolor='rgb(0,255,255)',
        projection=dict(type='orthographic', rotation=dict(lon=60, lat=10)),
        lonaxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)'),
        lataxis=dict(showgrid=True, gridcolor='rgb(102, 102, 102)')
    )
)
fig = go.Figure(data=data, layout=layout)

# Display Plotly map in Streamlit
st.plotly_chart(fig)

# Seaborn bar plot for average temperature by country
f, ax = plt.subplots(figsize=(4.5, 50))
colors_cw = sns.color_palette('coolwarm', len(countries))
sns.barplot(x=mean_temp, y=countries, palette=colors_cw[::-1], ax=ax)
ax.set(xlabel='Average temperature', title='Average land temperature in countries')

# Display Matplotlib bar plot in Streamlit
st.pyplot(f)

# Processing global temperature data for time series
years = np.unique(global_temp['dt'].apply(lambda x: x[:4]))
mean_temp_world = [global_temp[global_temp['dt'].apply(lambda x: x[:4]) == year]['LandAverageTemperature'].mean() for year in years]
mean_temp_world_uncertainty = [global_temp[global_temp['dt'].apply(lambda x: x[:4]) == year]['LandAverageTemperatureUncertainty'].mean() for year in years]

# Plotly line plot for global temperature with uncertainty
trace0 = go.Scatter(x=years, y=np.array(mean_temp_world) + np.array(mean_temp_world_uncertainty), fill=None, mode='lines', name='Uncertainty top', line=dict(color='rgb(0, 255, 255)'))
trace1 = go.Scatter(x=years, y=np.array(mean_temp_world) - np.array(mean_temp_world_uncertainty), fill='tonexty', mode='lines', name='Uncertainty bot', line=dict(color='rgb(0, 255, 255)'))
trace2 = go.Scatter(x=years, y=mean_temp_world, name='Average Temperature', line=dict(color='rgb(199, 121, 093)'))

data = [trace0, trace1, trace2]
layout = go.Layout(xaxis=dict(title='Year'), yaxis=dict(title='Average Temperature, °C'), title='Average land temperature in the world', showlegend=False)
fig = go.Figure(data=data, layout=layout)

# Display Plotly line plot in Streamlit
st.plotly_chart(fig)

# Compare temperatures over time for specific continents/countries
continent = ['Russia', 'United States', 'Niger', 'Greenland', 'Australia', 'Bolivia']
mean_temp_year_country = [[0] * len(years[70:]) for i in range(len(continent))]

j = 0
for country in continent:
    all_temp_country = global_temp_country_clear[global_temp_country_clear['Country'] == country]
    i = 0
    for year in years[70:]:
        mean_temp_year_country[j][i] = all_temp_country[all_temp_country['dt'].apply(lambda x: x[:4]) == year]['AverageTemperature'].mean()
        i += 1
    j += 1

traces = []
colors = ['rgb(0, 255, 255)', 'rgb(255, 0, 255)', 'rgb(0, 0, 0)', 'rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']
for i in range(len(continent)):
    traces.append(go.Scatter(x=years[70:], y=mean_temp_year_country[i], mode='lines', name=continent[i], line=dict(color=colors[i])))

layout = go.Layout(xaxis=dict(title='Year'), yaxis=dict(title='Average Temperature, °C'), title='Average land temperature on the continents')
fig = go.Figure(data=traces, layout=layout)

# Display Plotly line plot for continents in Streamlit
st.plotly_chart(fig)

# streamlit run /Users/ronitvyas/Documents/GitHub/CloudDeploymentProject/app2.py
