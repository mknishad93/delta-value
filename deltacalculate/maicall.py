import time
import deltacalculate.getOption as delta
from datetime import datetime
import logging
import requests
import sys
#import pywhatkit as kit


TELEGRAM_BOT_TOKEN = "7196489801:AAEtN8UxDlPjO8_5RdkeVen9dfs0H7LyW2M"
CHAT_ID = "5102108402"

count = 0

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, json=payload)
    return response.json()

def recall(count):
    try:
        while True:
            logging.info("Entred in recall method -----")
            now = datetime.now()
            if now.hour == 11 and now.minute == 00:  # 3:30 PM
             print("Exiting the function as it's 3:30 PM.")
            sys.exit()  #
            deltaValue =delta.callEveryMinute()  # Run the task
            print("Running -----")
            logging.info("Running -----")
            count = count+1
            # Get the current date and time
            current_datetime = datetime.now()
            current_hour = current_datetime.hour
            current_minute = current_datetime.minute
            current_minuteis = current_minute+2
            print(current_hour, current_minute+2)
            
            # Print the current date and time

            if count == 10 :
              deltaVal = 'Service is Running fine :'
              string_num = str(deltaValue)
              value = deltaVal + string_num
              count =0
              #kit.sendwhatmsg('+919899096249',value, current_hour, current_minuteis)
              send_telegram_message(f"Service is running fine")
              print("hey i am ready", count)
            print("Current Date and Time:", current_datetime)
            time.sleep(60)  # Wait for 60 seconds before running again

    except Exception as e:
         logging.info(f"exception 1 :: {e}")
         print("exception 1===================================================================================================", e)
         count = count+1
         if count == 10 :
            count =0
            
            #kit.sendwhatmsg('+919899096249','Service has error::', current_hour, current_minuteis)
            print("hey i am ready", count)
         time.sleep(120)
         recall(count)



class DeltaValue:

 def calling(self,pe,ce,expirydate, niftySpotPrice, strikepriceSpotPE, strikepriceSpotCE):
   deltaValue =delta.callEveryMinute(pe,ce,expirydate, niftySpotPrice, strikepriceSpotPE, strikepriceSpotCE)
   
   return deltaValue
   



 def calling1(self):
  count = 0
  try:
      while True:
        logging.info("Task is Started to run...")
        now = datetime.now()
        if now.hour == 11 and now.minute == 00:  # 3:30 PM
            print("Exiting the function as it's 3:30 PM.")
            sys.exit()  #
        delta.callEveryMinute()
        count = count+1 # Run the task
        print("Running -----")
        logging.info("Running -----")
        # Get the current date and time
        current_datetime = datetime.now()
        current_hour = current_datetime.hour
        current_minute = current_datetime.minute
        current_minuteis = current_minute+2
        print(current_hour, current_minute+2)
        
        # Print the current date and time

        print("Current Date and Time:", current_datetime)
        if count == 10 :
            deltaVal = 'Service is Running fine :'
            send_telegram_message(f"Service is running fine")
            #string_num = str(deltaValue)
            #value = deltaVal + string_num
            count =0
            
            print("hey i am ready", count)
        time.sleep(80)  # Wait for 60 seconds before running again
  except Exception as e:
    
    count = count+1
    if count == 2 :
      count =0
      #kit.sendwhatmsg('+919899096249','Service has error:', current_hour, current_minuteis)
      print("hey i am ready", count)
    logging.info(f"exception 2 :: {e}")
    print("exception 2===================================================================================================", e)
    time.sleep(120)
    recall(count)
  #return self.e


class CreateToken:
  def token(self,name, userId, token):
        # Open the file in 'write' mode (overwrites any existing content)
      with open('deltacalculate/enctoken.txt', 'w') as file:
       file.write(token)
      with open('deltacalculate/userdetail.txt', 'w') as user: 
       user.write(name)
      with open('deltacalculate/usercode.txt', 'w') as code:  
       code.write(userId)
      
      
      return 'Sucessfully added' 