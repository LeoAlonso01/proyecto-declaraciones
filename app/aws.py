import boto3
from botocore.exceptions import ClientError

# credenciales de AWS
s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAU72LF6GUUEM6RWDH',
    aws_secret_access_key='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',
    region_name='us-east-1'
    )

# nombre del bucket
BUCKET_NAME = 'nombramientos-bucket'