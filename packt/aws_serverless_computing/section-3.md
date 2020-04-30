##### Development Patterns

---

##### Serverless Framework

- Services: A service is our unit of project. It's the top level name for the service we are creating and contains all the functions, events, and resources we need for th project.
  - You can build everything you need into one service, or have multiple services for a single serverless application.
  - It's up to us to define what the delineation is and where the domain boundaries are.
  
```bash
$ sls create -t "aws-python3" --path notification-service --name notification-service
```

- Events(serverless.yml)
    ```yaml
    events:
      http:
        path: notification/all
        method: get
    ```
  - The terms for each event type have been generalized so that the implementation underneath can support multi-cloud deployments.
  - For example, if we assigned an HTTP event to a function, when we deployed this to AWS, we would get an Amozon API Gateway endpoint integrated into trigger our function. 
  - In another cloud provider, the equivalent service integration would be created.
  - We can define multiple event mappings for each function.
  - List of AWS [events](https://www.serverless.com/framework/docs/providers/aws/events/)

- Resources: CloudFormation template syntax is used to define the resources.
```yaml
resources:
  Resources:
    notificationManager:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: notificationManager
        AttributeDefinitions:
          - AttributeName: name
            AttributeType: S
          - AttributeName: id
            AttributeType: HASH
        KeySchema:
          - AttributeName: id
            AttributeValue: HASH
        ProvisionedThroughput:
          ReadCapacityUnits: 1
          WriteCapacityUnits: 1
``` 

- Plugins: e.g. - [Serverless Python Requirements](https://github.com/UnitedIncome/serverless-python-requirements)
```bash
notification-service$ sls plugin install -n serverless-python-requirements
Serverless: Creating an empty package.json file in your service directory
Serverless: Installing plugin "serverless-python-requirements@latest" (this might take a few seconds...)
Serverless: Successfully installed "serverless-python-requirements@latest"
```

```bash
notification-service$ sls deploy
Serverless: Generated requirements from /home/afour/tanveer/ws/work_repos/aws/packt/aws_serverless_computing/notification-service/requirements.txt in /home/afour/tanveer/ws/work_repos/aws/packt/aws_serverless_computing/notification-service/.serverless/requirements.txt...
Serverless: Using static cache of requirements found at /home/afour/.cache/serverless-python-requirements/12104f2f8fb0c8baf53a7f80980e301c56aefae545831992d577783b87a94299_slspyc ...
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Injecting required Python packages to package...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service notification-service.zip file to S3 (9.03 MB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
..........................................
Serverless: Stack update finished...
Service Information
service: notification-service
stage: dev
region: us-east-1
stack: notification-service-dev
resources: 15
api keys:
  None
endpoints:
  GET - https://qa8a2f52y8.execute-api.us-east-1.amazonaws.com/dev/notification/all
functions:
  notification_handler: notification-service-dev-notification_handler
layers:
  None
Serverless: Removing old service artifacts from S3...
Serverless: Run the "serverless" command to setup monitoring, troubleshooting and testing.

```