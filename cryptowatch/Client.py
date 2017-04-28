
import requests
from urlparse import urljoin, parse_qsl, urlunparse, urlparse
import urllib

import cryptowatch.Msg as Msg

API_URL = 'https://api.cryptowat.ch/'



def _get_url(kwargs):
    return API_URL if not ('url' in kwargs) else kwargs['url']
    
def _raiseIfError(response):
    if(response.ok):
        return
    raise Msg.ApiRequestException(response)

def _get_response(url):
    resp = requests.get(url)
    _raiseIfError(resp)
    return resp.json()
    
def _include_allowance(res, json, kwargs):
    if('get_allowance' in kwargs and kwargs['get_allowance']):
        alw = Msg.Allowance(json)
        return (res, alw)
    else:
        return res
        
def _add_query_string(url, params):
    x = list(urlparse(url))
    q = dict(parse_qsl(x[4]))
    q.update(params)
    x[4] = urllib.urlencode(q)
    return urlunparse(x)
    
def GetAllowance(**kwargs):
    """Request the status of your current allowance"""
    url = _get_url(kwargs)
    resp = _get_response(url)
    
    res = Msg.Allowance(resp)
    return res
        
def GetMarkets(exchange = None, **kwargs):
    """
    Get a list of available exchanges and currency pairs
    """
    if(exchange):
        url = urljoin(_get_url(kwargs), "markets/")
        url = urljoin(url, exchange)
    else:
        url = urljoin(_get_url(kwargs), "markets")
    resp = _get_response(url)
    
    res = [Msg.Market(x) for x in resp['result']]
    return _include_allowance(res, resp, kwargs)

def GetAllPrices(split_slug = False, **kwargs):    
    """
    Get prices from all currency pairs on all exchanges.
    
    split_slug: Indicates whether the 'slug' should be split. By default, the result will
    return a dict() with concatenated exchange and currency pair names as the key, joined by
    a colon (e.g.  'coinbase:ethusd'). If this is set true, instead of a dict, the result 
    will be a list of 3-tuples containing the exchange, currency pair and price (in that order)
    """
    url = urljoin(_get_url(kwargs), "markets/prices")
    resp = _get_response(url)
    
    if(split_slug):
        res = []
        for slug in resp['result']:
            price = resp['result'][slug]
            exch,cpair = slug.split(":")
            res.append((exch, cpair, price))
    else:
        res = {x: resp['result'][x] for x in resp['result']}
    return _include_allowance(res, resp, kwargs)
    
    
def GetAllSummaries(split_slug = False, **kwargs):
    """
    Get summaries from all currency pairs on all exchanges.
    
    split_slug: Indicates whether the 'slug' should be split. By default, the result will
    return a dict() with concatenated exchange and currency pair names as the key, joined by
    a colon (e.g.  'coinbase:ethusd'). If this is set true, instead of a dict, the result 
    will be a list of 3-tuples containing the exchange, currency pair and summary (in that order)
    """
    url = urljoin(_get_url(kwargs), "markets/summaries")
    resp = _get_response(url)

    if(split_slug):
        res = []
        for slug in resp['result']:
            summ = Msg.Summary(resp['result'][slug])
            exch,cpair = slug.split(":")
            res.append((exch, cpair, summ))
    else:
        res = {x: Msg.Summary(resp['result'][x]) for x in resp['result']}
        
    return _include_allowance(res, resp, kwargs)


class MarketClient():
    def __init__(self, exchange, currencyPair, api_url=API_URL):
        """
        Initialize this MarketClient.
        
        exchange: The exchange on which the market exists
        currencyPair: The currency pair of interest for this client
        """
        self.api_url = api_url
        self.exchange = exchange
        self.currencyPair = currencyPair
        self.base_url = urljoin(self.api_url, "markets/%s/%s/" % (exchange, currencyPair))
        
    def GetPrice(self, **kwargs):
        """
        Get the most recent price on this market.
        """
        url = urljoin(self.base_url, "price")
        resp = _get_response(url)
        
        res = resp['result']['price']
        return _include_allowance(res, resp, kwargs)

            
        
    def GetSummary(self, **kwargs):
        """
        Get a 24-hour summary of this exchange.
        
        Result includes last, highest and lowest prices, volume, and price change information.
        """
        url = urljoin(self.base_url, "summary")
        resp = _get_response(url)
        
        res = Msg.Summary(resp['result'])
        return _include_allowance(res, resp, kwargs)
 
    
    def GetTrades(self, **kwargs):
        """
        Get a trade history.
        
        Keyword args:
        limit: Limit amount of trades returned. Defaults to 50. Integer
        since: Only return trades at or after this time. UNIX timestamp
        """
        url = urljoin(self.base_url, "trades")
        params = {}
        if('limit' in kwargs):
            params['limit'] = kwargs['limit']
        if('since' in kwargs):
            params['since'] = kwargs['since']
        
        url = _add_query_string(url, params)
        
        resp = _get_response(url)
        
        res = [Msg.Trade(x) for x in resp['result']]
        return _include_allowance(res, resp, kwargs)

            
    def GetOrderBook(self, **kwargs):
        """
        Get the current order book.
        """
        url = urljoin(self.base_url, "orderbook")
        params = {}
        url = _add_query_string(url, params)
        
        resp = _get_response(url)
        
        res = Msg.OrderBook(resp['result'])
        return _include_allowance(res, resp, kwargs)

            
    def GetOHLC(self, **kwargs):
        """
        Gets candlestick data with the Opening, High, Low and Closing values during specified time periods.
        
        Keyword args:
        before: Only return candles opening before this time. (UNIX Timestamp)
        after: Only return candles opening after this time. (UNIX Timestamp)
        periods: Only return these time periods. (Integer list)
        """
        url = urljoin(self.base_url, "ohlc")
        params = {}
        if('before' in kwargs):
            params['before'] = kwargs['before']
        if('after' in kwargs):
            params['after'] = kwargs['after']
        if('periods' in kwargs):
            params['periods'] = ",".join(kwargs['periods'])
        url = _add_query_string(url, params)
        
        resp = _get_response(url)
        
        res = {}
        for period in resp['result']:
            data = resp['result'][period]
            period_ms = int(period)*1000
            res[period] = [Msg.Candle(x, period_ms) for x in data]
        return _include_allowance(res, resp, kwargs)


































