from urllib.request import Request, urlopen  
import pandas as pd
import json
#import requests
import streamlit as st
from curl_cffi import requests
cookies = st.secrets['cookies']
crumb = st.secrets['crumb']

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    # 'cookie': 'tbla_id=e24ed925-5d8b-4e39-aa86-0e3ff4b64013-tuct9603ce7; OTH=v=2&s=0&d=eyJraWQiOiIwIiwiYWxnIjoiUlMyNTYifQ.eyJjdSI6eyJndWlkIjoiQ1BWUVBXMjMzQlpSTTZDVEdHVTdNUVdUQlUiLCJwZXJzaXN0ZW50Ijp0cnVlLCJzaWQiOiJLaUJIcTdWekVOMGcifX0.VV82Rl35i2wmyaPEQPQZ0kNDI4JPu6Sf_6YPTSgGJNRoh-boavq1T2hete4J4nMvp4grlUQ2eGK11fuiydZ0K9h6kBu8ANEWM16ghcoeV6zxr5enZNMzlbnLOLuD7M36-JsNuqc2FiSGQlJ4N7BniZAJNZHCidVI48VJaANvg2A; OTHD=g=CCD9AC87A490DAEDF04CD0471B4935AAC7966E86CDC91AEF20FCD6D621AFF054&s=A95464835FDF1140C822507EDC1D2FA77950930C58E31D5C3E38D0CF8DCC9459&b=bid-ef719d9h4468q&j=us&bd=b280de554b72cc19ebd508f5a24f7015&gk=x1a9z-qJCjBBcc&sk=x1a9z-qJCjBBcc&bk=x1a9z-qJCjBBcc&iv=DDFB91B2537D8AF8FC512FA26A64BC3A&v=1&u=0; F=d=HFFTVhg9vIsF34HO.6kIkwZQy5PkljFrIUPujhV5mJ2LjXZ4ELUAcpQb0huM; T=af=QkNBQkJBJnRzPTE3NDExODk4MTMmcHM9MlNFanVkaWh0Z0dJRDZtbEVYblhQdy0t&d=bnMBeWFob28BZwFDUFZRUFcyMzNCWlJNNkNUR0dVN01RV1RCVQFhYwFBSGVZdEQ1WQFhbAFib2dkYW4uYS50dWRvc2VAZ21haWwuY29tAXNjAWRlc2t0b3Bfd2ViAWZzAVNSeXplU3hueUhLMQF6egExS0h5bkJBN0UBYQFRQUUBbGF0ATFLSHluQgFudQEw&kt=EAAZ5_X31Jyo8xK6gFn4ESadA--~I&ku=FAAQnAFlRrC8p2VaxgDXh2r1DMtPpGCsu4tvSaXsqJgfMlpBTu8hqSBcvzLKjF1pMZnG7h8vpos3eiUuHglzPJGJ4NFYJHXbQn0CFczKSdz2EJ6S7fzLo2Md0mTntzLvDbaFx4MpJT3_IjgKZtI8rjEhn0zyWRIRd_YY9aSzb14S3E-~E; PH=l=en; Y=v=1&n=5m66vf1rviedo&l=4twp6kwk8nj8bwgxft0cfe1f4e5hgkd51ms9208w/o&p=02q000000000000&r=108&intl=us; ucs=tr=1744836975000; axids=gam=y-PD35SO9G2uJHdPLGJV4odbcXROIv4XMKFv.F7V5CQlbWTtz4LQ---A&dv360=eS1CXy5uZFdSRTJ1RkNiTVF4RmZZZGh2RTZVQWZtX3ZmbnlsUEJoRTNHUmtrc3NXeUR3SjFRMW51RmRERmtCZ3oybkl5Tn5B&ydsp=y-ZaSGzYZE2uKrXkRZ75hoMG90WPznnV.gviaLfzCncGQb83aYBIfC_B6aEmvhQE_XAJNA~A&tbla=y-cUrbgFFG2uICBD4NdaBCZ1_EIWERf8UPs09qi0DlED7jRUnrOA---A; GUC=AQEBCAFob_FonUIatAO5&s=AQAAAE62VFfZ&g=aG6oFA; A1=d=AQABBBoZQmICENQNaRY6sf9IVmEquGopnOcFEgEBCAHxb2idaCXaxyMA_eMDAAcIGhlCYmopnOcIDy1w9X8iOVkO1X1OIuh7jgkBBwoBMw&S=AQAAAiXXoutQvRD05r3WBVQLlqU; A3=d=AQABBBoZQmICENQNaRY6sf9IVmEquGopnOcFEgEBCAHxb2idaCXaxyMA_eMDAAcIGhlCYmopnOcIDy1w9X8iOVkO1X1OIuh7jgkBBwoBMw&S=AQAAAiXXoutQvRD05r3WBVQLlqU; PRF=t%3D%255EGSPC%252BQQQ%252BNPO%252BIIP-UN.TO%252BCHR.TO%252BCPH.TO%252BSMCI%252BSPY%252BIGV%252BVICI%252BEPR-PC%252BBHM%252BDDS%252BDNTL.TO%252BVAW%26newChartbetateaser%3D1%26theme%3Dauto%26ft%3DthemeSwitchEducation%26dock-collapsed%3Dtrue; cmp=t=1752147296&j=0&u=1---; A1S=d=AQABBBoZQmICENQNaRY6sf9IVmEquGopnOcFEgEBCAHxb2idaCXaxyMA_eMDAAcIGhlCYmopnOcIDy1w9X8iOVkO1X1OIuh7jgkBBwoBMw&S=AQAAAiXXoutQvRD05r3WBVQLlqU; ySID=v=1&d=8nBd.Ap_NQ--',
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
    response = requests.get(url, params=params, cookies=dict(cookies), impersonate="chrome")
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
    response = requests.get(url, params=params, cookies=dict(cookies), impersonate="chrome")
    data = response.json()
    
    #data = pd.read_json(url)
    optionsData = data['optionChain']['result'][0]['options'][0]
    dfOptions = pd.DataFrame(optionsData[calls_puts])
    dfOptions['Exp'] = pd.to_datetime(dfOptions['expiration'],origin="unix",unit='s')
    return dfOptions
