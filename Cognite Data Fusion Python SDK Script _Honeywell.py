
# Import Packages and Create Cognite Client Object -------------------------------------
from cognite.client.credentials import OAuthClientCredentials
from cognite.client import CogniteClient, ClientConfig
import pandas as pd
import openpyxl
from datetime import datetime, timedelta

credentials = OAuthClientCredentials(
    token_url=f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token", 
    client_id=CLIENT_ID, 
    scopes=[f"{BASE_URL}/.default"], 
    client_secret= CLIENT_SECRET
)
config = ClientConfig(
    client_name="Cognite Academy course taker",
    project=COGNITE_PROJECT,
    base_url=BASE_URL,
    credentials=credentials,
)
client = CogniteClient(config)

# Perform Some Simple API Calls using Cognite Client -------------------------------------
print(client)
print(client.data_sets.list())
print(client.files.list(limit=5))

# Fuction to Delete Empty Timeseries -----------------------------------------------------
dataset_name = "src:003:honeywell:ds"
dataset_id = 1960039874814037
time_series_filter = {'datapoints': {'max': 0}}
timeseries = client.time_series.list(filter=time_series_filter, limit=10000, )
for ts in timeseries:
    print(f"Empty Time Series: {ts.name}, ID: {ts.id}")
for timeseries1 in timeseries:
    client.time_series.delete(id=[timeseries1.id])
print("Deleted timeseries")

# Delete Asset ---------------------------------------------------------------------------
client.assets.delete(external_id='HWPHD:http://opcfoundation.org/UA/:i=85', recursive=True)
print("Deleted asset")

# Retrieve All Timeseries ----------------------------------------------------------------
all_time_series = client.time_series.list(limit=10000)

# Create Empty List and Data Frames ------------------------------------------------------
empty_time_series = []
final_df = pd.DataFrame()
final_df2 = pd.DataFrame()

# Generate Analysis Report 1 -------------------------------------------------------------
for ts in all_time_series:
    # Retrieve the number of data points for each time series
    data_points = client.time_series.data.retrieve(id=ts.id, aggregates=['count'], granularity='1d').aggregates[0].count
    # Check if the time series has zero data points
    if data_points == 0:
        empty_time_series.append(ts)

    granularity = '365d'
    datapoints = len(client.time_series.data.retrieve(id=ts.id))
    
    datapoints = client.time_series.data.retrieve(id=ts.id)
    print(type(datapoints))
    df = pd.DataFrame(datapoints.to_pandas())
    df = df.reset_index()
    new_column_name = 'Timestamp'
    df.rename(columns={df.columns[0]: new_column_name}, inplace=True)
    print(df)
    current_date = datetime.now()
    days_ahead = current_date + timedelta(days=1)
    if df['Timestamp'].max() > current_date:
        print(f"Future Time Series: {ts.name}, ID: {ts.id}, External ID: {ts.external_id}")
        new_row = {'NodeName': [ts.name,], 'TimeseriesId': [ts.id,], 'TimeseriesExternalId': [ts.external_id,]}
        new_df = pd.DataFrame(new_row)
        final_df = pd.concat([final_df, new_df]).sort_index(ignore_index=True)
print(final_df)
excel_file_path = 'TimeseriesWithFutureDatapoints.xlsx'
# Export the DataFrame to Excel
final_df.to_excel(excel_file_path, index=False)
print(f'DataFrame exported to {excel_file_path}')

# Generate Analysis Report 2 -------------------------------------------------------------
for ts in all_time_series:   

    datapoints = client.time_series.data.retrieve(id=ts.id)
    print(type(datapoints))
    df = pd.DataFrame(datapoints.to_pandas())
    df = df.reset_index()
    new_column_name = 'Timestamp'
    df.rename(columns={df.columns[0]: new_column_name}, inplace=True)
    print(df)
    current_date = datetime.now()

    days_ago = current_date - timedelta(days=1)
    if df['Timestamp'].max() <= days_ago:
        print(f"24 hours old Time Series: {ts.name}, ID: {ts.id}, External ID: {ts.external_id}")
        new_row = {'NodeName': [ts.name,], 'TimeseriesId': [ts.id,], 'TimeseriesExternalId': [ts.external_id,]}
        new_df = pd.DataFrame(new_row)
        final_df = pd.concat([final_df, new_df]).sort_index(ignore_index=True)
    
    hours_ago = current_date - timedelta(hours=6)
    if df['Timestamp'].max() <= hours_ago:
        print(f"6 hours old Time Series: {ts.name}, ID: {ts.id}, External ID: {ts.external_id}")
        new_row2 = {'NodeName': [ts.name,], 'TimeseriesId': [ts.id,], 'TimeseriesExternalId': [ts.external_id,]}
        new_df2 = pd.DataFrame(new_row2)
        final_df2 = pd.concat([final_df2, new_df2]).sort_index(ignore_index=True)
        
print(final_df)
print(final_df2)

excel_file_path = 'TimeseriesWithOldDatapoints.xlsx'
with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, sheet_name='24HoursOld', index=False)
    final_df2.to_excel(writer, sheet_name='6HoursOld', index=False)

