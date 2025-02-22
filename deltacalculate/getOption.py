import requests
import math
from scipy.stats import norm
import deltacalculate.calculatedelta as delta
from scipy.optimize import brentq
from deltacalculate.kiteapp import *
from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, date, timedelta
#import pywhatkit as payval
from decimal import Decimal
import re
import time
import sys


logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"
)
TELEGRAM_BOT_TOKEN = "7196489801:AAEtN8UxDlPjO8_5RdkeVen9dfs0H7LyW2M"
CHAT_ID = "5102108402"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    return response.json()
def fetch_nifty_option_chain(expiry):
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY&expiryDate={expiry}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        response = session.get(url, headers=headers, verify=False)
        option_chain_data = response.json()
        return option_chain_data
def get_option_chain_for_expiry(symbol, expiry_date):
        # Define the URL for fetching option chain data
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

        # Define the headers for the request
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }

        # Fetch data from NSE
        response = requests.get(url, headers=headers, verify=False)
        #logging.info(f"response:: {response}")
        # Parse the response as JSON
        data = response.json()

        # Extract the records from the data
        records = data['records']['data']

        # Filter data for the specific expiry date
        filtered_data = [
            entry for entry in records if entry['expiryDate'] == expiry_date]

        return filtered_data    

def callEveryMinute():
   
 #logging.info(f"detail PE is :{pe}")
 #logging.info(f"detail CE is :{ce}")
 #logging.info(f"detail Expiry is :{expirydate}")
 # Fetch Nifty option chain data from NSE API
 session = requests.Session()
 now = datetime.now()
 logging.info(f"Task is Started to run:: {now} {now.hour}")
 if now.hour >= 15:  # 3:30 PM
  logging.info("Exiting call function as it's 3:30 PM.")
  sys.exit()

 #print(records)




# Example usage
 #option_chain_data = fetch_nifty_option_chain()
 #print(option_chain_data)


# Example usage
 symbol = "NIFTY"
 #expiry_date = "28-Nov-2024"  # Define the expiry date you want to filter
 #expiry_date = expirydate
 #filtered_option_chain = get_option_chain_for_expiry(symbol, expiry_date)
 #logging.info(f"filtered_option_chain:: {filtered_option_chain}")

# Example usage
 # option_chain_data = fetch_nifty_option_chain()
# print(option_chain_data)

 with open("deltacalculate/enctoken.txt") as f1:
    enctoken = f1.read()
 with open("deltacalculate/userdetail.txt") as user:
    username = user.read()
 with open("deltacalculate/usercode.txt") as code:
    usercode = code.read()       

 kite = KiteApp(reqsession=session,api_key=username, userid=usercode, enctoken=enctoken, debug=False)

 #logging.info(f"usercode::   {usercode}")
 #logging.info(f"enctoken:: {enctoken} ")
 #logging.info(f"username:: {username} ")
# holding = kite.holdings()
 positionm = kite.positions()
 peToken = ''
 peLastPrice = ''
 ceToken = ''
 ceLastPrice = ''
 CeStrikePrice = ''
 CeStrikePrice = ''
 expiryMonth = ''
 optionTypeCE = ''
 optionTypePE = ''
 
 for item in positionm["net"]:
 
    tradingsymbol = item["tradingsymbol"]
    instrument_token = item["instrument_token"]
    quantity = item["quantity"]
    last_price = item["last_price"]
    pnl = item["pnl"]
    expiry, option_type, strike_price = parse_option_symbol(tradingsymbol)
    expiryMonth = expiry
    if option_type == 'PE':
        peToken = instrument_token
        peLastPrice= last_price
        PeStrikePrice = strike_price
        optionTypePE = option_type
    if option_type == 'CE': 
        ceToken = instrument_token
        ceLastPrice= last_price
        CeStrikePrice = strike_price
        optionTypeCE = option_type
          
    print(f"Expiry: {expiry}, Option Type: {option_type}")
    print(f"Symbol: {tradingsymbol}, Token: {instrument_token}, Qty: {quantity}, LTP: {last_price}, CE: {CeStrikePrice}, PE: {PeStrikePrice}")
    #insturment_type = nifty_option.iloc[0]['instrument_type']
 
    
 print(f"ceToken: {ceToken}, ceLastPrice: {ceLastPrice}, peToken: {peToken}, peLastPrice: {peLastPrice}")
 
 # Filter for Nifty options
 #nifty_options = [i for i in instruments if i["tradingsymbol"].startswith("NIFTY")]

