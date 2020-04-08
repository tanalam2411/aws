#! /usr/env/bin python3

import boto3


def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')

    instances = dict()

    for instance in ec2.instances.all():
        print(instance.id, instance.state)
        instances[instance.id] = instance.state

    return {
        'statusCode': 200,
        'body': instances
    }
