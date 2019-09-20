## intent:greeting
- hello
- hi
- nice to meet you
- how do you do

## intent:thank
- thank you
- thanks

## intent:love
- i love you
- you are my darling
- darling
- you are my destiny

## intent:reset
- cancel operation
- cancel
- reset

## intent:company_name
- [Apple Inc.](company_name)
- [Bilibili Inc.](company_name)
- [Huawei Inc.](company_name)
- [Lenovo Inc.](companuy_name)

## intent:stock_id
- [AAPL](stock_id)
- [GOOG](stock_id)
- [BILI](stock_id)

## intent:company_info_query
- company information
- can you tell me the company information
- i want the information about [Apple Inc.](company_name)
- i want to know what [Alphabit Inc](company_name) is
- who is the [CEO](company_info) of [Bilibili Inc.](company name)
- the [CEO](company_info) of [Bilibili Inc.](company name)
- [webiste](company_info) of [Bilibili Inc.](company name)
- where is [Bilibili Inc.](company_name)
- what's the [website](company_info) of [Bilibili Inc.](company_name)
- can you tell me the [address](company_info) of [Bilibili Inc.](company_info)
- what's the name of [CEO](company_info) of [BILI](stock_id)

## intent:price_type
- [close](price_type) price
- [open](price_type) price
- [low](price_type) price
- [high](price_type) price
- [volume](price_type)
- [close](price_type)
- [open](price_type)
- [low](price_type)
- [high](price_type)
- [close](price_type) price, please
- [open](price_type) price, please
- [low](price_type) price, please
- [high](price_type) price, please

## intent:price_query_historical
- can you tell me the stocks price of [Apple Inc.](company_name) at [2019-01-01](date)
- what's the price of stocks of [Apple Inc.](company_name) at [2019-01-01](date)
- what's the stocks price of [Apple Inc.](company_name) at [2019-01-01](date)
- what's the [open](price_type) price of stocks of stocks of [Bilibili Inc.](company_name) at [2019-01-12](date)
- [close](price_type) price at [2019-01-09](date) of stocks of [Apple Inc.](company_name)
- can you tell me the [close](price_type) price of stocks of [Alphabet Inc.](company_name) at [2019-01-01](date)
- [low](price_type) price of stocks of [Bilibili Inc.](company_name) at [2019-01-01](date)
- [volume](price_type) of stocks of [Bilibili Inc.](company_name) at [2008-08-08](date)

## intent:graph_query
- graph
- graph of [Alphabet Inc.](company_name)
- graph of [Alphabet Inc.](company_name) from [2018-12-31](date)
- can you plot the graph of [Bilibili Inc.](company_name) from [2019-01-01](date)
- can you plot the graph of [Alphabet Inc.](company_name)
- plot the graph of [Apple Inc.](company_name)
- plot the graph of [Bilibili Inc.](company_name) from [2012-01-11](date)
- plot the graph of [Bilibili Inc.](company_name) from [2019-12-11](date) to now

## intent:price_query_current
- stocks price
- prices of stock
- stocks price of [Apple Inc.](company_name)
- latest stocks price of [Bilibili Inc.](company_name)
- current price of stocks of [Alphabet Inc.](company_name)
- [close](price_type) price of stocks of stocks of [Bilibili Inc.](company_name)
- [open](price_type) price of stocks of [Alphabet Inc.](company_name)
- [low](price_type) price of stocks of [Bilibili Inc.](company_name)
- [high](price_type) price of stocks of [Apple Inc.](company_name)
- [volume](price_type) of of stocks [Apple Inc.](company_name)
- can you tell me the stock price
- can you tell me the latest stock price of [Bilibili Inc.](company_name)
- can you tell me the price of stocks of [Apple Inc.](company_name)
- can you tell me the stock price of [Apple Inc.](company_name)
- can you tell me the latest price of stocks of [Apple Inc.](company_name)
- can you tell me the [close](price_type) of stocks of [Apple Inc.](company_name)
- what's the [open](price_type) price of stocks of [Bilibili Inc.](company_name)
- what's the latest price of stocks of [Alphabet Inc.](company_name)
- what's the [volume](price_type) of stocks of [Apple Inc.](company_name)

## regex:date
-  /^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/;