# Display Nifty options instruments
 #for option in nifty_options:
 #   print(option["tradingsymbol"])
 
 #nifty = Ticker("^NSEI")  # ^NSEI is the ticker for NIFTY 50
 #nifty_price = nifty.history(period="1d")["Close"].iloc[-1]
 #nifty_price = round(nifty_price, )
 #nifty_option = nifty.history(period="2mo")

 #print(f"NIFTY 50 Last Price: {nifty_price}")
 #expirations = nifty_option.options
 #print("Available Expiry Dates: ", nifty_option)

# Select a particular expiry date (example: '2025-02-20')
 #expiry_date = '2025-02-27'  # Get the first available expiry date

# Fetch the option chain data for the selected expiry date
 #option_chain = nifty.option_chain(expiry_date)

# Get the Call and Put options data
 #calls = option_chain.calls
 #puts = option_chain.puts

 #print("\nCall Options Data:")
 #print(calls)

 #print("\nPut Options Data:")
 #print(puts)
 #ltp= kite.quote(['NSE: NIFTY50'])
 #print(positionm)
 #nifty_spot = kite.ltp("NSE:NIFTY") 
 #print(nifty_spot)

# Initialize KiteConnect with your API key
# kite = KiteConnect(api_key="your_api_key")

# Set the access token that you generated in the previous step#
# kite.set_access_token("your_access_token")


# Fetch the instrument list
 
 #nifty_options_df = kite.get_nifty_option_chain()
 #logging.info(f"detail PE is :{nifty_options_df}")
 #print(nifty_options_df.head())
 # Convert to JSON
 #json_data = nifty_options_df.to_json(orient="records")

 #print(json_data)
 #token=kite.get_nifty_50_token()
 #print(token)
 #key = "NSE:INFY"
 #price=kite.quote(key)
 #print(price)
 #niftySpot = kite.get_nifty_50_price()
 #print(niftySpot)
 #nifty_price = kite.get_nifty_50_price()
 #print("NIFTY 50 Current Price:", nifty_price)
 #instrumentsVal = kite.fetch_nse_instruments()
 #nifty_token = 256265
 #expiry = "2025-02-27"
 #strike_price = 23600

 #filtered_options = nifty_options_df[(nifty_options_df["expiry"] == expiry) & 
  #                                  (nifty_options_df["strike"] == strike_price)]
 #print(filtered_options)




 

 #logging.info(f"instruments:: {instruments} ")
 #instruments = kite.instruments()
 #df_instruments = pd.DataFrame(instruments)
 #logging.info(f"df_instruments:: {df_instruments} ")
# Specify the instrument token to search for
 #instrument_token1 = 12902146  # Replace with actual token PE
 #instrument_token2 = 12913922  #CE
 instrument_token1 = peToken  # Replace with actual token PE
 instrument_token2 = ceToken  #CE

 openpositionlist = []
 openpositionlist.append(16114434)
 openpositionlist.append(14021378)


# Filter the instrument list for the matching token
 #nifty_option = df_instruments[df_instruments['instrument_token'] == instrument_token1]
 #logging.info(f"nifty_option:: {nifty_option} ")
# Extract and print the details if found
 #if not nifty_option.empty:
 #   expiry_date = nifty_option.iloc[0]['expiry']
  #  strikeprice = nifty_option.iloc[0]['strike']
   # tradingsymbol = nifty_option.iloc[0]['tradingsymbol']
   # insturment_type = nifty_option.iloc[0]['instrument_type']

    #print(f"Instrument found: {tradingsymbol}")
    #print(f"Expiry Date: {expiry_date}")
    #print("hg", expiry_date)
    #print(f"Strike Price: {strikeprice}")
 #else:
  #  print(f"Instrument with token {instrument_token1} not found.")

