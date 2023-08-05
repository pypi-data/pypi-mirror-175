import customermerge.util as util
from google.cloud import bigquery


class LoadAvroToBigQuery:
    """
    :param schema: list of bigquery SchemaField objects
    :param project: str gcp project name
    :param dataset: str gcp bigquery dataset name: [PROJECT].[DATASET_NAME]
    :param customer: str name of business customer
    :param bucket: str gcp bucket name
    :param file_path: str file path: [gs://PATH]
    :param expiration: int minutes to expire
    :param query_cooler_update: str bq query merge
    :param query_erp_update: str bq query merge


    This class loads customer data from bucket/file into bigquery datasets \n
    steps: \n
    1. Make a random tmp table name. \n
    2. Define bq temp table structure with time expiration (bigquery schema). \n
    3. Get last avro file name (automatically). \n

    todo::
        The merge method do next functions:
            > Create temp table into dataset defined. \n
            > A bigquery is loading data until status it's done. \n
            > The query to merge customer data is executed. \n
            > The query to merge erp data is executed.


    """
    def __init__(self,
                 schema: list,
                 project: str,
                 dataset: str,
                 customer: str,
                 bucket: str,
                 file_path: str,
                 expiration: int,
                 query_cooler_update: str,
                 query_erp_update: str
                 ):
        super(LoadAvroToBigQuery, self).__init__()
        self.config = dict(project=project,
                           dataset=dataset,
                           customer=customer,
                           bucket=bucket,
                           file_path=file_path,
                           expiration=expiration)
        self.tmp_table_name = util.get_tmp_table_name(config=self.config)
        self.tmp_config = (self.tmp_table_name, schema, self.config)
        self.tmp_table_structure = util.get_bq_temp_table_def(config=self.tmp_config)
        self.avro_filename_from_bucket = util.get_last_avro_filename_from_bucket(config=self.config)
        self.query_heineken_merge_context = query_cooler_update.replace("<TEMP_TABLE>", self.tmp_table_name)
        self.query_erp_merge_context = query_erp_update
    
    def merge_data(self):
        # todo
        util.create_bq_tmp_table(client=bigquery.Client, tmp_table=self.tmp_table_structure)
        util.job_avro_load_to_bq_tmp_table(client=bigquery.Client,
                                           temp_table_name=self.tmp_table_name,
                                           file_path=self.config['file_path'],
                                           file_name=self.avro_filename_from_bucket)

        util.bq_exec_query(client=bigquery.Client,
                           query=self.query_heineken_merge_context,
                           src='merge_heineken_temp_table')

        util.bq_exec_query(client=bigquery.Client,
                           query=self.query_erp_merge_context,
                           src='merge_external_query_erp')