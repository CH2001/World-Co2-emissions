import streamlit as st

import numpy as np
import pandas as pd
import time
import plotly
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

st.header("Co2/ Greenhouse gas emission analysis")

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

# readme = st.checkbox("readme first")

# if readme:

#     st.write("""
#         This is a web app demo using [streamlit](https://streamlit.io/) library. It is hosted on [heroku](https://www.heroku.com/). You may get the codes via [github](https://github.com/richieyuyongpoh/myfirstapp)
#         """)

#     st.write ("For more info, please contact:")

#     st.write("<a href='https://www.linkedin.com/in/yong-poh-yu/'>Dr. Yong Poh Yu </a>", unsafe_allow_html=True)

option = st.sidebar.selectbox(
    'Select a mini project',
     ['line chart','map','T n C','Long Process'])


if option=='line chart':
    # Line plot for change in co2 emission 
    fig = px.line(df_asean,
                  x="year",
                  y="co2",
                  hover_name = 'country',
                  hover_data=['country','population'],
                  color='country')

    fig.update_layout(title="Change in CO₂ Emission in ASEAN region for the last 10 years: 2012-2021")

    fig.show()
    st.plotly_chart(fig, use_container_width=True)  
#st.line_chart(chart_data)

elif option=='map':
    map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

    st.map(map_data)

elif option=='T n C':

    st.write('Before you continue, please read the [terms and conditions](https://www.gnu.org/licenses/gpl-3.0.en.html)')
    show = st.checkbox('I agree the terms and conditions')
    if show:
        st.write(pd.DataFrame({
        'Intplan': ['yes', 'yes', 'yes', 'no'],
        'Churn Status': [0, 0, 0, 1]
        }))


else:
    'Starting a long computation...'

    
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
   
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    '...and now we\'re done!'