# Convert to integer
 #strikepriceint = int(strikeprice)
 
 PeStrikePriceInt = int(PeStrikePrice)
 CeStrikePriceInt = int(CeStrikePrice)

# records = positionm['net']
# str = 'NIFTY24SEP25350PE'


# Convert the string into a datetime objec
 date_obj = pd.to_datetime(expiryMonth)
# Format the date to "DD-MMM-YYYY"
 expiry = date_obj.strftime("%d-%b-%Y")

 print('date', expiry) # format will be like 28-Nov-2024
 filtered_option_chain = fetch_nifty_option_chain(expiry)

# Function to fetch and filter option chain by expiry date
 #records = filtered_option_chain['filtered']['data']
 nifty_price = filtered_option_chain["records"]["underlyingValue"]  # Extract latest price
 print("Nifty 50 Price:", nifty_price)


# nifty spot price S
# K strike price 24000
#market price for spot 
# expiry_date_str '28-Nov-2024


# Example usage

 disct = delta.parse_and_calculate_delta_static(nifty_price, PeStrikePriceInt, peLastPrice,expiry, optionTypePE)
 print('disct is ===', disct)
 pedelta = disct['PE']
 logging.info(f"pedelta::   {pedelta}")
 print('pedelta is ===', pedelta)

# Filter the instrument list for the matching token
 #nifty_option = df_instruments[df_instruments['instrument_token'] == instrument_token2]

# Extract and print the details if found
 #if not nifty_option.empty:
 #   expiry_date = nifty_option.iloc[0]['expiry']
 #   strikeprice = nifty_option.iloc[0]['strike']
 #   tradingsymbol = nifty_option.iloc[0]['tradingsymbol']
 #   insturment_type = nifty_option.iloc[0]['instrument_type']

    # print(f"Instrument found: {tradingsymbol}")
    # print(f"Expiry Date: {expiry_date}")
    # print("hg",expiry_date)
    # print(f"Strike Price: {strikeprice}")
 #else:
 #   print(f"Instrument with token {instrument_token1} not found.")

# Convert to integer
 #strikepriceint = int(strikeprice)

# records = positionm['net']
# str = 'NIFTY24SEP25350PE'


# Convert the string into a datetime objec
 #date_obj = pd.to_datetime(expiry_date)
# Format the date to "DD-MMM-YYYY"
 #formatted_date = date_obj.strftime("%d-%b-%Y")
 #expiry = date_obj.strftime("%d-%b-%Y")
 
 
 # nifty spot price S
# K strike price 24000
#market price for spot 
# expiry_date_str '28-Nov-2024


 disct = delta.parse_and_calculate_delta_static(nifty_price, CeStrikePriceInt, ceLastPrice,expiry, optionTypeCE)
 cedelta = disct['CE']
 logging.info(f"cedelta::   {cedelta}")
 print('CEdelta is ===', cedelta)

 absolute_difference = abs(cedelta) - abs(pedelta)
 absolute_differencenew = round(absolute_difference, 2)
 print("The absolute difference is:", absolute_differencenew)
 if  abs(absolute_differencenew) <= 0.9:
     time.sleep(300)
     send_telegram_message(f"current delta Value is :: {absolute_differencenew} | CE delta: {cedelta} | PE delta: {pedelta}")
     
 

 if abs(absolute_differencenew) >= 0.13:
    send_telegram_message(f"current delta Value is :: {absolute_differencenew} | CE delta: {cedelta} | PE delta: {pedelta}")
    print("going to start take new psotion")
    current_datetime = datetime.now()
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute
    current_minuteis = current_minute+1
    deltaString = str(absolute_differencenew)
    deltaVal = 'Current delta diff price is :'
    value = deltaVal + deltaString
    print("delta is:::",value)

    
    print("going to start take new psotion")
    if abs(cedelta) < abs(pedelta):
        print("going to exit ce position")
        # exit call
        # find ce delta price as same of pe delta
      
       # strikepriceforentry =delta.parse_and_find_delta(
        #    filtered_option_chain, formatted_date, 'CE', pedelta)
        print("gooing to excute this stirke price", strikepriceforentry)

    if abs(cedelta) > abs(pedelta):
        print("going to exit PE position")
        # exit call
        # find ce delta price as same of pe delta
      
        #strikepriceforentry = delta.parse_and_find_delta(
        #    filtered_option_chain, formatted_date, 'PE', cedelta)
        print("gooing to excute this stirke price", strikepriceforentry)

 
 print("Running =======")
 #return absolute_differencenew

