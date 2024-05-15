import plotly.express as px
import pandas as pd
import streamlit as st

#%% Streamlit Controls
st.set_page_config(layout="wide",page_title='Options Calculator',
menu_items={
        "About": f"CPI - Inflation Data"
        f"\nApp contact: [Bogdan Tudose](mailto:bogdan.tudose@marqueegroup.ca)",
    })

#%% App Details
appDetails = """
Created by: [Bogdan Tudose](https://www.linkedin.com/in/tudosebogdan/) \n
Date: May 15, 2024 \n
Purpose: Compare different CPI indicators in Canada and US.
Source: https://www.bankofcanada.ca/rates/price-indexes/cpi/
"""
with st.expander("See app info"):
    st.write(appDetails)

@st.cache
def grab_cpi():
  url = 'https://www.bankofcanada.ca/rates/price-indexes/cpi/'
  df = pd.read_html(url)[0]
  properCols = [x[-2] for x in df.columns]
  codes = [x[-1] for x in df.columns]  
  df.columns = properCols
  df['Month'] = pd.to_datetime(df['Month'])
  df.set_index('Month',inplace=True) 
  filterDF = df.iloc[:, 2:]
  df = pd.melt(filterDF, var_name='CPI Metric',value_vars=filterDF.columns, ignore_index=False)
  return filterDF, df

df, melt = grab_cpi()
fig = px.line(melt, y='value', color='CPI Metric',
              labels={
                     "value": "Inflation (%)"},
              title='CPI Indicators (Source:Bank of Canada)')

st.plotly_chart(fig, use_container_width=True)
df.index = df.index.date
st.write(df)
#st.dataframe(df,column_config={"Month":st.column_config.DateColumn()})
