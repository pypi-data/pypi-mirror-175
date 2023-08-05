# Hepsiburada Data Science Utilities

This module includes utilities for Hepsiburada Data Science Team.

- Library is available via PyPi. 
- Library can be downloaded using pip as follows: `pip install heps-ds-utils`
- Existing library can be upgraded using pip as follows: `pip install heps-ds-utils --upgrade`

***
## Available Modules

1. Hive Operations

```python
from heps_ds_utils import HiveOperations

# A connection is needed to be generated in a specific runtime.
# There are 3 ways to set credentials for connection.

# 1) Instance try to set default credentials from Environment Variables.
hive_ds = HiveOperations()
hive_ds.connect_to_hive()

# 2) One can pass credentials to instance initiation to override default.
hive_ds = HiveOperations(HIVE_HOST="XXX", HIVE_PORT="YYY", HIVE_USER="ZZZ", HIVE_PASS="WWW", HADOOP_EDGE_HOST="QQQ")
hive_ds = HiveOperations(HIVE_USER="ZZZ", HIVE_PASS="WWW")
hive_ds.connect_to_hive()

# 3) One can change any of the credentials after initiation using appropriate attribute.
hive_ds = HiveOperations()
hive_ds.hive_username = 'XXX'
hive_ds.hive_password = 'YYY'
hive_ds.connect_to_hive()

# Execute an SQL query to retrieve data.
# Currently Implemented Types: DataFrame, Numpy Array, Dictionary, List.
SQL_QUERY = "SELECT * FROM {db}.{table}"
data, columns = hive_ds.execute_query(SQL_QUERY, return_type="dataframe", return_columns=False)

# Execute an SQL query to create and insert data into table.
SQL_QUERY = "INSERT INTO .."
hive_ds.create_insert_table(SQL_QUERY)

# Send Files to Hive and Create a Table with the Data.
# Currently DataFrame or Numpy Array can be sent to Hive.
# While sending Numpy Array columns have to be provided.
SQL_QUERY = "INSERT INTO .."
hive_ds.send_files_to_hive("{db}.{table}", data, columns=None)

# Close the connection at the end of the runtime.

hive_ds.disconnect_from_hive()

```

2. BigQuery Operations

```python
from heps_ds_utils import BigQueryOperations, execute_from_bq_file

# A connection is needed to be generated in a specific runtime.
# There are 3 ways to set credentials for connection.

# 1) Instance try to set default credentials from Environment Variables.
bq_ds = BigQueryOperations()

# 2) One can pass credentials to instance initiation to override default.
bq_ds = BigQueryOperations(gcp_key_path="/tmp/keys/ds_qos.json")

# Unlike HiveOperations, initiation creates a direct connection. Absence of
# credentials will throw an error.

# Execute an SQL query to retrieve data.
# Currently Implemented Types: DataFrame.
QUERY_STRING = """SELECT * FROM `[project_name].[dataset_name].[table_name]` LIMIT 20"""
data = bq_ds.execute_query(QUERY_STRING, return_type='dataframe')

# Create a Dataset in BigQuery.
bq_ds.create_new_dataset("example_dataset")

# Create a Table under a Dataset in BigQuery.
schema = [
    {"field_name": "id", "field_type": "INTEGER", "field_mode": "REQUIRED"},
    {"field_name": "first_name", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "last_name", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "email", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "gender", "field_type": "STRING", "field_mode": "REQUIRED"},
    {"field_name": "ip_address", "field_type": "STRING", "field_mode": "REQUIRED"}]

bq_ds.create_new_table(dataset='example_dataset', table_name='mock_data', schema=schema)

# Insert into an existing Table from Dataframe.
# Don't create and insert in the same runtime.
# Google throws an error when creation and insertion time is close.
bq_ds.insert_rows_into_existing_table(dataset='example_dataset', table='mock_data', data=df)

# Delete a Table.
bq_ds.delete_existing_table('example_dataset', 'mock_data')

# Delete a Dataset.
# Trying to delete a dataset consisting of tables will throw an error.
bq_ds.delete_existing_dataset('example_dataset')

# Load Dataframe As a Table. BigQuery will infer the data types.
bq_ds.load_data_to_table('example_dataset', 'mock_data', df, overwrite=False)

# To execute BQ commands sequentially from a BigQuery Script without a return statement !
execute_from_bq_file(bq_client=bq_ds, bq_file_path="tests/test_data/test_case_2.bq", verbose=True)

```