def parse_option_symbol(symbol):
    # Regular expression pattern for extracting details
    pattern = r"NIFTY(\d{2})([A-Z]{3})(\d{5})([CP]E)"
    match = re.match(pattern, symbol)
    
    if match:
        year = 2000 + int(match.group(1))  # Extract year and convert to full format
        month_str = match.group(2)  # Extract month abbreviation
        strike_price = match.group(3)  # Extract strike price
        option_type = match.group(4)  # Extract CE/PE
        
        # Convert month abbreviation to month number
        month = datetime.strptime(month_str, "%b").month
        
        # Construct expiry date (assuming last Thursday of the month)
        # Get the last Thursday of the expiry month
        expiry_date = get_last_thursday(year, month)
        #expiry_date = datetime(int(year), month, 1)  # First day of the expiry month
        return expiry_date.strftime("%Y-%m-%d"), option_type, strike_price  # Returning year-month and option type
    
    return None, None , None
def get_last_thursday(year, month):
    """Returns the last Thursday of the given month and year."""
    # Find the last day of the month
    last_day = datetime(year, month + 1, 1) - timedelta(days=1)  # Last day of the given month
    
    # Move back to the last Thursday
    while last_day.weekday() != 3:  # Thursday is represented by 3 in weekday()
        last_day -= timedelta(days=1)
    
    return last_day

'''
if option_chain_data:
    # Accessing all the data for a specific strike price
    for record in option_chain_data['records']['data']:
        print(f"Strike Price: {record['strikePrice']}")
        if 'CE' in record:
            print(f"Call Option OI: {record['CE']['openInterest']}")
            print(f"Call Option LTP: {record['CE']['lastPrice']}")
        if 'PE' in record:
            print(f"Put Option OI: {record['PE']['openInterest']}")
            print(f"Put Option LTP: {record['PE']['lastPrice']}")
        print("------------")

'''


'''
# Black-Scholes function to calculate the option price
def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == 'call':
        option_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        option_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return option_price

# Function to calculate implied volatility
def implied_volatility(S, K, T, r, market_price, option_type='call'):
    # Define a function that computes the difference between the Black-Scholes price and the market price
    def difference_in_price(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - market_price
    
    # Use Brent's method to find the root of the difference_in_price function
    # (i.e., the value of sigma that makes the difference_in_price zero)
    try:
        implied_vol = brentq(difference_in_price, 1e-6, 5.0)  # bounds for volatility [0.000001, 5]
    except Exception as e:
        print(f"Could not calculate implied volatility: {e}")
        implied_vol = None
    
    return implied_vol

# Example usage

# Input parameters
S = 25790  # Nifty current price (spot price)
K = 26000  # Strike price of the option
T = 0.25   # Time to expiration (in years, e.g., 3 months = 0.25)
r = 0.06   # Risk-free interest rate (6%)
market_price = 150  # The market price of the option (observed in the option chain)
option_type = 'call'  # Can be 'call' or 'put'

# Calculate implied volatility
iv = implied_volatility(S, K, T, r, market_price, option_type)
print(f"Implied Volatility: {iv:.4f}")

'''
