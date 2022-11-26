import streamlit as st

import numpy as np
import pandas as pd
import time
import plotly
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns 

st.header("ASEAN Co2/ Greenhouse gas emission analysis")

# Read dataset 
df_co2 = pd.read_csv('https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv')

# Subset data last 10 years data available: 2011-2021
df_10yrs = df_co2[df_co2['year'] > 2011]

option = st.sidebar.selectbox(
    'Select a plot',
     ['Worldwide', 'ASEAN'])


if option=='ASEAN':
    # Subset ASEAN countries only 
    asean = ['Thailand', 'Vietnam', 'Cambodia', 'Singapore', 'Laos', 'Indonesia', 'Myanmar', 'Malaysia', 'Brunei', 'Philippines', 'Timor']
    df_asean = df_10yrs[df_10yrs.country.isin(asean)] 
    
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

    fig1.update_layout(title="Total CO2/ green house gas emission in each ASEAN countries from 2012-2021")

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


    fig2.update_layout(title="CO2/ green house gas emission: ASEAN countries rankings")

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

    fig3.update_layout(title="Change in CO2/ green house gas emission in ASEAN region for the last 10 years: 2012-2021")
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

    fig4.update_layout(title="CO2/ green house gas emission in each ASEAN countries for the last 10 years: 2012-2021")

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

    fig5.update_layout(title="CO2/ green house gas emission: ASEAN countries rankings")

    fig5.show()
    st.plotly_chart(fig5, use_container_width=True) 
    
    df_asean_melt = df_asean.groupby(["country"])[["coal_co2", "oil_co2", "flaring_co2", "cement_co2", "gas_co2"]].sum().reset_index()
    st.dataframe(data=df_asean_melt)
    
else:
    # Keep countries only 
    continents = ['Asia', 'Central America', 'South America', 'North America', 'Africa', 'Europe', 'International transport', 'South America', 'Oceania', 'European Union (27)', 'European Union (28)']
    df_co2_clean = df_10yrs[df_10yrs["country"].str.contains("(GCP)")==False]
    df_co2_clean1 = df_co2_clean[df_co2_clean["country"].str.contains("excl.")==False]
    df_co2_clean2 = df_co2_clean1[df_co2_clean["country"].str.contains("income")==False]
    df_co2_clean3 = df_co2_clean2[df_co2_clean["country"].str.contains("World")==False]
    df_co2_clean4 = df_co2_clean3[~df_co2_clean3.country.isin(continents)]
    
    st.text(" ") 
    # Total emission in the last 10 years 2012-2021
    df_co2_total = df_co2_clean4.groupby(["country", "iso_code"])["co2"].sum().to_frame().reset_index()

    # Plot the choropleth map figure
    fig6 = px.choropleth(df_co2_total,
                        locations="iso_code", 
                        locationmode='ISO-3',
                        color="co2", 
                        hover_name="country", 
                        hover_data=['country', 'co2'],
                        color_continuous_scale="thermal")

    fig6.update_layout(title="Total CO2/ green house gas emission in the world from 2012-2021")

    fig6.show()
    st.plotly_chart(fig6, use_container_width=True)
    
    df_total_sorted = df_co2_total.sort_values('co2', ascending = False)
    df_total_sorted_top10 = df_total_sorted.nlargest(15, 'co2')
    
    st.text(" ")  
    # Plot the bar figure
    fig7 = px.bar(df_total_sorted_top10,
                  x = 'country',
                  y = 'co2',
                  color='co2',
                  hover_name = 'country',
                  hover_data = ['co2'],
                  color_continuous_scale = "thermal",
                  height=500)

    fig7.update_layout(title="Top 15 countries with the highest CO2/ green house gas emission the last 10 years: 2012-2021")

    fig7.show()
    st.plotly_chart(fig7, use_container_width=True) 
    
    
    df_total_sorted_bottom10 = df_total_sorted.nsmallest(15, 'co2')

    # Plot the bar figure
    fig8 = px.bar(df_total_sorted_bottom10,
                  x = 'country',
                  y = 'co2',
                  color='co2',
                  hover_name = 'country',
                  hover_data = ['co2'],
                  color_continuous_scale = "thermal",
                  height=500)

    fig8.update_layout(title="Countries with the lowest CO2/ green house gas emission the last 10 years: 2012-2021")

    fig8.show()
    st.plotly_chart(fig8, use_container_width=True) 
