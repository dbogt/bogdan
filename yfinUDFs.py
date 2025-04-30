from urllib.request import Request, urlopen  
import pandas as pd
import json
#import requests
import streamlit as st
from curl_cffi import requests
cookies = st.secrets['cookies']
crumb = st.secrets['crumb']

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
    'crumb': crumb,
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
    
    



def fnYFinJSONAll(stock): 
    urlData = "https://query2.finance.yahoo.com/v7/finance/quote?symbols="+stock 
    # response = requests.get(urlData, params=params, cookies=cookies, headers=headers)
    response = requests.get(urlData, params=params, cookies=dict(cookies), impersonate="chrome")
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


#%% Option chains
def grabExpDates(ticker):
    """
    Returns a dataframe of expiration dates available on Yahoo Finance.
    e.g.: https://query2.finance.yahoo.com/v7/finance/options/SPY
    
    """
    url = "https://query1.finance.yahoo.com/v7/finance/options/"+ticker+"?crumb=" + crumb
    #url = "https://query2.finance.yahoo.com/v7/finance/options/" + ticker
    #data = pd.read_json(url)
    
    # response = requests.get(url, params=params, cookies=cookies, headers=headers)
    response = requests.get(urlData, params=params, cookies=dict(cookies), impersonate="chrome")
    data = response.json()
    #st.write(data)

    expDatesUnix = data['optionChain']['result'][0]['expirationDates']
    expDatesNormal = pd.to_datetime(expDatesUnix, origin="unix",unit='s')
    df = pd.DataFrame(expDatesUnix,index=expDatesNormal,columns=["Unix Date"])
    return df

def optionChain(ticker='SPY', date='2022-11-18', calls_puts = 'calls'):
    """
    Scrapes option chain from Yahoo Fiance by converting date to unix code:
        https://query2.finance.yahoo.com/v7/finance/options/{ticker}?date={date}
        e.g.: https://query2.finance.yahoo.com/v7/finance/options/TSLA?date=1668729600
    
    Parameters
    ----------
    ticker : str, optional
        DESCRIPTION. The default is 'SPY'.
    date : str, optional
        DESCRIPTION. Maturity date of options. Enter in yyy-mm-dd format. The default is '2022-11-18'.
    calls_puts : str, optional
        DESCRIPTION. Enter 'calls' or 'puts'. The default is 'calls'.
    Returns
    -------
    dfOptions : DataFrame
        Returns calls or puts option chain.
    """
    url = "https://query2.finance.yahoo.com/v7/finance/options/{}?date={}"
    unixTS = pd.Timestamp('{} 00:00:00'.format(date)).timestamp()
    url = url.format(ticker, int(unixTS))

    # response = requests.get(url, params=params, cookies=cookies, headers=headers)
    response = requests.get(urlData, params=params, cookies=dict(cookies), impersonate="chrome")
    data = response.json()
    
    #data = pd.read_json(url)
    optionsData = data['optionChain']['result'][0]['options'][0]
    dfOptions = pd.DataFrame(optionsData[calls_puts])
    dfOptions['Exp'] = pd.to_datetime(dfOptions['expiration'],origin="unix",unit='s')
    return dfOptions
