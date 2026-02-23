"""AWS cloud resource types."""

from pydantypes.cloud.aws.arn import Arn, IamRoleArn, SnsTopicArn
from pydantypes.cloud.aws.compute import (
    AmiId,
    Ec2InstanceId,
    EcsClusterName,
    EksClusterName,
    LambdaFunctionName,
)
from pydantypes.cloud.aws.containers import EcrRepositoryUri
from pydantypes.cloud.aws.database import DynamoDbTableName, RdsInstanceId
from pydantypes.cloud.aws.identity import AccountId, CognitoUserPoolId, Region
from pydantypes.cloud.aws.messaging import SqsQueueUrl
from pydantypes.cloud.aws.monitoring import CloudWatchLogGroupName
from pydantypes.cloud.aws.network import (
    CloudFrontDistributionId,
    ElasticIpAllocationId,
    EniId,
    InternetGatewayId,
    NatGatewayId,
    Route53HostedZoneId,
    SecurityGroupId,
    SubnetId,
    VpcId,
)
from pydantypes.cloud.aws.security import KmsKeyId, SecretsManagerSecretName, SsmParameterName
from pydantypes.cloud.aws.storage import EbsSnapshotId, EbsVolumeId, S3BucketName, S3Uri

__all__ = [
    "AccountId",
    "AmiId",
    "Arn",
    "CloudFrontDistributionId",
    "CloudWatchLogGroupName",
    "CognitoUserPoolId",
    "DynamoDbTableName",
    "EbsSnapshotId",
    "EbsVolumeId",
    "Ec2InstanceId",
    "EcrRepositoryUri",
    "EcsClusterName",
    "EksClusterName",
    "ElasticIpAllocationId",
    "EniId",
    "IamRoleArn",
    "InternetGatewayId",
    "KmsKeyId",
    "LambdaFunctionName",
    "NatGatewayId",
    "RdsInstanceId",
    "Region",
    "Route53HostedZoneId",
    "S3BucketName",
    "S3Uri",
    "SecretsManagerSecretName",
    "SecurityGroupId",
    "SnsTopicArn",
    "SqsQueueUrl",
    "SsmParameterName",
    "SubnetId",
    "VpcId",
]
