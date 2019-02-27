from flask import Flask
import pandas as pd
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/drugabacus/getalldisease',methods=['GET'])
def getAllDisease():
    
    data = []
    json_disease = {}
    
    for diseas in data_set['Disease'].unique():
        tmp_dict = {}
        tmp_dict['name'] = diseas
        data.append(tmp_dict)
    json_disease["disease"] = data
    
    return json.dumps(json_disease)

@app.route('/drugabacus/getdrugs/<diseaseName>',methods=['GET'])
def getAllDrug(diseaseName):
    
    drug_name = data_set[(data_set['Disease'] ==diseaseName)]
    data = []
    json_drugname = {}
    
    for drugname,price in zip(drug_name['Drug'],drug_name['Price($)']):
        tmp_dict = {}
        tmp_dict['name'] = drugname
        tmp_dict['cost'] = price
        data.append(tmp_dict)
    json_drugname["drugname"] = data
  
    return json.dumps(json_drugname)

def initialize():
    global data_set
    data_set = pd.read_excel("drug_prices.xlsx")
    
if __name__ == '__main__':
    initialize()
    app.run()
