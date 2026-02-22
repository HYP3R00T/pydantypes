"""Smoke tests — verify the package is importable."""

import pydantypes


def test_version() -> None:
    assert isinstance(pydantypes.__version__, str)


def test_subpackages_importable() -> None:
    from pydantypes import data, devops, web  # noqa: F401
    from pydantypes.cloud import aws, azure, gcp  # noqa: F401


def test_all_aws_types_importable() -> None:
    from pydantypes.cloud.aws import (  # noqa: F401
        AccountId,
        Arn,
        DynamoDbTableName,
        Ec2InstanceId,
        IamRoleArn,
        LambdaFunctionName,
        RdsInstanceId,
        Region,
        S3Uri,
        SecurityGroupId,
        SnsTopicArn,
        SqsQueueUrl,
        SubnetId,
        VpcId,
    )


def test_all_azure_types_importable() -> None:
    from pydantypes.cloud.azure import (  # noqa: F401
        BlobStorageUri,
        CosmosDbAccountName,
        FunctionAppName,
        KeyVaultUri,
        Region,
        ResourceGroupName,
        ResourceId,
        ServiceBusNamespace,
        SqlServerName,
        SubscriptionId,
        TenantId,
    )


def test_all_gcp_types_importable() -> None:
    from pydantypes.cloud.gcp import (  # noqa: F401
        BigQueryDatasetId,
        CloudRunServiceName,
        CloudSqlInstanceId,
        GcsUri,
        ProjectId,
        PubSubTopicName,
        Region,
        ServiceAccountEmail,
        Zone,
    )


def test_all_devops_types_importable() -> None:
    from pydantypes.devops import (  # noqa: F401
        DockerImageRef,
        HelmChartName,
        K8sLabelKey,
        K8sLabelValue,
        K8sNamespaceName,
        K8sResourceName,
        TerraformResourceAddress,
    )


def test_all_web_types_importable() -> None:
    from pydantypes.web import (  # noqa: F401
        Jwt,
        Md5Hex,
        MimeType,
        Sha1Hex,
        Sha256Hex,
    )


def test_all_data_types_importable() -> None:
    from pydantypes.data import TableIdentifier  # noqa: F401
