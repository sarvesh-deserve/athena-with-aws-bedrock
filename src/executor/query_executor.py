import time
import uuid

import boto3
import pandas as pd

athena = boto3.client(service_name="athena")
s3 = boto3.client(service_name="s3")


class QueryExecutor:

    @staticmethod
    def execute_sql(query: str, report_id):
        bucket_name: str = "sandbox-data-query-service"
        result_bucket: str = f"s3://{bucket_name}/"
        report_location: str = f"{result_bucket}{report_id}"

        response = athena.start_query_execution(
            QueryString=query,
            ClientRequestToken=report_id,
            QueryExecutionContext={
                "Database": "sandbox_payments",
                "Catalog": "AwsDataCatalog",
            },
            ResultConfiguration={"OutputLocation": report_location},
            WorkGroup="primary",
        )

        time.sleep(5)

        obj = s3.get_object(
            Bucket=bucket_name, Key=f"{report_id}/{response['QueryExecutionId']}.csv"
        )
        data = pd.read_csv(obj["Body"])
        data.fillna("", inplace=True)

        return data
