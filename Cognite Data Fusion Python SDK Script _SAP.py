
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

# Function to Clear Raw Explorer Tables Data in Chunks ------------------------------------
def clear_table_data(database_name, table_name):
    keys_list = []

    def retrieve_table_data(database_name,table_name):
        # Retrieve all rows from the specified table
        rows = client.raw.rows.list(database_name, table_name, limit=1000000)
        for row in rows:
            key = str(row.key)
            keys_list.append(key)
        print("total number of rows available in table {} are {}".format(table_name,len(keys_list)))

    def chunk_list(lst, chunk_size):
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    def delete_table_data(database_name, table_name, chunk):
        client.raw.rows.delete(database_name, table_name, chunk)
        print("chunk of rows deleted from table {}".format(table_name))

    retrieve_table_data(database_name,table_name)
    chunk_size = 20000
    key_chunks = chunk_list(keys_list, chunk_size)
    for chunk in key_chunks:
        delete_table_data(database_name, table_name, chunk)
    print("{} table data cleared successfully".format(table_name))

database_name = "src:001:sap:db"
table_names_list = ["EQST_Equipment_To_BoM_Link_B60_EP", 
                    "Equipment_Master_B60_EP", 
                    "Functional_Locations_B60_EP", 
                    "Maintenance_Schedule_B60_EP"]

for table_name in table_names_list:
    clear_table_data(database_name, table_name)
