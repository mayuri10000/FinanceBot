# This file contains the templates of the bot's response.

# When the confidence of intents or entities are too low, we are not sure what the user mean
# The following message will be displayed when the bot don't sure about what the user mean
fallback_msg = ["Sorry, I don't know what you mean.",
                "What did you just said to me? Sorry, I don't get it.",
                "Not again, please stop saying weired things to me."]


reset_msg = ["Ok, let's do other things first, previous cancelled."]

price_type_fallback_msg = ["Please tell me the correct price type you want to query! Possible price types are:"
                           "open, close, high, low, and volume"]

date_range_fallback_msg = [["What did you just said? I'm asking you the time range of the candlestick graph.",
                           "Available time ranges are: all, 5 years, 2 years, 1 year, from the begin of the year,",
                            "6 months, 3 months, 1 months, 5 days"]]

date_fallback_msg = ["Sorry, please give me a valid date."]

ask_price_type_msg = ["Please tell me which type of price you're looking for. "
                      "Possible price types are: open, close, high, low, and volume",
                      "Do you want the volume, open, close, high or low price of the stock?"]

ask_date_msg = ["Please tell me the date what you're querying for.",
                "What date do you want me to find the price?"]

graph_msg = ["Here is the graph showing the price and volume variation of {} in past {}."]

current_price_msg = ["The latest {} price of stocks of {} is {} {} (data from {})"]

ask_stock_id_msg = [
    "You should tell me which company you're querying. Tell me the stock ID or the company name (ends with 'Inc.')"]


no_company_msg = ["Sorry, there is no company with that name!"]

ask_date_range_msg = ["How long ago do you want to plot the graph?"]

ask_date_graph_msg = ["Which day do you want the candlestick graph start from?"]

stock_id_fallback_msg = ["Sorry, the stock {} does not exist or not queryable!"]

historical_price_msg = ["The {} of stocks of {} at {} is {} {}"]

company_info_msg = {"description": "{}",
                    "industry": "The industry of the company is {}.",
                    "ceo": "The CEO of the company is {}.",
                    "website": "{}",
                    "address": "{}"}

thank_response_msg = ["You're welcome.", "That's OK.", "It's okay. Helping human is the responsibility of bots."]

greeting_msg = ["Hello!", "Hi!", "Nice to see you!", "How do you do?"]

love_msg = ["I love you too!", "Darling", "you are my destiny.", "Don't say this to me, I am only a robot and."]

hate_msg = ["If you don't think I am good enough, please send feedback to my developer."]