import threading
import requests
from flask import Flask, jsonify
import streamlit as st
from flask import Flask, jsonify
from deltacalculate.maicall import DeltaValue, CreateToken
import logging

# Flask API Setup

value = DeltaValue()
getToken = CreateToken()

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Streamlit Interface
st.title("Streamlit with Integrated Flask API")

with st.form("user_form"):
 pe = st.number_input("Enter the PE number", placeholder="Type PE here...")
 strikepriceSpotPE = st.number_input("Enter PE Spot Price", placeholder="Type PE Spot Price here...")
 ce = st.number_input("Enter the CE number", placeholder="Type CE here...")
 strikepriceSpotCE = st.number_input("Enter CE Spot Price", placeholder="Type CE Spot Price here...")
 niftySpotPrice = st.number_input("Enter NIFTY Spot Price", placeholder="Type NIFT Spot Price here...")
 expirydate = st.text_input("Enter the Expiry",placeholder="Type expiry here...")
 submitted = st.form_submit_button("Submit")
 
if submitted:    
   if pe and ce and expirydate:
       logging.info("Entred in method -----")
       item = value.calling(pe,ce,expirydate, niftySpotPrice, strikepriceSpotPE, strikepriceSpotCE)
       logging.info(f"detail is :{item}") 
       st.success(f"delta Value, {item}")

if st.button("Running API"):
    try:
        # Call the Flask API
        value.calling1()

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")       
st.title("Fill the form to create the token")
with st.form("create_token"):
 name = st.text_input("Enter the username", placeholder="Type user name here...")
 id = st.text_input("Enter the code", placeholder="Type user code here...")
 token = st.text_input("Enter the token",placeholder="Type expiry here...")
 submitted = st.form_submit_button("Submit")

if submitted:    
   if name and id and token:
        logging.info("Entred in method -----")
        msg =getToken.token(name,id,token)
        data = {"message": " {msg} "}
        st.success(f"Hello, {data}")
   else:
       st.error("error")    

if st.button("Get Data from Flask API"):
    try:
        # Call the Flask API
        response = requests.get("http://127.0.0.1:5000/api/data")
        if response.status_code == 200:
            data = response.json()
            st.write("API Response:", data)
        else:
            st.error("Failed to get data from the API.")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")




