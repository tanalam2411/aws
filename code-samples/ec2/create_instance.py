import boto3
from botocore.exceptions import ClientError


ec2 = boto3.client('ec2')

pg = ec2.start_instances()