3. Logging Operations

```python
from heps_ds_utils import LoggingOperations

# A connection is needed to be generated in a specific runtime.
# There are 3 ways to set credentials for connection.

# 1) Instance try to set default credentials from Environment Variables.
logger_ds = LoggingOperations()

# 2) One can pass credentials to instance initiation to override default.
logger_ds = LoggingOperations(gcp_key_path="/tmp/keys/ds_qos.json")

# Unlike HiveOperations, initiation creates a direct connection. Absence of
# credentials will throw an error.


```

4. Bucket Operations

```python
from heps_ds_utils import BucketOperations

# A connection is needed to be generated in a specific runtime.
# There are 2 ways to set credentials for connection.

# 1) Instance try to set default credentials from Environment Variables.
bct_ds = BucketOperations()

# 2) One can pass credentials to instance initiation to override default.
bct_ds = BucketOperations(gcp_key_path="/tmp/keys/ds_qos.json")

# Unlike HiveOperations, initiation creates a direct connection. Absence of
# credentials will throw an error.

BUCKET_NAME = "bucket-name"

# Upload File using filepath.
# Blob name is the filepath you want the file to be under the bucket.
# Filepath is the path to the file you want to upload.
bct_ds.upload_from_filepath(BUCKET_NAME, "project_name/dev/data/output.csv", "data/output.csv")

# Upload File from memory data.
# If you want to save the data in memory to a file, you can use this function.
bct_ds.upload_from_memory(BUCKET_NAME, "project_name/dev/model/model.pkl", model)

# Download file from bucket to filepath.
bct_ds.download_to_filepath(BUCKET_NAME, "project_name/dev/data/sample.json", "data/sample.json")

# Download data from bucket to memory.
# If you want to save the data in a file to memory, you can use this function.
frame = bct_ds.download_to_memory(BUCKET_NAME, "project_name/dev/data/sample.csv", "dataframe")

# Delete file from bucket.
bct_ds.delete_file_from_bucket(BUCKET_NAME, "project_name/dev/data/sample.json")

# Create empty folder to bucket.
bct_ds.create_new_folders(BUCKET_NAME, "project_name/dev/data/")

```

Release Notes:

0.4.4:
- BigQueryOperations:
    - insert_rows_into_existing_table: insertion exception handling added.
    - insert_rows_into_existing_table: retry added. 
        - Put time between table creation and insertion.
    - execute_query: total_bytes_processed info added.
    - execute_query: max allowed total_bytes_processed set to 100GB.
    - execute_query: return_type=None for Queries w/o any return.
    - load_data_to_table: kwargs['overwrite'] is added.
        - load_data_to_table(..., overwrite=True) to overwrite to table.
        - load_data_to_table(..., overwrite=False) to append to table.
        - not passing overwrite kwarg will print a DeprecationWarning.
    - execute_from_bq_file: sequential execution of BigQuery commands from
    a file. It has its own parser. 
        - execute_from_bq_file(..., verbose=True) to print BigQuery commands to console.
        - execute_from_bq_file(..., verbose=False) not to print BigQuery commands to console.

0.4.5:
- LoggingOperations
    - Bug Fix in Authentication to GCP Logging !
- BigQueryOperations
    - Executing BQ files for different environments !

0.4.6:
- BigQueryOperations
    - BQ Parser bug fix !
    - BQ File Execution dependent queries
        - Some of the queries depends on the previous command executions. For these cases:
        dependent_queries is needed to be set to True !
        execute_from_bq_file(
            bq_ds,
            "tests/test_data/test_case_4.bq",
            verbose=True,
            config=configs,
            dependent_queries=True)
    - BQ Create Table Results in Empty Table Check Added!
        - Raises an error if CREATE TABLE ... SELECT AS ... query results in empty table.
        - This doesn't work in the case of dependent_queries=True !!!
    - 100GB limit is turned into a warning, which will not be displayed in prod env.
    - BQ Return Types Implemented (Numpy Array and Arrow Formats)
- LoggingOperations
    - protobuf dependency issue resolved!
- BucketOperations
    - upload_from_filepath function added.
    - upload_from_memory function added.
    - download_to_filepath function added.
    - download_to_memory function added.
    - delete_file_from_bucket function added.
    - create_new_folders function added.
    - delete_folder function added.
