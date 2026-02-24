"""Azure cloud resource types."""

from pydantypes.cloud.azure.compute import (
    AksClusterName,
    ApiManagementName,
    AppServiceName,
    ContainerAppName,
    FunctionAppName,
    LogAnalyticsWorkspaceName,
)
from pydantypes.cloud.azure.containers import ContainerRegistryName
from pydantypes.cloud.azure.database import (
    CosmosDbAccountName,
    DatabricksWorkspaceName,
    DataFactoryName,
    RedisCacheName,
    SqlServerName,
)
from pydantypes.cloud.azure.identity import ResourceGroupName, SubscriptionId, TenantId
from pydantypes.cloud.azure.keyvault import KeyVaultName, KeyVaultSecretName, KeyVaultUri
from pydantypes.cloud.azure.messaging import EventHubNamespaceName, ServiceBusNamespace
from pydantypes.cloud.azure.region import Region
from pydantypes.cloud.azure.resource import ResourceId
from pydantypes.cloud.azure.storage import BlobStorageUri, StorageAccountName

__all__ = [
    "AksClusterName",
    "ApiManagementName",
    "AppServiceName",
    "BlobStorageUri",
    "ContainerAppName",
    "ContainerRegistryName",
    "CosmosDbAccountName",
    "DataFactoryName",
    "DatabricksWorkspaceName",
    "EventHubNamespaceName",
    "FunctionAppName",
    "KeyVaultName",
    "KeyVaultSecretName",
    "KeyVaultUri",
    "LogAnalyticsWorkspaceName",
    "RedisCacheName",
    "Region",
    "ResourceGroupName",
    "ResourceId",
    "ServiceBusNamespace",
    "SqlServerName",
    "StorageAccountName",
    "SubscriptionId",
    "TenantId",
]
