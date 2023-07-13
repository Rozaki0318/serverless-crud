# How to start dev of lambda with dynamodb at local env

Sam, aws-cli, docker are required.

SAM CLI, version 1.88.0
aws-cli/2.0.7 Python/3.7.4 Darwin/22.2.0 botocore/2.0.0dev11
Docker version 20.10.11, build dea9396
docker-compose version 1.29.2, build 5becea4c

$ sam init
```
Which template source would you like to use?
	1 - AWS Quick Start Templates
	2 - Custom Template Location
Choice: 1
Choose an AWS Quick Start application template
	1 - Hello World Example
	2 - Data processing
	3 - Hello World Example with Powertools for AWS Lambda
	4 - Multi-step workflow
	5 - Scheduled task
	6 - Standalone function
	7 - Serverless API
	8 - Infrastructure event management
	9 - Lambda Response Streaming
	10 - Serverless Connector Hello World Example
	11 - Multi-step workflow with Connectors
	12 - Full Stack
	13 - Lambda EFS example
	14 - DynamoDB Example
	15 - Machine Learning
Template: 1

Use the most popular runtime and package type? (Python and zip) [y/N]: y

Would you like to enable X-Ray tracing on the function(s) in your application?  [y/N]: N

Would you like to enable monitoring using CloudWatch Application Insights?
For more info, please view https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-application-insights.html [y/N]: N

Project name [sam-app]: serverless-crud

    -----------------------
    Generating application:
    -----------------------
    Name: serverless-crud
    Runtime: python3.9
    Architectures: x86_64
    Dependency Manager: pip
    Application Template: hello-world
    Output Directory: .
    Configuration file: serverless-crud/samconfig.toml
    
    Next steps can be found in the README file at serverless-crud/README.md
        

Commands you can use next
=========================
[*] Create pipeline: cd serverless-crud && sam pipeline init --bootstrap
[*] Validate SAM template: cd serverless-crud && sam validate
[*] Test Function in the Cloud: cd serverless-crud && sam sync --stack-name {stack-name} --watch
```

Create docker network(external) to access from sam to local dyanamodb

$ docker network create lambda-local

$ docker network ls 

$ cd servereless-crud

$ mkdir local-containers&&cd local-containers

$ vi docker-compose.yml

```
   version: '3.8'
   services:
     dynamodb-local:
       command: "-jar DynamoDBLocal.jar -sharedDb -dbPath ./data"
       image: "amazon/dynamodb-local:latest"
       container_name: dynamodb-local
       ports:
         - "8000:8000"
       volumes:
         - "./docker/dynamodb:/home/dynamodblocal/data"
       working_dir: /home/dynamodblocal
       networks:
         - lambda-local
     nginx-local:
       image: nginx:latest
       container_name: nginx-local
       ports:
         - "8001:80"
       volumes:
         - "./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf"
         - "./docker/nginx/html/:/usr/share/nginx/html/"
       networks:
         - lambda-local
   networks:
     lambda-local:
       external: true
```

$ docker-compose up -d

Update directory name helloworld to read

Update app.py to pull data from dynamodb by boto3

Update template.yml to change CodeUri, Path and Name of Function&Events

$ sam build && sam local start-api --docker-network lambda-local

