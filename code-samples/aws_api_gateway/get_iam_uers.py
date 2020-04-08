#! /usr/env/bin python3

import boto3


def lambda_handler(event, context):
    users = {}

    iam = boto3.client('iam')
    for userlist in iam.list_users()['Users']:
        userGroups = iam.list_groups_for_user(UserName=userlist['UserName'])

        groups = list()

        for groupName in userGroups['Groups']:
            groups.append(groupName['GroupName'])

        users[userlist['UserName']] = groups

    return {
        'statusCode': 200,
        'body': users
    }
