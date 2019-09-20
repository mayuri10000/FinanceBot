import random
import datetime
from IEXQuery import IEXQuery
from Templates import *
from pandas import to_datetime

# Make sure the required packages are installed, otherwise display a friendly error message and exit
try:
    from rasa_nlu.training_data import load_data
    from rasa_nlu.config import RasaNLUModelConfig
    from rasa_nlu.model import Trainer
    from rasa_nlu import config
except ImportError:
    print("Oops! This program requires rasa_nlu but it's not installed on your system!")
    exit(-1)


# This class holds the main function of the chat-bot.
# Including nature language parsing and responding to the users' message.
class Bot:
    def __init__(self):
        trainer = Trainer(config.load('spacy_config.yaml'))
        train_data = load_data('training.md')
        self._interpreter = trainer.train(train_data)  # The natual language interpreter trained from the training data
        self._state = "init"  # The state of the bot, can be reset anytime
        self._last_intent = "none"  # Previous intent, useful for multi-time dialog, this is another state variable
        self._query = IEXQuery()  # The IEX cloud query object
        self._stock = ""          # Current stock id, avoiding setting same stock id for more than once
        self._params = {}         # Stored params for multi-time dialog

    # Set the stock Id
    def _set_stock_id(self, stock_id):
        if self._stock != stock_id:
            self._stock = stock_id
            return self._query.set_stock_id(stock_id)
        return True

    # Handle the graph query
    def _handle_graph_ask(self):
        # Check params, once a required param not presented, enter another round of dialog
        # and ask the user for the param
        if 'stock_id' not in self._params:
            self._last_intent = "graph_query"
            self._state = "ask_stock_id"
            return random.choice(ask_stock_id_msg)

        if 'date' not in self._params:
            self._last_intent = 'graph_query'
            self._state = 'ask_date'
            return random.choice(ask_date_graph_msg)

        stock_id = self._params['stock_id']
        date = self._params['date']

        if not self._set_stock_id(stock_id):
            self._last_intent = "none"
            self._params.clear()
            return random.choice(stock_id_fallback_msg).format(stock_id)

        ret = [random.choice(graph_msg).format(stock_id, date), self._query.plot_graph(date)]
        # After each succeed dialog, reset the last intent and params
        self._last_intent = "none"
        self._params.clear()
        return ret

    # Handle the query of the latest price
    def _handle_current_price_ask(self):
        if 'stock_id' not in self._params:
            self._state = "ask_stock_id"
            self._last_intent = "price_query_current"
            return random.choice(ask_stock_id_msg)

        if 'price_type' not in self._params:
            self._state = "ask_price_type"
            self._last_intent = "price_query_current"
            return random.choice(ask_price_type_msg)

        stock_id = self._params['stock_id']
        price_type = self._params['price_type']

        if not self._set_stock_id(stock_id):
            self._last_intent = "none"
            self._params.clear()
            return random.choice(stock_id_fallback_msg).format(stock_id)

        # quote = self._query.query_current_quote()

        # The realtime price is not always available in the quote, so we use the latest data instead
        hist_price = self._query.query_historical_price(str(datetime.date.today()))

        if hist_price is None:
            return "Sorry, the data is not available"

        price = hist_price[price_type]

        # The actual date when the data from is also included
        ret = random.choice(current_price_msg).format(
            price_type, stock_id, price, "" if price_type == 'volume' else self._query.symbol_info['currency']
            , hist_price['actual_date'])
        self._last_intent = "none"
        self._params.clear()
        return ret

    # Handle price ask at specific date
    def _handle_historical_price_ask(self):
        if 'stock_id' not in self._params:
            self._state = "ask_stock_id"
            self._last_intent = "price_query_historical"
            return random.choice(ask_stock_id_msg)

        if 'price_type' not in self._params:
            self._state = "ask_price_type"
            self._last_intent = "price_query_historical"
            return random.choice(ask_price_type_msg)

        if 'date' not in self._params:
            self._state = "ask_date"
            self._last_intent = "price_query_historical"
            return random.choice(ask_date_msg)

        stock_id = self._params['stock_id']
        price_type = self._params['price_type']
        date = self._params['date']

        if not self._set_stock_id(stock_id):
            return random.choice(stock_id_fallback_msg)

        s = self._query.query_historical_price(date)

        if s is None:
            self._last_intent = "none"
            self._params.clear()
            return "Sorry, no data is available."

        price = s[price_type]

        self._last_intent = "none"
        self._params.clear()
        return random.choice(historical_price_msg)\
            .format(price_type if price_type == 'volume' else price_type + ' price', self._query.symbol_info['symbol'],
                    s['actual_date'], price, "" if price_type == 'volume' else self._query.symbol_info['currency'])

    # Handles query of company info
    def _handle_company_info_ask(self):
        if 'stock_id' not in self._params:
            self._state = "ask_stock_id"
            self._last_intent = "company_info_query"
            return random.choice(ask_stock_id_msg)

        if 'company_info' in self._params:
            company_info = self._params['company_info']
        else:
            company_info = 'description'

        stock_id = self._params['stock_id']

        if not self._set_stock_id(stock_id):
            self._last_intent = "none"
            self._params.clear()
            return random.choice(stock_id_fallback_msg).format(stock_id)

        info = self._query.company_info(company_info)

        # If the user ask about a invalid type of information, we don't know
        if info is None or company_info not in company_info_msg:
            self._last_intent = "none"
            self._params.clear()
            return "Sorry, I don't know this."

        self._last_intent = "none"
        self._params.clear()
        return company_info_msg[company_info].format(info)

    # Other stuffs
    def _handle_thank(self):
        return random.choice(thank_response_msg)

    def _handle_greeting(self):
        return random.choice(greeting_msg)

    def _handle_love(self):
        return random.choice(love_msg)

    def _handle_hate(self):
        return random.choice(hate_msg)

    # Utility function to find a entity with specific name in a entities array
    def _obtain_entity(self, entities, name):
        for entity in entities:
            if entity['entity'] == name:
                return entity['value']
        return None

    # def _handle_query_stock_id(self, ):
    # Utility function to find the stock ID (symbol) for specific company
    def _get_symbol(self, stock_name):
        stock_name = stock_name.replace('.', '').strip()
        lst = IEXQuery.search_stock_name(stock_name)
        if len(lst) >= 1:
            return lst[0]
        else:
            return None

    # respond function to user messages
    def respond(self, user_msg):
        try:
            # First we should interpret the user's word
            parsed = self._interpreter.parse(user_msg)
            intent = parsed["intent"]
            entities = parsed["entities"]

            # return str(parsed)

            # The confidence of the intent is too low, we're not sure about it
            if intent["confidence"] < 0.2:
                return random.choice(fallback_msg)

            intent = intent["name"]
            stock_id = None

            # First find all the stock id and stock names
            stock_id = self._obtain_entity(entities, 'stock_id')

            stock_name = self._obtain_entity(entities, 'company_name')
            if stock_name is not None:
                symbol = self._get_symbol(stock_name)
                if symbol is None:
                    return random.choice(no_company_msg)
                stock_id = symbol

            if stock_id is not None:
                self._params["stock_id"] = stock_id

            # Reset command, reset the bot's state to initial
            if intent == 'reset':
                self._state = 'init'
                self._last_intent = 'none'
                self._params.clear()
                return random.choice(reset_msg)

            if self._state == 'ask_stock_id':
                if intent != 'stock_id' and intent != 'company_name':
                    return random.choice(stock_id_fallback_msg).format(stock_id)
                elif intent == 'stock_id':
                    stock_id = self._obtain_entity(entities, 'stock_id')
                elif intent == 'company_name':
                    stock_name = self._obtain_entity(entities, 'company_name')
                    symbol = self._get_symbol(stock_name)
                    if symbol is None:
                        return random.choice(no_company_msg)
                    stock_id = symbol
                self._state = 'init'
                intent = self._last_intent
                self._last_intent = "none"
                self._params['stock_id'] = stock_id

            if self._state == 'ask_price_type':
                if intent != 'price_type' and 'price_type' not in entities:
                    return random.choice(price_type_fallback_msg)
                else:
                    self._state = 'init'
                    intent = self._last_intent
                    self._last_intent = "none"
                    self._params['price_type'] = self._obtain_entity(entities, 'price_type')

            if self._state == 'ask_date':
                # The evaluation of intent 'date' always fails (I don't know why)
                # so I just extract the date entities instead
                date = self._obtain_entity(entities, "date")
                if date is None:
                    return random.choice(date_fallback_msg)
                else:
                    self._state = 'init'
                    intent = self._last_intent
                    self._last_intent = "none"
                    self._params['date'] = self._obtain_entity(entities, 'date')

            if self._state == "init":
                # Find the entities in the statement and store them as params
                if self._obtain_entity(entities, 'date') is not None:
                    self._params['date'] = self._obtain_entity(entities, 'date')

                if self._obtain_entity(entities, 'price_type') is not None:
                    self._params['price_type'] = self._obtain_entity(entities, 'price_type')

                if self._obtain_entity(entities, 'company_info') is not None:
                    self._params['company_info'] = self._obtain_entity(entities, 'company_info')

                # Handle different stuffs
                if intent == 'graph_query':
                    return self._handle_graph_ask()

                if intent == 'price_query_current' or intent == 'price_type':
                    return self._handle_current_price_ask()

                if intent == 'company_info_query' or intent == 'company_name':
                    # if we detect where keyword, we know the user
                    # is asking the location of the company
                    if 'where' in user_msg:
                        self._params["company_info"] = 'address'
                    return self._handle_company_info_ask()

                if intent == 'price_query_historical':
                    return self._handle_historical_price_ask()

                if intent == 'thank':
                    return self._handle_thank()

                if intent == 'greeting':
                    return self._handle_greeting()

                if intent == 'love':
                    return self._handle_love()

                if intent == 'hate':
                    return self._handle_hate()

            return random.choice(fallback_msg)
        except Exception as e:
            # raise e
            return "Sorry, due to a internal error, I have trouble understanding your words."
