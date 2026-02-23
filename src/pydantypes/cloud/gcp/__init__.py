"""GCP cloud resource types."""

from pydantypes.cloud.gcp.compute import CloudFunctionName, CloudRunServiceName, ComputeResourceName
from pydantypes.cloud.gcp.containers import ArtifactRegistryImageUri
from pydantypes.cloud.gcp.database import (
    BigQueryDatasetId,
    BigQueryTableId,
    CloudSqlInstanceId,
    SpannerDatabaseId,
    SpannerInstanceId,
)
from pydantypes.cloud.gcp.identity import (
    BillingAccountId,
    OrganizationId,
    ProjectId,
    ProjectNumber,
    Region,
    ServiceAccountEmail,
    Zone,
)
from pydantypes.cloud.gcp.messaging import PubSubSubscriptionName, PubSubTopicName
from pydantypes.cloud.gcp.security import (
    KmsKeyName,
    SecretManagerSecretName,
    SecretManagerVersionName,
)
from pydantypes.cloud.gcp.storage import GcsBucketName, GcsUri

__all__ = [
    "ArtifactRegistryImageUri",
    "BigQueryDatasetId",
    "BigQueryTableId",
    "BillingAccountId",
    "CloudFunctionName",
    "CloudRunServiceName",
    "CloudSqlInstanceId",
    "ComputeResourceName",
    "GcsBucketName",
    "GcsUri",
    "KmsKeyName",
    "OrganizationId",
    "ProjectId",
    "ProjectNumber",
    "PubSubSubscriptionName",
    "PubSubTopicName",
    "Region",
    "SecretManagerSecretName",
    "SecretManagerVersionName",
    "ServiceAccountEmail",
    "SpannerDatabaseId",
    "SpannerInstanceId",
    "Zone",
]
