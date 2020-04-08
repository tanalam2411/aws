##### Building Scalable APIs with the AWS API Gateway

- API Gateway - managed service from AWS for building APIs.
- Rapid and scalable.
- Provides monitoring such as API calls, Latency, Errors (stored in CloudWatch, Alarms via CloudWatch).
- App API calls are done via HTTPs.
- Default APIs use AWS SSL certificate.
- Custom domain APIs can use their own SSL certificate.
- Throttling API calls.
  - Throttle by burst(max) and rate(min) limit.
  - Prevent overloading backend services.
  - Requests over the limit receive HTTP 429 response.
  - This can be configured per API methods.
- Caching Your API Requests.
  - Configured per stage or API. (From 0.5GB - 237GB)
  - Additional billing charges apply.

- Definition of stages of API, e.g.,:
```bash
https://myapi.com/dev/shoes
https://myapi.com/beta/shoes
https://myapi.com/v1/shoes
```

- Lifecycle of an API
  - API -> Staging -> Production (v1)
  - API -> Staging -> Production (v2)
  - API -> Staging -> Production (vN)
  

---

##### Generating User Access Permissions

- About Access Polices
  - by default access is denied unless a policy exists allowing access.
  - can be combined allowing different access to different apis.
  - build using a combination of action-statements and resource-statements.
  
  - ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
              "Effect": "Allow",
              "Action": [
                "<action-statement>"
              ],
              "Resource": [
                "<resource-statement>"
              ]
            }
        ]
    }
    ```
  - action-statement: represent api actions where action is an available API Gateway action: GET, POST, PUT, DELETE, PATCH, HEAD, and OPTIONS.
      - ```bash
        "Action": [
            "apigateway:action"
        ]
        ```
        ```json
        "Effect: "Allow",
        "Action": [
          "apigateway:GET",
          "apigateway:POST"
          # or
          "apigateway:*"
        ]
        ```
      - Action statements are the same whether managing entity access or api call polices.  
  - resource-statement: represent API Gateway resources where region is an AWS target region and resource-path-specifier is the path to the target resources.
  - ```bash
    "'Resources": [
        "arn:aws:apigateway:region::resource-path-specifier"
    ]
    ```
    ```bash
    # this statement includes all resources, methods, models and states in the specified <region>.
    arn:aws:apigateway:<region>::/restapis/*
  
    # Specifies all resources, methods, models, and stages in the API with an id of <api-id> in the AWS <region>.
    arn:aws:apigateway:<region>::/restapis/<api-id>/*
    
    # Specifies resources and methods in the resource with an identifier of <resource-id>, in the API with an identifier of <api-id> in the AWS <region>.
    arn:aws:apigateway:<region>::/restapis/<api-id>/resources/<resource-id>/*
    
    # Specifies just the GET method in the resource with an identifier of <resource-id>, in the API with an identfier of <api-id> in the AWS region of region.
    arn:aws:apigateway:<region>::/restapis/<api-id>/resources/<resource-id>/methods/GET
    ```
  - Define access to the resources within API such as stages(dev, staging...), models, and resources(GET, POST...)  
    
---

##### Controlling API Access

- manage API entities:
 - Controlling access to the API entity in the AWS console.

- manage calling APIs:
  - Controlling calls to the API via IAM authentication.    
  
---

##### Managing Access: Calling APIs

- Allows securing access to APIs with IAM.
- Requires API requests to be signed.
  - Only supports AWS Signature Version 4
  - Required code included with SDK  

- Action statement includes <stage-name> :`arn:aws:apigateway:<region>::<api-id>:/<stage-name>/<resource-path-specifier>

```bash
# Specifies <any> resource path in any <stage>, for any <API> in any <region>.
arn:aws:apigateway:*::*:*

# Specifies any resource path in any <stage>, for any <API> in the region `us-east-1`.
arn:aws:apigateway:us-east-1::*:*

# Specifies any resource path in the stage of test, for the api with an identifier <api-id> in the region `us-east-1`
arn:aws:apigateway:us-east-1::<api-id>:/test/*
```

---

- Creating new User - 
  - Username - tan1
  - Password - Tan1@123

- Creating new group -
  - name: acmeshoes-dev
  
- Create a new Policy -
  - name: acmeshoes-devpolicy
  - description: Policy for developers working on ACME Shoes.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "apigateway:GET"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "apigateway:*"
            ],
            "Resource": [
                "arn:aws:apigateways:us-west-2::/restapis/*/stages/dev"
            ]
        }
    ]
}
```

- Attach `acmeshoes-devpolicy` to `acmeshoes-dev` group.

---

##### Using Lambda as a Backend Service

- Lambda: AWS Lambda is a compute service that runs your code in response to events and automatically manages the compute resources for you, making it easy to build applications that respond quickly to new information.
  - Runs you code in demand
  - No servers
  - Starts within milliseconds
  - Supports language such as Node.js, Java 8, Python 2.7 etc.
  - Managed for you:
    - Server
    - OS Maintenance
    - Scaling
    - Provisioning
    - Deployment
    
- Creating a Lambda function:


- Lambda Security:
  - Execution Permissions: permissions that your lambda function needs to access other AWS resources.
  - Invocation Permission: permission needed by the event source to communicate with your lambda function.    

- AWS Basic Execution Policy:
```json
{
  "Version": "2012-10-17",
  "statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```  

```json
{
  "Version": "2012-10-17",
  "statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:*"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

- Role Policy
```json
{
  "Version": "2012-10-17",
  "statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "apigateway.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

- Invocation Policy
```json
{
  "Statement": {
    "StatementId": "Id-1",
    "Action": "lambda:InvokeFunction",
    "Principal": "apigateway.amazonaws.com",
    "SourceArn": "arn:aws:execute-api:api_specific_resource_path",
    "SourceAccount": "account_id"
  }
}
```

---

```bash
You are about to give API Gateway permission to invoke your Lambda function:
arn:aws:lambda:ap-south-1:390618173518:function:getIAMUsers
```

##### Enabling CORS on a Method

- Method Response Settings: Define the headers allowed.
- Integration Response Settings: Define the values permitted for each header.


