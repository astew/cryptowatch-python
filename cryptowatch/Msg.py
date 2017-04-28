
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class ApiRequestException(Exception):
    def __init__(self, response):
        msg = "(%s) %s [%s]" % (response.status_code, response.reason, response.url)
        super(ApiRequestException, self).__init__(msg)
        
        self.response = response
        self.status_code = response.status_code
        self.reason = response.reason

            
class Allowance():
    PER_HOUR_ALLOWANCE = 4000000000

    def __init__(self, json):
        self.cost = json['allowance']['cost']
        self.remaining = json['allowance']['remaining']
        self.used = Allowance.PER_HOUR_ALLOWANCE - self.remaining
        
    def RemainingFraction(self):
        return float(self.remaining) / Allowance.PER_HOUR_ALLOWANCE
        
    def __str__(self):
        return "<Allowance> Cost: %d\tRemaining: %d" % (self.cost, self.remaining)
    def __repr__(self):
        return self.__str__()
        
class Market():
    def __init__(self, json):
        self.exchange = json['exchange']
        self.currencyPair = json['currencyPair']
        
    def __str__(self):
        return "<Market> %s: %s" % (self.exchange, self.currencyPair)
    def __repr__(self):
        return self.__str__()
        
        
class Summary():
    def __init__(self, json):
        self.last = json['price']['last']
        self.high = json['price']['high']
        self.low = json['price']['low']
        self.change_percentage = json['price']['change']['percentage']
        self.change_absolute = json['price']['change']['absolute']
        self.volume = json['volume']
        
    def __str__(self):
        return "<Summary> Last: %.2f\tHigh: %.2f\tLow: %.2f\tVol: %.2f" % (self.last, self.high, self.low, self.volume)
    def __repr__(self):
        return self.__str__()
        
class Trade():
    def __init__(self, json):
        self.id, self.timestamp, self.price, self.size = json
        
        
    def GetDateTime(self):
        return datetime.fromtimestamp(self.timestamp)
        
    def __str__(self):
        return "<Trade> (%s) %.2f @ %.2f" % (self.GetDateTime().strftime(DATE_FORMAT), self.size, self.price)
    def __repr__(self):
        return self.__str__()
        
class Order():
    def __init__(self, json):
        self.price, self.size = json
        
    def __str__(self):
        return "<Order> %.2f @ %.2f" % (self.size, self.price)
    def __repr__(self):
        return self.__str__()

class OrderBook():
    def __init__(self, json):
        self.asks = [Order(x) for x in json['asks']]
        self.bids = [Order(x) for x in json['bids']]
        
    def __str__(self):
        return "<OrderBook>"
    def __repr__(self):
        return self.__str__()


class Candle():
    def __init__(self, json, period_milliseconds):
        self.close_time, self.open, self.high, self.low, self.close, self.volume = json
        self.open_time = self.close_time - period_milliseconds
        
    def GetOpenDateTime(self):
        return datetime.fromtimestamp(self.open_time)
    def GetCloseDateTime(self):
        return datetime.fromtimestamp(self.close_time)
        
    def __str__(self):
        return "<Candle>%s | O:%.2f | H:%.2f | L:%.2f | C:%.2f | V:%.2f" % (self.GetOpenDateTime().strftime(DATE_FORMAT), self.open, self.high, self.low, self.close, self.volume)
    def __repr__(self):
        return self.__str__()



























