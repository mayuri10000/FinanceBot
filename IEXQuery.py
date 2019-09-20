import datetime

try:
    # Import the necessary things, otherwise throw an error and exit
    from iexfinance.stocks import Stock
    from iexfinance.refdata import get_symbols
    from iexfinance.base import IEXQueryError
    from iexfinance.stocks import get_historical_data
except ImportError:
    print("Oops! This program requires iexfinance but it's not installed on your system!")
    exit(-1)

# The api key of IEX finance APIs, can only access free APIs since it's from a free account
API_KEY = "pk_f6dafbac7efe4534a291b581c52d8f30"


# This class handles all the querying task related to IEX finance
class IEXQuery:

    # Search for a stock ID (symbol) based on a name of company
    @staticmethod
    def search_stock_name(name):
        ret = []
        f = get_symbols(output_format="json", token=API_KEY)
        for s in f:
            if name in s['name'].lower():
                ret.append(s['symbol'])
        return ret

    # Get the details about a stock_id (symbol)
    # This will include the name of the company, the currency used and so on
    @staticmethod
    def get_symbol_detail(symbol):
        f = get_symbols(output_format='json', token=API_KEY)
        for s in f:
            if s['symbol'] == symbol:
                return s
        return None

    def __init__(self):
        self._stock = None      # The current stock id
        self.symbol_info = None # Details about current stock id

    # Set the current stock Id that is querying
    def set_stock_id(self, stock_id):
        self.symbol_info = IEXQuery.get_symbol_detail(stock_id)
        if self.symbol_info is None:
            return False
        else:
            self._stock = Stock(stock_id, output_format="json", token=API_KEY)
            return True

    # Show the candlestick graph of the current stock from a specified date to now
    def plot_graph(self, start):
        price_sheet = None
        try:
            # obtain the data from IEX cloud. we use json format since it's easy to process
            # chartSimplify meant to simply the data, since we don't want to many data to plot the graph
            price_sheet = get_historical_data(self.symbol_info['symbol'], start, str(datetime.date.today()),
                                              output_format='json', chartSimplify=True, token=API_KEY)
        except IEXQueryError as ex:
            return "Sorry, but I have trouble obtaining the balance data."

        try:
            # Import the MatPlotLib and MatPlotLib Finance libraries
            import matplotlib.pyplot as plt
            import mpl_finance as mpf
            from matplotlib.pylab import date2num

            # Convert the obtained data to the format that MatPlotLib can understand
            data = []
            for k in price_sheet.keys():
                a = price_sheet[k]
                # Convert the dates to float, making MatPlotLib understand them
                date_time = datetime.datetime.strptime(k, '%Y-%m-%d')
                data.append([date2num(date_time), a['open'], a['close'], a['high'], a['low'], a['volume']])

            fig, ax = plt.subplots(figsize=(1200 / 72, 480 / 72))
            fig.subplots_adjust(bottom=0.1)
            mpf.candlestick_ochl(ax, data, colordown='#53c156', colorup='#ff1717', width=0.3, alpha=1)
            ax.grid(True)
            ax.xaxis_date()

            # Now return the figure instead of string.
            # Different user interfaces have different ways to show figures
            return fig
        except Exception as e:
            # Once there's errors, we just return a error message.
            return "Oops, something wrong happened while plotting the graph!"

    # (Not used) Get the Quote of the stock, which includes realtime data
    # Not used since realtime data are not always available
    def query_current_quote(self):
        quote = self._stock.get_quote()
        return quote

    # Obtain the company details of the stock
    # the information includes name, description, location, website, ceo of the company
    def company_info(self, item):
        info = self._stock.get_company()
        for k in info:
            if item in k.lower():
                return info[k]
        return None

    # Obtain the historical price data at specific date
    def query_historical_price(self, date):
        price_info = get_historical_data(self.symbol_info['symbol'], date, chartByDay=True, token=API_KEY, output_format='json')
        if isinstance(price_info, dict):
            actual_date = list(price_info.keys())[0]
            price_info = price_info[actual_date]
            ret = {
                'actual_date': actual_date,
                'open': price_info['open'],
                'close': price_info['close'],
                'high': price_info['high'],
                'low': price_info['low'],
                'volume': price_info['volume']
            }
            return ret
        else:
            return None

