import requests
import math
from scipy.stats import norm
import deltacalculate.calculatedelta as delta
from scipy.optimize import brentq
from deltacalculate.kiteapp import *
from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, date
import pywhatkit as payval
from decimal import Decimal
from nsepy.derivatives import get_expiry_date
from nsepy.derivatives import get_history

logging.basicConfig(
    level=logging.DEBUG,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def callEveryMinute(pe,ce,expirydate, niftySpotPrice, strikepriceSpotPE, strikepriceSpotCE):
   
 logging.info(f"detail PE is :{pe}")
 logging.info(f"detail CE is :{ce}")
 logging.info(f"detail Expiry is :{expirydate}")
 # Fetch Nifty option chain data from NSE API
 def fetch_nifty_option_chain():
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, verify=False)
        option_chain_data = response.json()
        return option_chain_data


# Function to fetch and filter option chain by expiry date


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


# Example usage
 #option_chain_data = fetch_nifty_option_chain()
 #print(option_chain_data)


# Example usage
 symbol = "NIFTY"
 #expiry_date = "28-Nov-2024"  # Define the expiry date you want to filter
 expiry_date = expirydate
 filtered_option_chain = get_option_chain_for_expiry(symbol, expiry_date)
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
 kite = KiteApp(username, usercode, enctoken)

 logging.info(f"usercode::   {usercode}")
 logging.info(f"enctoken:: {enctoken} ")
 logging.info(f"username:: {username} ")
# holding = kite.holdings()
 positionm = kite.positions()
 print(positionm)
# ins = kite.profile()


# Initialize KiteConnect with your API key
# kite = KiteConnect(api_key="your_api_key")

# Set the access token that you generated in the previous step#
# kite.set_access_token("your_access_token")


# Fetch the instrument list
 instruments = kite.instruments()
 #logging.info(f"instruments:: {instruments} ")
 df_instruments = pd.DataFrame(instruments)
 #logging.info(f"df_instruments:: {df_instruments} ")
# Specify the instrument token to search for
 #instrument_token1 = 12902146  # Replace with actual token PE
 #instrument_token2 = 12913922  #CE
 instrument_token1 = pe  # Replace with actual token PE
 instrument_token2 = ce  #CE

 openpositionlist = []
 openpositionlist.append(16114434)
 openpositionlist.append(14021378)


# Filter the instrument list for the matching token
 nifty_option = df_instruments[df_instruments['instrument_token']
                              == instrument_token1]
 #logging.info(f"nifty_option:: {nifty_option} ")
# Extract and print the details if found
 if not nifty_option.empty:
    expiry_date = nifty_option.iloc[0]['expiry']
    strikeprice = nifty_option.iloc[0]['strike']
    tradingsymbol = nifty_option.iloc[0]['tradingsymbol']
    insturment_type = nifty_option.iloc[0]['instrument_type']

    print(f"Instrument found: {tradingsymbol}")
    print(f"Expiry Date: {expiry_date}")
    print("hg", expiry_date)
    print(f"Strike Price: {strikeprice}")
 else:
    print(f"Instrument with token {instrument_token1} not found.")

# Convert to integer
 strikepriceint = int(strikeprice)
 niftySpotPrice = 12000
 strikepriceSpot = 123

# records = positionm['net']
# str = 'NIFTY24SEP25350PE'


# Convert the string into a datetime objec
 date_obj = pd.to_datetime(expiry_date)
# Format the date to "DD-MMM-YYYY"
 expiry = date_obj.strftime("%d-%b-%Y")

 print('date', formatted_date)

# nifty spot price S
# K strike price 24000
#market price for spot 
# expiry_date_str '28-Nov-2024


# Example usage
 if filtered_option_chain:
    disct = delta.parse_and_calculate_delta_static(niftySpotPrice, strikepriceint, strikepriceSpot,expiry, insturment_type)
    print('disct is ===', disct)
    pedelta = disct['PE']
    print('pedelta is ===', pedelta)

# Filter the instrument list for the matching token
 nifty_option = df_instruments[df_instruments['instrument_token']
                              == instrument_token2]

# Extract and print the details if found
 if not nifty_option.empty:
    expiry_date = nifty_option.iloc[0]['expiry']
    strikeprice = nifty_option.iloc[0]['strike']
    tradingsymbol = nifty_option.iloc[0]['tradingsymbol']
    insturment_type = nifty_option.iloc[0]['instrument_type']

    # print(f"Instrument found: {tradingsymbol}")
    # print(f"Expiry Date: {expiry_date}")
    # print("hg",expiry_date)
    # print(f"Strike Price: {strikeprice}")
 else:
    print(f"Instrument with token {instrument_token1} not found.")

# Convert to integer
 strikepriceint = int(strikeprice)

# records = positionm['net']
# str = 'NIFTY24SEP25350PE'


# Convert the string into a datetime objec
 date_obj = pd.to_datetime(expiry_date)
# Format the date to "DD-MMM-YYYY"
 formatted_date = date_obj.strftime("%d-%b-%Y")
 
 
 # nifty spot price S
# K strike price 24000
#market price for spot 
# expiry_date_str '28-Nov-2024

 if filtered_option_chain:
    disct = delta.parse_and_calculate_delta_static(niftySpotPrice, strikepriceint, strikepriceSpot,expiry, insturment_type)
    cedelta = disct['CE']
    print('CEdelta is ===', cedelta)

 absolute_difference = abs(cedelta) - abs(pedelta)
 absolute_differencenew = round(absolute_difference, 2)
 print("The absolute difference is:", absolute_differencenew)
 

 if abs(absolute_differencenew) >= 0.17:
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
      
        strikepriceforentry =delta.parse_and_find_delta(
            filtered_option_chain, formatted_date, 'CE', pedelta)
        print("gooing to excute this stirke price", strikepriceforentry)

    if abs(cedelta) > abs(pedelta):
        print("going to exit PE position")
        # exit call
        # find ce delta price as same of pe delta
      
        strikepriceforentry = delta.parse_and_find_delta(
            filtered_option_chain, formatted_date, 'PE', cedelta)
        print("gooing to excute this stirke price", strikepriceforentry)

 
 print("Running =======")
 return absolute_differencenew

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
