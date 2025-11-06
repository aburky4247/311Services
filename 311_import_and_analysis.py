import pandas as pd
import requests as req
import sqlite3 as sq
from io import StringIO
from datetime import datetime, timedelta
from time import sleep

pd.set_option('display.max_columns', None)

BASE_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"

DB = "nyc_311_data_ab.db"

BATCH_SIZE = 50000

conn = sq.connect(DB)
cursor = conn.cursor()

# COMMENTED CODE BELOW WILL DELETE ALL HISTORICAL DATA only run if you want this to run as if its running for the first time
# cursor.execute("""DROP TABLE IF EXISTS store_311_service_requests""")
# cursor.execute("""DROP TABLE IF EXISTS store_311_agencies""")

# raw_311_service_requests drop existing table then create new table
cursor.execute("""DROP TABLE IF EXISTS raw_311_service_requests""")

cursor.execute("""CREATE TABLE raw_311_service_requests (
    unique_key TEXT PRIMARY KEY,
    created_date TEXT,
    closed_date TEXT,
    agency TEXT,
    agency_name TEXT,
    complaint_type TEXT,
    descriptor TEXT,
    location_type TEXT,
    incident_zip TEXT,
    incident_address TEXT,
    street_name TEXT,
    cross_street_1 TEXT,
    cross_street_2 TEXT,
    intersection_street_1 TEXT,
    intersection_street_2 TEXT,
    address_type TEXT,
    city TEXT,
    landmark TEXT,
    facility_type TEXT,
    status TEXT,
    due_date TEXT,
    resolution_description TEXT,
    resolution_action_updated_date TEXT,
    community_board TEXT,
    bbl TEXT,
    borough TEXT,
    x_coordinate_state_plane TEXT,
    y_coordinate_state_plane TEXT,
    open_data_channel_type TEXT,
    park_facility_name TEXT,
    park_borough TEXT,
    vehicle_type TEXT,
    taxi_company_borough TEXT,
    taxi_pick_up_location TEXT,
    bridge_highway_name TEXT,
    bridge_highway_direction TEXT,
    road_ramp TEXT,
    bridge_highway_segment TEXT,
    latitude REAL,
    longitude REAL,
    location TEXT
);
""")

# store_311_service_requests table creation if not already existing (only activates on first run)
cursor.execute("""
CREATE TABLE IF NOT EXISTS store_311_service_requests (
    unique_key TEXT PRIMARY KEY,
    created_date TEXT,
    closed_date TEXT,
    agency TEXT,
    complaint_type TEXT,
    descriptor TEXT,
    location_type TEXT,
    incident_zip TEXT,
    incident_address TEXT,
    street_name TEXT,
    cross_street_1 TEXT,
    cross_street_2 TEXT,
    intersection_street_1 TEXT,
    intersection_street_2 TEXT,
    address_type TEXT,
    city TEXT,
    landmark TEXT,
    facility_type TEXT,
    status TEXT,
    due_date TEXT,
    resolution_description TEXT,
    resolution_action_updated_date TEXT,
    community_board TEXT,
    bbl TEXT,
    borough TEXT,
    x_coordinate_state_plane TEXT,
    y_coordinate_state_plane TEXT,
    open_data_channel_type TEXT,
    park_facility_name TEXT,
    park_borough TEXT,
    vehicle_type TEXT,
    taxi_company_borough TEXT,
    taxi_pick_up_location TEXT,
    bridge_highway_name TEXT,
    bridge_highway_direction TEXT,
    road_ramp TEXT,
    bridge_highway_segment TEXT,
    latitude REAL,
    longitude REAL,
    location TEXT
);
""")


# store_311_agencies table creation if not already existing (only activates on first run)
cursor.execute("""
CREATE TABLE IF NOT EXISTS store_311_agencies (
    agency TEXT,
    agency_name TEXT,
    FOREIGN KEY (agency) REFERENCES store_311_service_requests(agency)
);
""")

conn.commit()

# find max_created_date and max_resolution_action_updated date to use as an iterative ETL process for pulling data in the future


def get_max_dates():
    """Retrieve latest created/resolution dates from store table."""
    try:
        result = pd.read_sql_query("""
        SELECT 
        MAX(created_date)                       AS max_created_date,
        MAX(resolution_action_updated_date)     AS max_resolution_action_updated_date
        FROM store_311_service_requests;""", conn)
        max_created = result.loc[0, "max_created_date"]
        max_resolution = result.loc[0, "max_resolution_action_updated_date"]
        return max_created, max_resolution
    except Exception:
        return None, None


max_created_date, max_resolution_date = get_max_dates()

# create where_clause to only pull data with a created_date >= max_created_date OR resolution_action_updated_date >= max_resolution_action_updated_date
# if max_resolution_date and max_created_date don't exists (i.e store table empty because this is the first run), then pull trailing 13 months
end_date = datetime.now()
start_date = end_date - timedelta(days=13*30)  # changed from days=13 * 30

if max_created_date or max_resolution_date:
    filters = []
    if max_resolution_date:
        filters.append(
            f"resolution_action_updated_date >= '{max_resolution_date}'")
    if max_created_date:
        filters.append(f"created_date >= '{max_created_date}'")
    where_clause = " OR ".join(filters)
    print(f"🔁 Incremental pull:\n{where_clause}")
else:
    where_clause = (
        f"created_date between '{start_date.strftime('%Y-%m-%dT00:00:00')}' "
        f"and '{end_date.strftime('%Y-%m-%dT23:59:59')}'"
    )
    print(f"Initial pull for last 13 months:\n{where_clause}")

# pull data in batches defined by batch size set at beginning and give response on failure


def fetch_311_batch(offset=0, limit=BATCH_SIZE):
    params = {
        "$limit": limit,
        "$offset": offset,
        "$where": where_clause
    }
    response = req.get(BASE_URL, params=params)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        print(f"Failed batch (HTTP {response.status_code})")
        return pd.DataFrame()

# define import_to_raw using fetch_311_batch and keep pulling data until fetch_311_batch is empty (i.e. failed or where_clause prevented any data from being pulled)


def import_to_raw():

    offset = 0
    total_rows = 0

    while True:
        df = fetch_311_batch(offset)
        if df.empty:
            break

        df.to_sql('raw_311_service_requests', conn,
                  if_exists="append", index=False)
        total_rows += len(df)

        offset += BATCH_SIZE
        sleep(1)

    print(f"Loaded {total_rows:,} total rows into 'raw_311_service_requests'")


import_to_raw()
