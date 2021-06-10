import pandas as pd


class YahooClient:
    BASE_URI = 'https://query1.finance.yahoo.com/v7/finance/download/'

    def get_time_series(self, etfs):
        result = dict()
        for etf in etfs:
            try:
                df = pd.read_csv(YahooClient.BASE_URI + etf)
                result[etf] = {
                    'meta': {
                        'symbol': etf,
                        'currency': 'USD'
                    },
                    'values': [
                        {
                            "open": df.iloc[0]['Open'],
                            "high": df.iloc[0]['High'],
                            "low": df.iloc[0]['Low'],
                            "close": df.iloc[0]['Close'],
                            "volume":df.iloc[0]['Volume']
                        }
                    ]
                }
            except:
                result[etf] = {
                    "code": 400,
                    'message': '%s symbol not found!' % (etf,)
                }
        return result