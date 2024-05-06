
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

# Deletion of Files Using ID -------------------------------------------------------------
client.files.delete(id=1523517114957616)
client.files.delete(id=7900216178498015)

# Deletion of Raw Explorer Table Rows Using Key ------------------------------------------
database_name = "src:006:documentum:b60:db"
table_name = "metadata_documentum"
client.raw.rows.delete(database_name,table_name,"DM09002b678014e6d9:docx")
client.raw.rows.delete(database_name,table_name,"DM09002b678014e6d9:pdf")

# Retrieve Files from Dataset using API --------------------------------------------------
dataset_name = "src:005:file-ep:b60:ds"
dataset_id = 6581557552959954

dataset = client.data_sets.retrieve(id=dataset_id)
print(dataset)
files = client.files.list(limit=20000,data_set_ids=dataset.id)
print(files)

# Delete Retrived Files in Loop ----------------------------------------------------------
for file in files:
    client.files.delete(id=file.id)
print("All files from the dataset have been deleted.")

# Function to Clear Raw Explorer Tables Data ---------------------------------------------
database_name = "src:006:documentum:b60:db"
table_name = "metadata_documentum"
rows = client.raw.rows.list(database_name, table_name, limit=20000)
for row in rows:
    # Delete each row
    print(row)
    key = str(row.key)
    print(key)
    client.raw.rows.delete(database_name,table_name,key)
    print(f"Deleted row with ID: {row.key}")
print(f"All rows from table '{table_name}' have been deleted.")

