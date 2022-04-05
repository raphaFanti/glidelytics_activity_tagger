# Authentication

# 1. Get client_id from
# https://www.strava.com/settings/api. In your first time you need to create an app to get this info.

# 2. Visit page
# http://www.strava.com/oauth/authorize?client_id=[YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all
# replacing placeholder with client_id. This step is not needed if you only want to access your public activities (read scope which is default). In that case you can skip step 3 and copy your access code directly to the config.ini file (step 4)

# Get field "code" from response after redirection, finding it on the response URL (it will look like an error response).

# 3. Using postman or CURL, make a POST request to https://www.strava.com/oauth/token?client_id=[YOUR_CLIENT_ID]&client_secret=[YOUR_CLIENT_SECRET]&code=[CODE_FROM_PREVIOUS_STEP]&grant_type=authorization_code

# You should get a response with an authorization token, a refresh token and a validity (expires_at)

# 4. Open file config.ini (or else create such file on root using example_config.ini). Update the file with the below fields and save:
# - client_id
# - client_secret
# - access_token
# - refresh_token
# - expires_at (in seconds from epoch format - same as the above response. Also works if left at zero)

import datetime
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from pandas import json_normalize

auth_url = "https://www.strava.com/oauth/token"
activites_url = "https://www.strava.com/api/v3/athlete/activities"
activity_url = "https://www.strava.com/api/v3/activities/"

config_filename = "config.ini"

import configparser
config = configparser.ConfigParser()
config.read(config_filename)
print("Client ID: {}".format(config["strava"]["client_id"]))

expires_at_epoch = int(config["strava"]["expires_at"])
expires_at_date = datetime.datetime.fromtimestamp(expires_at_epoch)
refresh_token = config["strava"]["refresh_token"]
access_token = config["strava"]["access_token"]
print("Token expires at: {}".format(expires_at_date))

if datetime.datetime.now() >= expires_at_date:
    print("Refreshing token")
    payload = {
        'client_id': config["strava"]["client_id"],
        'client_secret': config["strava"]["client_secret"],
        'refresh_token': refresh_token,
        'grant_type': "refresh_token",
        'f': 'json'
    }

    try:
        response = requests.post(auth_url, data=payload, verify=False).json()
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        expires_at_epoch = int(response['expires_at'])
        expires_at_date = datetime.datetime.fromtimestamp(expires_at_epoch)
        print("Token refreshed successtully and expires at: {}".format(expires_at_date))
    except:
        print("Problem refreshing token")

    # writes refreshed values to config file
    config.set("strava", "access_token", access_token)
    config.set("strava", "refresh_token", refresh_token)
    config.set("strava", "expires_at", str(expires_at_epoch))
    with open(config_filename, 'w') as configfile:
        config.write(configfile)
else:
    print("Token still valid")

header = {'Authorization': 'Bearer ' + access_token}

# Getting list of paragliding activities

activities_total = 400
# activities per page
activities_pp = 100
# number of pages
import math
pgs = math.ceil(activities_total / activities_pp)

# columns to keep from activities
cols = ["id", "name", "distance", "moving_time", "elapsed_time", "total_elevation_gain", "type", "start_date_local", "map.id", "average_speed", "max_speed", "elev_high", "elev_low"]

pg_contents = []
for pg in range(pgs):
    if datetime.datetime.now() >= expires_at_date:
        print("Token outdated")
        break
    print("Page: {}".format(pg + 1))
    param = {'per_page': act_pp, 'page': pg + 1}
    try:
        pg_dataset = requests.get(activites_url, headers=header, params=param).json()
        #print(pg_dataset)
        pg_activities = json_normalize(pg_dataset)
    except:
        print("Problem accessing API")
        break
    pg_activities = pg_activities[cols]
    print("retrieved {} activities".format(pg_activities.shape[0]))
    print(pg_activities.head(5))
    pg_contents.append(pg_activities)

my_activities = pd.concat(pg_contents)
print("Total of {} activities retrieved".format(my_activities.shape[0]))


# Tagging paragliding activities (have ""#glidelytics" in their description)
my_workouts = my_activities[my_activities["type"] == "Workout"]

my_activities["paragliding"]  = False
my_activities["contains_hike"]  = False
my_activities["multiple_runs"]  = False

for index, row in my_workouts.iterrows():
    param = {'include_all_efforts' : "false"}
    url = activity_url + str(index)
    try:
        res = requests.get(url, headers=header, params=param).json()
    except:
        print("Problem getting activity {} details".format(row["id"]))
        break
    description = res["description"]
    print("Activity {}: description: {}".format(str(index), description))
    if description:
        if "#glidelytics" in description:
            my_activities.loc[index, ["paragliding"]] = True
            print("Tagged as paragliding")
        if "#contains_hike" in description:
            my_activities.loc[index, ["contains_hike"]] = True
            print("Tagged as containing hike")
        if "#multiple_runs" in description:
            my_activities.loc[index, ["multiple_runs"]] = True
            print("Tagged as multiple runs")

# store data in file
my_activities.to_csv("My_activities.csv")


# Data exploration
import seaborn as sns
sns.set_theme(style="ticks")

cols_to_analyze = ["distance", "moving_time", "elapsed_time", "total_elevation_gain", "average_speed", "max_speed", "elev_high", "elev_low", "paragliding"]
sns.pairplot(my_activities[cols_to_analyze], hue = "paragliding")

# Simple classifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier


cols_to_analyze = ["paragliding", "distance", "moving_time", "elapsed_time", "total_elevation_gain", "average_speed", "max_speed", "elev_high", "elev_low"]
dataset = my_activities[cols_to_analyze]
dataset = dataset.dropna()

X = dataset[cols_to_analyze]
X = StandardScaler().fit_transform(X)
y = dataset["paragliding"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state = 42)

print("Train set has {} activities".format(len(y_train)))
parag_activities = len([act for act in y_train if act == True])
print("Out of which {} are paragliding".format(parag_activities))

classifier = MLPClassifier(alpha = 1, max_iter = 1000)
classifier.fit(X_train, y_train)

print("Test set has {} activities".format(len(y_test)))
parag_activities = len([act for act in y_test if act == True])
print("Out of which {} are paragliding".format(parag_activities))
predictions = classifier.predict(X_test)
paragliding_non_tagged = 0
other_activity_tagged = 0
correctly_tagged = 0
y_test_array = [y for y in y_test]
for index in range(len(y_test_array)):
    if y_test_array[index] == False and predictions[index] == True:
        other_activity_tagged += 1
    elif y_test_array[index] == True and predictions[index] == False:
        paragliding_non_tagged +=1
    else:
        correctly_tagged += 1

print("Classifier did {} correct classifications".format(correctly_tagged))
print("A total of {} paragliding activities were not correctly tagged".format(paragliding_non_tagged))
print("A total of {} activities were wrongfully tagged as paragliding".format(other_activity_tagged))


score = classifier.score(X_test, y_test)
print("The calculated score of the classifier is {}".format(score))
