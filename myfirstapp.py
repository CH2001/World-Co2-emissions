import streamlit as st

import numpy as np
import pandas as pd
import time
import plotly
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.header("ASEAN Co2/ Greenhouse gas emission analysis")

# Read dataset 
df_co2 = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')

# Subset data last 10 years data available: 2011-2021
df_10yrs = df_co2[df_co2['year'] > 2011]

# Subset ASEAN countries only 
asean = ['Thailand', 'Vietnam', 'Cambodia', 'Singapore', 'Laos', 'Indonesia', 'Myanmar', 'Malaysia', 'Brunei', 'Philippines', 'Timor']
df_asean = df_10yrs[df_10yrs.country.isin(asean)] 
df_asean.head(5)

def drop_missing(df_col): 
    for col in df_col.columns:
        cols_to_drop = []
        
        # Append column names to cols_to_drop if number of unique values under a column is less than 1
        if df_col[col].nunique() <= 1: 
            cols_to_drop.append(col)

        # Calculate the percentage of missing values 
        missing_percent = df_col[col].isna().mean() * 100 

        # If the percentage of missing value is more than 30 
        if missing_percent > 40: 
            cols_to_drop.append(col)
        
    print(f'Cols with high number of missing values (missing value >30) {cols_to_drop}')
    
    return(df_col)

df_asean_cleaned = drop_missing(df_asean)

option = st.sidebar.selectbox(
    'Select a plot',
     ['Worldwide', 'ASEAN','map','T n C','Long Process'])


if option=='ASEAN':
    
    # Plot the choropleth map figure
    # Total emission in the last 10 years 2012-2021
    df_asean_total = df_asean.groupby(["country", "iso_code"])["co2"].sum().to_frame().reset_index()

    # Plot the choropleth map figure
    fig1 = px.choropleth(df_asean_total,
                        locations="iso_code", 
                        locationmode='ISO-3',
                        color="co2", 
                        hover_name="country", 
                        hover_data=['country', 'co2'],
                        color_continuous_scale="thermal", 
                        scope="asia")

    fig1.update_layout(title="Total CO2 Emission in each ASEAN countries from 2012-2021")

    fig1.show()
    st.plotly_chart(fig1, use_container_width=True)  
    
    st.text(" ")    
    # ASEAN countries emission ranking in the last 10 years 2012-2021
    df_asean_total_sorted = df_asean_total.sort_values('co2', ascending = False)

    fig2 = px.bar(df_asean_total_sorted,
                  x = 'country',
                  y = 'co2',
                  color='co2',
                  hover_name = 'country',
                  hover_data = ['co2'],
                  color_continuous_scale = 'thermal')


    fig2.update_layout(title="CO2 Emission: ASEAN countries rankings")

    fig2.show()
    st.plotly_chart(fig2, use_container_width=True)      

    st.text(" ")
    # Line plot for change in co2 emission 
    fig3 = px.line(df_asean,
                  x="year",
                  y="co2",
                  hover_name = 'country',
                  hover_data=['country','population'],
                  color='country')

    fig3.update_layout(title="Change in CO₂ Emission in ASEAN region for the last 10 years: 2012-2021")
    fig3.show()
    st.plotly_chart(fig3, use_container_width=True)  

    
    st.text(" ")
    # Line plot for co2 emission in each ASEAN countries
    fig4 = px.area(df_asean,
                  x="year",
                  y="co2",
                  color="country",
                  facet_col="country",
                  facet_col_wrap=5,
                  height=350)

    fig4.update_layout(title="CO₂ Emission in each ASEAN countries for the last 10 years: 2012-2021")

    fig4.show()
    st.plotly_chart(fig4, use_container_width=True)  
    
    st.text(" ")    
    # ASEAN countries Co2 indicators 
    df_asean_melt = pd.melt(df_asean.groupby(["country"])[["coal_co2", "oil_co2", "flaring_co2", "cement_co2", "gas_co2"]].sum().reset_index(), id_vars=['country'])

    fig5 = px.line_polar(df_asean_melt, 
                         r="value", 
                         theta="variable", 
                         color="country", 
                         line_close=True, 
                         width=1000, 
                         height=500)

    fig5.update_layout(title="CO2 Emission: ASEAN countries rankings")

    fig5.show()
    st.plotly_chart(fig5, use_container_width=True) 
    
else:
    'Starting a long computation...'

    
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
   
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'
