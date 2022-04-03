# Glidelytics
This project was created to analyze paragliding data stored on Strava.

Our aim is to first work on a PoC but later on to open the service to all.

The first phase of the project consists in authorizing and downloading activity data from Strava. The second phase will consist on proper tagging of paragliding activities. After that? We will see but the vision is ambitious!

## This notebook
Here we attempt to achieve a satisfactory labelling of paragliding activities in Strava. Other platforms such as Suunto have a paragliding record mode. The problem is these activities are not labeled as such when uploaded to Strava. Our first mission is to tag them correctly.

To train data, I have manually tagged all of my paragliding ativities in Strava with a comment #glidelytics. The plan is to identify them to subsequently run analysis for labeling.

## running this notebook
- Clone or download the repository
- Create a Strava app and get the client_id, client_secret and refresh_code. Details can be found in the great [page](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde) written by Matt Ambrogi, and on Strava API [documentation](https://developers.strava.com/docs/authentication/)
- On the installed folder, create a "config.ini" text file (or any other name if you change the script). Use the model given by the file "example_config.ini" and replace with the information from your generated Strava app.
