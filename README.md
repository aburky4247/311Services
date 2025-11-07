# 311Services
Python + SQLite data flow and analysis of NYC OpenData 311 Service Requests

In this repository, you will find the following files that meet the Deliverables outlined in this technical:
-311_import_and_analysis.py: This contains both the script to build the SQLite tables and the script that runs the analysis for my five questions. I built and tested the code in my Jupyter Notebook and moved it into this .py file as I progressed, saving and pushing my changes as I went. This file has the same contents as my .ipynb file, but it contains version history for review
-311_import_and_analysis.ipynb: This is the same as my .py file, but I recommend using it because of the capabilities included in Jupyter notebooks

Instructions for execution:
-I import multiple packages that are utilized throughout my code at the start. The following should be run on your terminal to ensure you have the proper installations to use these packages:
  -pip install [fill in]
-Now you can run the 311_import_and_analysis.ipynb file
-This will pull data from the trailing ~13 months from the NYC OpenData 311 Service Requests 2010 to present online database. After it is run the first time, it can be run again to pull any data that has a created_date after the maximum created_date of the previous pull or a resolution_action_updated_date greater than the maximum created_date of the previous pull
-In order to aid in data normalization, agency_name is not included in the store_311_service_requests table and is instead in store_311_agencies table, along with agency (additional data normalization opportunity called out below)
-Five questions are found at the bottom, with the first 3 being answered with SQL and the last 2 being answered with Python. See these questions below:
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

