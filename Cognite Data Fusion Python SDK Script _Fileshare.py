
# Import Packages and Create Cognite Client Object -------------------------------------
from cognite.client.credentials import OAuthInteractive
from cognite.client import CogniteClient, ClientConfig

credentials = OAuthInteractive(
    authority_url=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_id=CLIENT_ID,
    scopes=[f"{BASE_URL}/.default"],
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

# Retrieve and Delete Files from Dataset -------------------------------------------------
dataset_name = "src:005:file-ep:b60:ds"
dataset_id = 6564460084991866
dataset = client.data_sets.retrieve(id=dataset_id)
print(dataset)
# Retrieve all files in the dataset
files = client.files.list(limit=20000,data_set_ids=dataset.id)
print(files)
# Delete each file
for file in files:
    client.files.delete(id=file.id)
print("All files from the dataset have been deleted.")

# Function to Clear Raw Explorer Tables Data ---------------------------------------------
database_name = "src:005:file-ep:b60:db:state"
table_name = "FileShare-EP_StateStore"
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