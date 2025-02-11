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
    # 'cookie': 'B=2hc15i1h3p44f&b=3&s=dj; A1=d=AQABBI-QPGICEPhghfRgPzYi2nCIbpAlsCgFEgEBCAGoNWRlZCUHb2UB_eMBAAcIj5A8YpAlsCg&S=AQAAAuZpWil7Nsv74jTOjnvSnng; A3=d=AQABBI-QPGICEPhghfRgPzYi2nCIbpAlsCgFEgEBCAGoNWRlZCUHb2UB_eMBAAcIj5A8YpAlsCg&S=AQAAAuZpWil7Nsv74jTOjnvSnng; GUC=AQEBCAFkNahkZUIatwPX; A1S=d=AQABBI-QPGICEPhghfRgPzYi2nCIbpAlsCgFEgEBCAGoNWRlZCUHb2UB_eMBAAcIj5A8YpAlsCg&S=AQAAAuZpWil7Nsv74jTOjnvSnng&j=WORLD; cmp=t=1681950149&j=0&u=1---; PRF=t%3DAAPL%252B%255EGSPC%252B%255EGSPTSE%252BCAD%253DX%252BTSLA%252BCBA.AX%252BDDS%252BBHP.AX%252BENEL.MI%252BAMZN%252BNFLX%252B%255EIXIC%252BCGX.TO%252BES%253DF%252BACN%26newChartbetateaser%3D1',
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
    'crumb': st.secrets['crumb'],
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
