# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 15:45:06 2022

@author: kvssn
"""

import requests
import json
import numpy as np

import pickle

from flask import Flask, request, render_template

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "EK-ymPhn_umtDDErCfMi0wUMXwYAIxatBJVd-XE-ZLBO"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"field":['city', 'BHKS', 'sqft_per_inch', 'build_up_area", "Type_of_property', 'deposit'], "values": [[1,12,200,2,2,20000]]}]}

#response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/62322893-025d-4b5e-ba56-71c902a6a5ba/predictions?version=2022-07-28', json=payload_scoring,
 #headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())
app=Flask(__name__)
model = pickle.load(open(r"C:\Users\INUGURTHI BHAGIRADH\Desktop\MLDL\model.pkl",'rb'))

@app.route('/', methods=['GET'])

def index():

    return render_template("sample.html")

@app.route('/sample.html', methods=['GET'])
def about():
    return render_template("sample.html")
@app.route('/sample2', methods=['GET'])
def page():
    return render_template("sample2.html")

@app.route('/sample3', methods=['GET', 'POST'])
def predict():

    #input_features = [float(x) for x in request.form.values()] 
    #features_value = [np.array(input_features)]
    City=request.form["City"]
    BHKS=request.form["BHKS"]
    sqft_per_inch=request.form["sqft_per_inch"]
    build_up_area=request.form["build_up_area"]
    Type_of_property=request.form["Type_of_property"]
    deposit=request.form["deposit"]
    if(City=="Ahmedabad"):
        City=0
    if(City=="Trivandram"):
        City=1
    if(City=="Banglore"):
        City=2
    if(City=="Chennai"):
        City=3
    if(City=="Hyderabad"):
        City=4
    if(City=="Mumbai"):
        City=5
    if(City=="Delhi"):
        City=6
    if(City=="Pune"):
        City=7
    if(build_up_area=="Build-up Area"):
        build_up_area=0
    if(build_up_area=="Carpet Area"):
       build_up_area=1
    if(build_up_area=="Plot Area"):
       build_up_area=2
    if(build_up_area=="Super built-up Area"):
       build_up_area=3
    if(Type_of_property=="Farm"):
         Type_of_property=0
    if(Type_of_property=="Independent"):
        Type_of_property=1
    if(Type_of_property=="Residential"):
        Type_of_property=0
    if(Type_of_property=="Studio"):
        Type_of_property=0
    t=[[int(City),int(BHKS),int(sqft_per_inch),int(build_up_area),int(Type_of_property),int(deposit)]]
    print(t)
    payload_scoring = {"input_data": [{"field":['city', 'BHKS', 'sqft_per_inch', 'build_up_area", "Type_of_property', 'deposit'], "values":t}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0ed31e1d-7a14-455f-816d-87a12e95f746/predictions?version=2022-08-03', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("scoring Respose")
    #print(features_value)

    #features_name = ['city', 'BHKS', 'sqft_per_inch', 'build_up_area", "Type_of_property', 'deposit']

   # prediction =model.predict(features_value)
    prediction=response_scoring.json()

    output=prediction["predictions"][0]["values"][0][0] #np.exp(predictions)

    output = np.exp(output)

    output= np.round(output)

    print(output)

    return render_template(r"sample2.html", prediction_text= 'House Rent is {}' .format((output)))

if __name__=='__main__':

    app.run(debug=False)
