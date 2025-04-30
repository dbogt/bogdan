import streamlit as st
import yfinUDFs as yf
import pandas as pd
import requests


cookies = st.secrets['cookies']
#st.write(cookies)

headers = {
    'authority': 'query2.finance.yahoo.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'origin': 'https://finance.yahoo.com',
    'referer': 'https://finance.yahoo.com/quote/AAPL?p=AAPL&.tsrc=fin-srch',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

params = {
    'lang': 'en-US',
    'region': 'US',
    'corsDomain': 'finance.yahoo.com',
}

def fnYFinJSONAll(stock): 
    urlData = "https://query2.finance.yahoo.com/v6/finance/quote?symbols="+stock
    #st.write("Running", stock)
    try:
        response = requests.get(urlData, params=params, cookies=cookies, headers=headers)
        data = response.json()
        df = pd.DataFrame(data)
        #         df = pd.read_json(urlData)
    except:
        print("Couldn't find", stock)
        df = pd.DataFrame({'symbol':[stock],'shortName':['n.a.']})
        df.set_index('symbol', inplace=True)
        return df
    
    df = pd.DataFrame(df.iloc[1][0]) 

    try: 
        df.set_index('symbol', inplace=True)
    except:
        df = pd.DataFrame({'symbol':[stock],'shortName':['n.a.']})
        df.set_index('symbol', inplace=True)
    return df


ticker = st.text_input("Enter a ticker")
st.write("https://query1.finance.yahoo.com/v1/test/getcrumb")
crumb = st.text_input("enter your crumb")
crumbDynamic = requests.get('https://query1.finance.yahoo.com/v1/test/getcrumb', params=params, cookies=cookies, headers=headers)
st.write(crumbDynamic.text)
urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols="+ticker
st.write(urlData + "&crumb=" + crumb)
params['crumb'] = st.secrets['crumb']
response = requests.get(urlData, params=params, cookies=cookies, headers=headers)
data = response.json()
st.write(data)
df2 = pd.DataFrame(data['quoteResponse']['result'])
df2.set_index('symbol',inplace=True)
st.write(df2)

#df = fnYFinJSONAll(ticker)
#st.write(df)
