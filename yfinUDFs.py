from urllib.request import Request, urlopen  
import pandas as pd
import json
import requests
import streamlit as st

cookies = st.secrets['cookies']

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
    'crumb': 'aQXXlwvY/Hw',
    'lang': 'en-US',
    'region': 'US',
    'corsDomain': 'finance.yahoo.com',
}

def fnYFinJSON(stock, field):
    df = fnYFinJSONAll(stock)
    if field in df.columns:
        return df.iloc[0][field]
    else:
        return "N/A"
    
    


def fnYFinJSONOLD(stock, field):
    if not stock:
        return "enter a ticker"
    else:
    	urlData = "https://query2.finance.yahoo.com/v6/finance/quote?symbols="+stock
    	webUrl = urlopen(urlData)
    	if (webUrl.getcode() == 200):
    		data = webUrl.read()
    	else:
    	    print ("Received an error from server, cannot retrieve results " + str(webUrl.getcode()))
    	yFinJSON = json.loads(data)
        
    try:
        tickerData = yFinJSON["quoteResponse"]["result"][0]
    except:
        return "N/A"
    if field in tickerData:
        return tickerData[field]
    else:
        return "N/A"

def fnYFinJSONAll(stock): 
    urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols="+stock 
    response = requests.get(urlData, params=params, cookies=cookies, headers=headers)
    #st.write("Running", stock)
    try:
        data = response.json()
        df = pd.DataFrame(data['quoteResponse']['result'])

#         df = pd.read_json(urlData)
    except:
        print("Couldn't find", stock)
        df = pd.DataFrame({'symbol':[stock],'shortName':['n.a.']})
        df.set_index('symbol', inplace=True)
        return df


    try: 
        df.set_index('symbol', inplace=True)
    except:
        df = pd.DataFrame({'symbol':[stock],'shortName':['n.a.']})
        df.set_index('symbol', inplace=True)
    return df
