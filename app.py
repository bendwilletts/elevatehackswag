from flask import Flask, redirect, send_from_directory, jsonify, request
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import copy
import random

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, "index.html")

#Read CSV
child_care = pd.read_csv("child-care.csv", encoding="latin1")

def availability_generator(df,listofcolumns):
    new_col = []
    for column in listofcolumns:
        x = []
        for i in range(len(df)):
            x.append(random.randint(0,int((df.iloc[i][column])/2)))
        df[column+'_AVAIL'] = x
        new_col.append(str(column+'_AVAIL'))
    return df, new_col

def calc_distance(lata,lona,latb,lonb):
   # approximate radius of earth in km
    R = 6373.0
    lat1 = radians(lata)
    lon1 = radians(lona)
    lat2 = radians(latb)
    lon2 = radians(lonb)
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def rand_cost_arr(low, high):
    test = []
    for i in range(count_cc_rows):
        rand = random.randrange(low, high)
        test.append(rand)
    return test

#Preprocessing:
#(1) AUSPICE: (Non Profit = 1 and Commercial = 0)
child_care['AUSPICE'] = (child_care['AUSPICE'] == 'Non Profit Agency').astype(int)

#(2) SUBSIDY: (Subsidized = 1 and Not Subsidized = 0)
child_care['SUBSIDY'] = (child_care['SUBSIDY'] == 'Y').astype(int)

#(3) AVAILABLE SPACE:
avail_space, col = availability_generator(copy.deepcopy(child_care),['IGSPACE','TGSPACE','KGSPACE','PGSPACE','SGSPACE'])
for column in col:
    child_care[column] = avail_space[column]
child_care['TOT_AVAIL'] = child_care[list(col)].sum(axis=1)

#(4) COST OF CHILD CARE (per day)
count_cc_rows = child_care.shape[0]
child_care['cost_IG'] = rand_cost_arr(45,65)
child_care['cost_TG'] = rand_cost_arr(45,65)
child_care['cost_PG'] = rand_cost_arr(35,55)
child_care['cost_KG'] = rand_cost_arr(30,45)
child_care['cost_SG'] = rand_cost_arr(20,35)

@app.route("/")
def helloWorld():
    return 'Hello World'

@app.route("/getPreprocessedData", methods=['GET'])
def preprocessedData():
    if request.method == 'GET':
        return child_care[['LOC_NAME', 'LONGITUDE', 'LATITUDE', 'PHONE', 'AUSPICE', 'SUBSIDY', #'DIST_FROM_HOME',
                 'IGSPACE', 'TGSPACE', 'PGSPACE', 'KGSPACE', 'SGSPACE', 'TOTSPACE',
                 'IGSPACE_AVAIL', 'TGSPACE_AVAIL', 'KGSPACE_AVAIL', 'PGSPACE_AVAIL', 'SGSPACE_AVAIL', 'TOT_AVAIL',
                 'cost_IG', 'cost_TG', 'cost_PG', 'cost_KG', 'cost_SG']
                ].to_json(orient='index')

@app.route("/getChildCareData", methods=['POST'])
def childcare():
    if request.method == 'POST':
        #Getting Parameters
        in_loc_lat = request.values.get('a', type=str, default=None)
        in_loc_lon = request.values.get('b', type=str, default=None)

        temp = copy.deepcopy(child_care)
        #(4) DISTANCE FROM HOME
        distance_col = []
        for K, row in child_care.iterrows():
            distance_col.append(calc_distance(float(in_loc_lat),float(in_loc_lon),row['LATITUDE'],row['LONGITUDE']))

        temp['DIST_FROM_HOME'] = distance_col

        return temp[['LOC_NAME', 'LONGITUDE', 'LATITUDE', 'PHONE', 'AUSPICE', 'SUBSIDY', 'DIST_FROM_HOME',
                 'IGSPACE', 'TGSPACE', 'PGSPACE', 'KGSPACE', 'SGSPACE', 'TOTSPACE',
                 'IGSPACE_AVAIL', 'TGSPACE_AVAIL', 'KGSPACE_AVAIL', 'PGSPACE_AVAIL', 'SGSPACE_AVAIL', 'TOT_AVAIL',
                 'cost_IG', 'cost_TG', 'cost_PG', 'cost_KG', 'cost_SG']
                ].to_json(orient='index')

if __name__ == '__main__':
    app.run()
