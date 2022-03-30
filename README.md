# stravaGliding
This project was created to analyse paragliding data stored on Strava.

Our aim is to first work on a PoC but later on to open the service to all.

The first phase of the project consists in authorizing and downloading activity data from Strava. The second phase will consist on proper tagging of paragliding activities. After that? We will see but the vision is ambitious!

## running the notebook
- Clone or download the repository
- Create a Strava app and get the client_id, client_secret and refresh_code. Details can be found in the great [page](https://towardsdatascience.com/using-the-strava-api-and-pandas-to-explore-your-activity-data-d94901d9bfde) written by Matt Ambrogi, and on Strava API [documentation](https://developers.strava.com/docs/authentication/) 
- On the installed folder, create a "config.ini" text file (or any other name if you change the script). Add the above variables to the file in the form key:value
