from pydantypes.cloud.azure.compute import FunctionAppName
from pydantypes.cloud.azure.database import CosmosDbAccountName, SqlServerName
from pydantypes.cloud.azure.identity import Region, ResourceGroupName, SubscriptionId, TenantId
from pydantypes.cloud.azure.keyvault import KeyVaultUri
from pydantypes.cloud.azure.messaging import ServiceBusNamespace
from pydantypes.cloud.azure.resource import ResourceId
from pydantypes.cloud.azure.storage import BlobStorageUri

__all__ = [
    "BlobStorageUri",
    "CosmosDbAccountName",
    "FunctionAppName",
    "KeyVaultUri",
    "Region",
    "ResourceGroupName",
    "ResourceId",
    "ServiceBusNamespace",
    "SqlServerName",
    "SubscriptionId",
    "TenantId",
]
