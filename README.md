# sqlalchemy-challenge

## Module 10 Challenge

For this challenge, I analyzed the climate database of Honolulu, Hawaii ahead of a holiday vacation. Using SQLAlchemy and Flask with Python, I performed climate analysis and created a Flask API with the queries performed.

### Analyze and Explore Climate Data
For this section, I performed an analysis on the precipitation and station data of Honolulu from the database. I begin by importing the dependencies needed, creating the engine and Base components to connect to the SQLite database, and saved references to both tables, before initialzing my session to the database for querying.

For precipitation, I found the most recent date in the dataset and used it to calculate the previous 12 months of data with the datetime module. In particular, I queried the database for the date and prcp (or precipitation) columns within this time frame. After, I loaded the results into a Pandas DataFrame, sorted it by the date, and plotted the results for precipitation (in inches) across the last year of data.

For stations, I found the total number of stations (9) and then found the most-active stations by querying based on observation counts. I found that Station USC00519281 (WAIHEE 837.5, HI US) had the most observations with 2,772. I then found the minimum, maximum, and average temperatures for this station across the entire dataset. Finally, I queried the dataset for the previous 12 months of temperature data for this particular station, and plotted a histogram for the frequency of temperatures for that time frame. Finally, I closed the session at the end of the notebook.


### Climate App

For this section, I created a Flask API that routes to different query results calculated from the previous section. All of the functions return the data using jsonify for a better visual output.

Before the routes, I created a few functions and variables that would be used in multiple routes. I calculated the last year of data using the same method from the previous section. I also defined a function to convert a tuple into a list, which is necessary to ensure query results are able to be read by jsonify. Finally, I created a function that converts the date from the dynamic routes into a datetime object to be used for querying.

On the homepage, I introduced the Flask API and listed the available routes. I made sure to include how the dates for the dynamic routes should be formatted.

For the precipitation route, I queried the database for the last 12 months of data and returned a dictionary of dates and precipitation.

For the stations route, I queried the database for a tuple of each station ID. I converted it into a list before returning it.

For the tobs route, I found the station with the most activity and queried the database for that station's temperatures across the last 12 months of data. I converted it into a dictionary and returned the results.

For the start and start/end dynamic routes, I defined the functions to accept the specified dates from the route as parameters. For the start route, the query returns the minimum, maximum, and average temperates for dates greater than or equal to the start date. For the start/end route, the query provides the same temperature statistics for dates from the start date to the end date, inclusive. Both routes' results are converted into a list and returned in a dictionary.