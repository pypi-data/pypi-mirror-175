# customermerge

This library was developed by the technology consulting company EmeralDigital.

Usage

```python	
import customermerge as load
from google.cloud import bigquery

schema = list(bigquery.SchemaField("NAME", "STRING", mode="REQUIRED")) # list: bigquery SchemaField objects
project = "PROJECT_NAME" # str: gcp project name
dataset = "DATASET_NAME" # str: gcp bigquery dataset name: [PROJECT].[DATASET_NAME]
customer = "CUSTOMER_NAME" # str: name of business customer
bucket = "BUCKET_NAME" # str: gcp bucket name
file_path = "gs://BUCKET_PATH/FOLDER/..." # str: This is the path of the avro file to read
expiration = 30 # int: The time in minutes at which the temporary table will expire
query_cooler_update = """
                        MERGE [DATASET] a
                        USING [TEMP_TABLE] b --new data sent by customer stored into this temp table
                            ON a.key=b.key
                        WHEN MATCHED THEN
                            UPDATE SET a.field = b.field
                        WHEN NOT MATCHED THEN
                            INSERT(field_1, field_2)
                    """ # str: this query do upsert to own customer data
query_erp_update = """
                        MERGE [DATASET] a
                        USING [DATASET] b --Here we used a EXTERNAL_QUERY where erp data is
                            ON a.key=b.key
                        UPDATE SET a.field1 = b.field1, a.field2=b.field2
 """ # str: In this case we do not use a insert cause de update is only over matched key

loading = load.LoadAvroToBigQuery(schema=schema,
                                  project=project,
                                  dataset=dataset,
                                  customer=customer,
                                  bucket=bucket,
                                  file_path=file_path,
                                  expiration=expiration,
                                  query_cooler_update=query_cooler_update,
                                  query_erp_update=query_erp_update)
loading.merge_data()
```
