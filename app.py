from flask import Flask, redirect, send_from_directory, jsonify, request, url_for, render_template
from flask_cors import CORS
import pandas as pd
from math import sin, cos, sqrt, atan2, radians
import copy
import random
import requests

davinciAPIkey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJDQlAiLCJ0ZWFtX2lkIjoiZGExMmEwZmUtNDkzNy0zNzQ3LWI3ZTctZTgzMDQwMTJmNmFiIiwiZXhwIjo5MjIzMzcyMDM2ODU0Nzc1LCJhcHBfaWQiOiJkNzI3OGJmYS1kZmM5LTRlODQtODdhMi01NDZlY2E5YThiOTcifQ.bhEkLXi8LHS6iLJCGGjhmnOfXkkT8LZs1-LaNb3c4j4"

app = Flask(__name__, static_folder='static')
app.debug = True

CORS(app)

current_user = None
form_data = {}

class User(object):
    name = ""
    age = 0
    gender = ""
    income = 0.0
    lat = 0.0
    lng = 0.0
    address = ""
    postCode = ""
    relationStatus = ""
    workAddress = ""
    dailyCost = 0.0
    numInfant = 0
    numTodd = 0
    numPre = 0
    numKinder = 0
    numSchool = 0

    # The class "constructor" - It's actually an initializer 
    def __init__(self, name, age, gender, income, lat, lng, address, postCode, relationStatus, workAddress, dailyCost, numInfant, numTodd, numPre, numKinder, numSchool):
        self.name = name
        self.age = age
        self.gender = gender
        self.income = income
        self.lat = lat
        self.lng = lng
        self.address = address
        self.postCode = postCode
        self.relationStatus = relationStatus
        self.workAddress = workAddress
        self.dailyCost = dailyCost
        self.numInfant = numInfant
        self.numTodd = numTodd
        self.numPre = numPre
        self.numKinder = numKinder
        self.numSchool = numSchool



@app.route('/')
def reroute():
	return redirect(url_for('login'))

@app.route('/login')
def login():
	if current_user != None:
		return redirect(url_for('home'))
	return render_template('login.html')

@app.route('/handle_data', methods=['POST'])
def handle_data():
    error=None
    if len(request.form['custId'])==0:
        error="Invalid customer ID"
        return render_template('login.html', error=error)

    for key,val in request.form.items():
        if val=='':
            form_data[key] = 0 if key != "workAddress" else ""
        else: 
            form_data[key] = val
    #return render_template('success.html', form_data=form_data)
    response = requests.get('https://api.td-davinci.com/api/customers/' + form_data['custId'],
                                headers = { 'Authorization': davinciAPIkey })
    print(response)
    global current_user
    current_user = User(
        str(response.json()['result']['givenName'] + " " + response.json()['result']['surname']), 
        int(response.json()['result']['age']), 
        str(response.json()['result']['gender']), 
        float(response.json()['result']['totalIncome']),
        float(response.json()['result']['addresses']['principalResidence']['latitude']),
        float(response.json()['result']['addresses']['principalResidence']['longitude']),
        str(response.json()['result']['addresses']['principalResidence']['streetNumber'] + " " + response.json()['result']['addresses']['principalResidence']['streetName']),
        str(response.json()['result']['addresses']['principalResidence']['postalCode']),
        str(response.json()['result']['relationshipStatus']),
        str(form_data["workAddress"]),
        float(form_data["dailyCost"]),
        int(form_data["numInfant"]),
        int(form_data["numToddler"]),
        int(form_data["numPreSchool"]),
        int(form_data["numKinder"]),
        int(form_data["numSchool"]))

    for attr, value in current_user.__dict__.items():
        print(attr, value)

    return redirect(url_for('home'))

@app.route('/home')
def home():
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


#Example ID: d7278bfa-dfc9-4e84-87a2-546eca9a8b97_c418b5e6-ef7a-4774-88bc-762f2e9adc53
@app.route("/getPreprocessedData", methods=['GET'])
def preprocessedData():
    if request.method == 'GET':
        return child_care[['LOC_NAME', 'LONGITUDE', 'LATITUDE', 'PHONE', 'AUSPICE', 'SUBSIDY', #'DIST_FROM_HOME',
                 'IGSPACE', 'TGSPACE', 'PGSPACE', 'KGSPACE', 'SGSPACE', 'TOTSPACE',
                 'IGSPACE_AVAIL', 'TGSPACE_AVAIL', 'KGSPACE_AVAIL', 'PGSPACE_AVAIL', 'SGSPACE_AVAIL', 'TOT_AVAIL',
                 'cost_IG', 'cost_TG', 'cost_PG', 'cost_KG', 'cost_SG']
                ].to_json(orient='index')

@app.route("/getChildCareData")
def childcare():
    #Getting Parameters
    in_loc_lat = request.values.get('lat', type=str, default=None)
    in_loc_lon = request.values.get('lon', type=str, default=None)

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
