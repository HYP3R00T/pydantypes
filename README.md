# pydantypes

pydantypes is an extension to Pydantic that defines a collection of various datatypes relevant for cloud software engineering. It includes custom types for AWS, Azure, and Google Cloud services, as well as other commonly used non-native types.

## Installation

To install pydantypes, use pip:

```bash
pip install pydantypes
```

## Usage

Here is a simple example of how to use pydantypes:


```python
from pydantic import BaseModel
import pydantypes.aws.S3 as S3

class Data(BaseModel):
    uri: S3.Uri

data = Data(uri="s3://my-bucket/my-object")
print(data)
```

## Features

- AWS Types: Custom datatypes for various AWS services like S3, EC2, Lambda, etc.
- Azure Types: Custom datatypes for various Azure services like Blob Storage, VMs, Functions, etc.
- Google Cloud Types: Custom datatypes for various Google Cloud services like GCS, Compute Engine, Cloud Functions, etc.
- Other Types: Frequently used types that are not native but commonly appear in engineering.

## Resources

- https://docs.pydantic.dev/latest/concepts/types/#strict-types
- https://docs.pydantic.dev/latest/api/types/#pydantic.types.NegativeInt
- https://github.com/pydantic/pydantic-extra-types/blob/main/.github/workflows/ci.yml
- https://github.com/pydantic/pydantic/blob/d654a0766c2f3c6fe0a12718f32aa3bf4d3ecc86/pydantic/types.py#L35
- https://github.com/annotated-types/annotated-types


## TODO

Suggested Types for pydantypes

AWS Types
S3.Uri: URI for S3 objects.
EC2.InstanceId: EC2 instance identifier.
Lambda.FunctionName: Lambda function name.
DynamoDB.TableName: DynamoDB table name.
SNS.TopicArn: SNS topic ARN.
SQS.QueueUrl: SQS queue URL.
IAM.RoleName: IAM role name.
RDS.DBInstanceIdentifier: RDS instance identifier.
Azure Types
BlobStorage.Uri: URI for Azure Blob Storage.
VM.ResourceId: Virtual Machine resource identifier.
FunctionApp.Name: Azure Function App name.
CosmosDB.AccountName: Cosmos DB account name.
ServiceBus.QueueName: Service Bus queue name.
AppService.Name: App Service name.
KeyVault.Uri: URI for Azure Key Vault.
SQLServer.ServerName: Azure SQL Server name.
Google Cloud Types
GCS.Uri: URI for Google Cloud Storage objects.
ComputeEngine.InstanceId: Compute Engine instance identifier.
CloudFunction.Name: Cloud Function name.
BigQuery.DatasetId: BigQuery dataset identifier.
PubSub.TopicName: Pub/Sub topic name.
Firestore.CollectionName: Firestore collection name.
CloudRun.ServiceName: Cloud Run service name.
CloudSQL.InstanceId: Cloud SQL instance identifier.
Common Cloud Types
Url: General URL datatype.
Email: Email address datatype.
UUID: Universal Unique Identifier.
Timestamp: ISO 8601 timestamp.
IPAddress: IP address datatype.
Region: Cloud region name.
ResourceName: General resource name.
Tag: Key-value tag pair for resource tagging.
Feel free to suggest more types or contribute to the project!
