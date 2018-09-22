from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def helloWorld():
    return 'Hello World'

@app.route("/getChildCareData")
def childcare():
    if request.method == 'GET':
        child_care = pd.read_csv("child-care.csv", encoding="latin1")
        #Preprocessing
        #(1) AUSPICE: (Non Profit = 1 and Commercial = 0)
        child_care['AUSPICE'] = (child_care['AUSPICE'] == 'Non Profit Agency').astype(int)
        #(2) SUBSIDY: (Subsidized = 1 and Not Subsidized = 0)
        child_care['SUBSIDY'] = (child_care['SUBSIDY'] == 'Y').astype(int)

        #(3) Temporary Output Frame
        output = child_care[['LOC_NAME','LONGITUDE', 'LATITUDE', 'AUSPICE', 'PHONE', 'IGSPACE', 'TGSPACE', 'PGSPACE', 'KGSPACE', 'SGSPACE', 'TOTSPACE', 'SUBSIDY']]
        return output[['LOC_NAME', 'LONGITUDE', 'LATITUDE', 'SUBSIDY', 'TOTSPACE']].to_json(orient='index')

if __name__ == '__main__':
    app.run()
