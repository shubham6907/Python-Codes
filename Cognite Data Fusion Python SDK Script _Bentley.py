
# Import Packages and Create Cognite Client Object -------------------------------------
from cognite.client.credentials import OAuthClientCredentials
from cognite.client import CogniteClient, ClientConfig

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

# Function to Clear Raw Explorer Tables Data ---------------------------------------------
def clear_table_data(database_name,table_name):
    # Retrieve all rows from the specified table
    rows = client.raw.rows.list(database_name, table_name, limit=20000)
    for row in rows:
        # Delete each row
        print(row)
        key = str(row.key)
        print(key)
        client.raw.rows.delete(database_name,table_name,key)
        print(f"Deleted row with ID: {row.key}")
    print(f"All rows from table '{table_name}' have been deleted.")

# Pass Database Name and Table Name Values to the Function ------------------------------
database_name = "src:002:bentley:db"
table_name = "rca_project_tasks_bentley_prod"
clear_table_data(database_name,table_name)

# Function to Delete Single Row From Raw Explorer Tables --------------------------------
def delete_table_row(database_name_new,table_name_new,row_key):
    client.raw.rows.delete(database_name_new,table_name_new,row_key)
    print("state store row is deleted.")

# Pass Database Name, Table Name and Row Key Values to the Function ---------------------
database_name_new = "src:002:bentley:db:state"
table_name_new = "bentley_state"
row_key = "bentley_RCA_Project_Tasks_query_0010_prod"
delete_table_row(database_name_new,table_name_new,row_key)

