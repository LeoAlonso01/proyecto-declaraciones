import boto3
from botocore.exceptions import ClientError
import os

# credenciales de AWS desde el archivo .env
AWS_SECRET_ID_KEY = os.getenv("AWS_SECRET_ID_KEY")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# credenciales de AWS
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_SECRET_ID_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name='us-east-1'
    )

# nombre del bucket
BUCKET_NAME = 'nombramientos-bucket'