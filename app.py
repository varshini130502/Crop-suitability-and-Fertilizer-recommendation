# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 11:40:53 2021

@author: K varshini
"""

import numpy as np
import pandas as pd
import requests
import config
import pickle
import streamlit as st
from utils.fertilizer import fertilizer_dic


crop_recommendation_model_path = r"C:/MINI PROJECT/models/RandomForest.pkl"
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))




def weather_fetch(city_name):
   
    api_key = config.weather_api_key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temperature = round((y["temp"] - 273.15), 2)
        humidity = y["humidity"]
        return temperature, humidity
    else:
        return None

def fert_recommend(N,P,K,crop_name):

    df = pd.read_csv(r"C:\crop ml model\fertilizer.csv")

    nr = df[df['Crop'] == crop_name]['N'].iloc[0]
    pr = df[df['Crop'] == crop_name]['P'].iloc[0]
    kr = df[df['Crop'] == crop_name]['K'].iloc[0]

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]
    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"
    return str(fertilizer_dic[key])

def crop_prediction(N,P,K,ph,rainfall,city):

        if weather_fetch(city) != None:
            temperature, humidity = weather_fetch(city)
            data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0] 
        return final_prediction    


def main():
    html_temp="""
    <div style="background-color:#342D7E;padding:10px">
    <h1 style="color:white;text-align:center;">Crop and Fertilizer Recommender</h1>
    </div><br></br>"""
    st.markdown(html_temp,unsafe_allow_html=True)
    html_temp="""
    <div style="background-color:pink;padding:2px">
    <h4 style="color:white;text-align:center;">Crop Recommender</h4>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    N = st.number_input("Nitrogen")
    P = st.number_input("Phoshorous")
    K = st.number_input("Pottasium")
    ph= st.number_input("pH")
    rainfall = st.number_input("Rainfall")
    city=st.selectbox("Select the city",{"hyderabad","Mumbai","Delhi"})
    result=""
    if st.button('Predict crop'):
        result=crop_prediction(N,P,K,ph,rainfall,city)
    st.success(result) 
    html_temp="""
    <div style="background-color:#342D7E;padding:2px">
    <h4 style="color:white;text-align:center;">Fertilizer Recommender</h4>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    Crop=st.text_input("Crop")
    result=""
    if st.button('Predict fertilizer'):
        result=fert_recommend(N,P,K,Crop)
    st.success(result) 
    
        

# ===============================================================================================
if __name__ == '__main__':
    main()
