# 311Services
Python + SQLite data flow and analysis of NYC OpenData 311 Service Requests

In this repository, you will find the following files that meet the Deliverables outlined in this technical:

-311_import_and_analysis.py: This contains both the script to build the SQLite tables and the script that runs the analysis for my five questions. I built and tested the code in my Jupyter Notebook and moved it into this .py file as I progressed, saving and pushing my changes as I went. This file has the same contents as my .ipynb file, but it contains version history for review

-analysis.ipynb: This is the same as my 311_import_and_analysis.py file, but I recommend using it because of the capabilities included in Jupyter notebooks

---------------------------------------------------------------

Instructions for execution:

-I import multiple extensions that are utilized throughout my code at the start. The following should be run on your terminal to ensure you have the proper installations to use these packages (this can also be found in requirements.txt:
  -pip install [fill in]

-Now you can run the 311_import_and_analysis.ipynb file

-This will pull data from the trailing ~13 months from the NYC OpenData 311 Service Requests 2010 to present online database. After it is run the first time, it can be run again to pull any data that has a created_date after the maximum created_date of the previous pull or a resolution_action_updated_date greater than the maximum created_date of the previous pull

-To aid in data normalization, agency_name is not included in the store_311_service_requests table and is instead in store_311_agencies table, along with agency (additional data normalization opportunity called out below)

-Five questions are found at the bottom, with the first 3 being answered with SQL and the last 2 being answered with Python. The questions are each in their own code block within the Jupyter Notebook, and their outputs are displayed below their respective code blocks. If running from the .py file, the outputs for each question are printed in order, and a chart is produced as a figure for question five. See each question below:
  
  -Q1: How many service requests are status = closed with no resolution or status <> closed with a resolution, and is it concentrated on any particular agency?
    This question helps to identify service requests that should be updated, as their values do not align with each other
  
  -Q2: How many service requests are there with status = closed and no closed date, or status <> closed and have a closed date, and is it concentrated on any particular agency?
    This question helps to identify service requests that should be updated, as their values do not align with each other
  
  -Q3: Which Agency has the most non-closed service requests, and of the non-closed, how many are unspecified or open?
    This question helps identify agencies that are lacking in closing their service requests
  
  -Q4: On average how long does it take from created_date to closed_date by agency?
    This question helps identify agencies that are leaving service requests open for too long
  
  -Q5: How many service requests come per month, per borough, and does one borough stand out?
    This question identifies which boroughs receive the most service requests, and if there are any jumps for a particular month

---------------------------------------------------------------

-311_Service_Requests selection: This database was easily accessible and had a lot of information to utilize. There was an opportunity for data normalization through the agency and agency_name fields. Also, there seemed to be an opportunity for questions that could target particular agencies or boroughs for service request records that should be updated

---------------------------------------------------------------

See below a screenshot of the table relationships I set up:
<img width="913" height="720" alt="image" src="https://github.com/user-attachments/assets/57b76b0d-a219-4bd7-a328-c5fdcbfd703c" />


---------------------------------------------------------------

Additional opportunities given more time:

-Further data normalization: other fields could have been pulled from the main service requests table and put into separate lookup tables, but they would have needed manipulation, particularly where a child was NULL across multiple parents. I saw an opportunity for additional normalization through the location-based fields (e.g. address, street name, city, borough, and lat/long). Similarly, the complaint type and descriptor could have been extracted in a similar manner to agency and agency_name.

-Better trailing 13 months definition: I selected trailing 13 months to have a full 12 months of data + the current month of data. The current methodology to get 13 months is to subtract (13 * 30) days from today. I would like to change this to use months instead of days.
