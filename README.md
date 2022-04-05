# Glidelytics
This project was created to analyze paragliding data stored on Strava.

Our aim is to first work on a PoC but later on to open the service to all.

The first phase of the project consists in authorizing and downloading activity data from Strava. The second phase will consist on proper tagging of paragliding activities. After that? We will see but the vision is ambitious!

## This code
Here we attempt to achieve a satisfactory labelling of paragliding activities in Strava. Other platforms such as Suunto have a paragliding record mode. The problem is these activities are not labeled as such when uploaded to Strava. Our first mission is to tag them correctly.

To train data, I have <b>manually tagged all of my paragliding ativities in Strava with a description #glidelytics</b>. Note that the tag is in description not on activity name nor comments (could had been coded that way as well).

This code hence:
- Downloads all the activities for an authorized athlete on Strava
- Filters the activities in which type is "Workout" (that's how strava labels my paragliding activities uploaded with Suunto). This is done to avoid overloading the API looking to get description for all activities (limit of 100 requests every 15 min)
- For each "Workout" activity, gets the field "description"
- If the description contains the "#glidelytics" tag, flag this activity as paragliding. This is used to train our classifier and check accuracy
- Runs exploratory analysis on the collected data using seaborn
- Develps a simple neural network classifier and checks its accuracy

## Running the notebook
- Clone or download the repository
- Follow the steps on Oauth authentication present in the notebook. Ressources can be found in the great [page](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde) written by Matt Ambrogi, and on Strava API [documentation](https://developers.strava.com/docs/authentication/). I struggled a bit to make these work at first for not understanding nor incorporating expiracy dates for tokens. The humble piece of code I wrote addresses the issues I found and has ran swiftly for API conversations so far for me
- On the installed folder, create a "config.ini" text file (or any other name if you change the script). Use the model given by the file "example_config.ini" and replace with the information from your generated Strava app.

## Running as script
For non Jypiter users I have created a script that runs, captures the above data, saves as CSV and run the analysis and classification. To use it however the authentication steps described in the jupyter notebook remain valid

## Results
I have 360 activities in Strava, out of which only 12 are paragliding so far. Hence I started this quite skeptical of the capability to harvest insights with such a reduced dataset. Therefore, please do let me know if you run this code?!

With the exploratory analysis we can see that the simple fields used by strava (time elapsed, distance, average speed, max speed, etc) do not allow for classification by a human. Paragliding speeds are similar to those of cycling; and the case is the same for all variables used. Therefore the classification with the 8 simple metrics is human impossible.

![exploratory analysis](https://user-images.githubusercontent.com/28501381/161739375-a55ab513-49fe-4c70-8f55-fa99a58a0a76.png)

Despite the limited data, and without performing any dimensionality reduction, we have tried to see how a classifier would perform. Without having performed any comparison, we decided to try out a neural network MLP classifier present in sklearn.
The results were surprising: the classifier performed perfectly for the dataset split at 40% for test.

<img width="533" alt="classifier result" src="https://user-images.githubusercontent.com/28501381/161739847-337b374d-a68f-4094-add3-95836303ab04.png">

## Next steps
We now need to look at a broader dataset to check the validity of the classifier. We aim at developing an app for that.
With the current data, the plan is to look at importance of the collected features and dimensionality reduction via PCA analysis.
