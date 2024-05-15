import plotly.express as px
import pandas as pd
import streamlit as st
import requests

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
  filterDF.index = filterDF.index.date
  df = pd.melt(filterDF, var_name='CPI Metric',value_vars=filterDF.columns, ignore_index=False)
  filterDF['MoM'] = filterDF['Total CPI'] - filterDF['Total CPI'].shift(-1)
  return filterDF, df

token = st.secrets['fredKEY']
@st.cache
def grab_fred_cpi():
  rootURL = 'https://api.stlouisfed.org/fred/series/observations?series_id='
  seriesID = 'CWSR0000SA0'
  apiKey = '&api_key=' + token #please change this to your API KEY
  fileType = '&file_type=json'
  freq = '&frequency=m' #change d to m, y, etc.
  units = '&units=pc1' #pc1=percent change year ago
  url= rootURL + seriesID + apiKey + fileType + freq + units

  req = requests.get(url)
  data = req.json()
  df = pd.DataFrame(data['observations'])
  df =df[ df['value']!='.' ]
  df['date'] = pd.to_datetime(df['date'])
  df['value'] = pd.to_numeric(df['value'])
  df.sort_values('date',ascending=False,inplace=True)
  df = df[['date','value']]   
  df['MoM'] = df['value'] - df['value'].shift(-1)
  return df


df, melt = grab_cpi()
dfUS = grab_fred_cpi()

fig = px.line(melt, y='value', color='CPI Metric',
              labels={
                     "value": "Inflation (%)", "index":'Date'},
              title='Canada CPI Indicators (Source: Bank of Canada)')
figUS = px.line(dfUS, x='date', y='value',
              labels={"date": "Date",'value':'Inflation (%)'},
              title='US CPI (Source: FRED)')


lastCanadaCPI = df.iloc[0]['Total CPI'] / 100
lastCanadaDate = df.index[0]
lastUSCPI = dfUS.iloc[0]['value'] / 100
lastUSDate = dfUS.iloc[0]['date']
deltaCanada = df.iloc[0]['MoM'] / 100
deltaUS = dfUS.iloc[0]['MoM'] / 100
output = "{:,.2%}"


st.title("CPI Data - Canada vs US")
col1, col2 = st.columns(2)
with col1:
    st.metric(f"Canada CPI ({lastCanadaDate:%Y-%m})", output.format(lastCanadaCPI), delta=output.format(deltaCanada))
with col2:
    st.metric(f"US CPI ({lastUSDate:%Y-%m})", output.format(lastUSCPI), delta=output.format(deltaUS))
col1, col2 = st.columns(2)


st.plotly_chart(fig, use_container_width=True)
st.plotly_chart(figUS, use_container_width=True)

st.title('Canada CPI Data (Source: BoC)')
st.dataframe(df)
st.title('US CPI Data (Source: FRED)')
st.write("Source: https://fred.stlouisfed.org/series/CWSR0000SA0#0")
st.dataframe(dfUS)
#st.dataframe(df,column_config={"Month":st.column_config.DateColumn()})
