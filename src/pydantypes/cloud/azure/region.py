"""Azure region types."""

from __future__ import annotations

from pydantypes._internal import StrEnum


# Source: https://learn.microsoft.com/en-us/azure/reliability/regions-list
class Region(StrEnum):
    """Azure region identifiers."""

    # US
    EASTUS = "eastus"
    EASTUS2 = "eastus2"
    WESTUS = "westus"
    WESTUS2 = "westus2"
    WESTUS3 = "westus3"
    CENTRALUS = "centralus"
    NORTHCENTRALUS = "northcentralus"
    SOUTHCENTRALUS = "southcentralus"
    WESTCENTRALUS = "westcentralus"

    # Canada
    CANADACENTRAL = "canadacentral"
    CANADAEAST = "canadaeast"

    # Brazil
    BRAZILSOUTH = "brazilsouth"
    BRAZILSOUTHEAST = "brazilsoutheast"

    # Europe
    NORTHEUROPE = "northeurope"
    WESTEUROPE = "westeurope"
    UKSOUTH = "uksouth"
    UKWEST = "ukwest"
    FRANCECENTRAL = "francecentral"
    FRANCESOUTH = "francesouth"
    GERMANYWESTCENTRAL = "germanywestcentral"
    GERMANYNORTH = "germanynorth"
    SWITZERLANDNORTH = "switzerlandnorth"
    SWITZERLANDWEST = "switzerlandwest"
    NORWAYEAST = "norwayeast"
    NORWAYWEST = "norwaywest"
    SWEDENCENTRAL = "swedencentral"

    # Asia Pacific
    EASTASIA = "eastasia"
    SOUTHEASTASIA = "southeastasia"
    JAPANEAST = "japaneast"
    JAPANWEST = "japanwest"
    AUSTRALIAEAST = "australiaeast"
    AUSTRALIASOUTHEAST = "australiasoutheast"
    AUSTRALIACENTRAL = "australiacentral"

    # India
    CENTRALINDIA = "centralindia"
    SOUTHINDIA = "southindia"
    WESTINDIA = "westindia"

    # Korea
    KOREACENTRAL = "koreacentral"
    KOREASOUTH = "koreasouth"

    # Middle East and Africa
    UAENORTH = "uaenorth"
    UAECENTRAL = "uaecentral"
    SOUTHAFRICANORTH = "southafricanorth"
    SOUTHAFRICAWEST = "southafricawest"

    # Other
    QATARCENTRAL = "qatarcentral"
    ISRAELCENTRAL = "israelcentral"
    ITALYNORTH = "italynorth"
    POLANDCENTRAL = "polandcentral"
    SPAINCENTRAL = "spaincentral"
    MEXICOCENTRAL = "mexicocentral"
    NEWZEALANDNORTH = "newzealandnorth"
    TAIWANNORTH = "taiwannorth"

    # US Government
    USGOVVIRGINIA = "usgovvirginia"
    USGOVARIZONA = "usgovarizona"
    USGOVIOWA = "usgoviowa"
    USGOVTEXAS = "usgovtexas"

    # China
    CHINAEAST = "chinaeast"
    CHINAEAST2 = "chinaeast2"
    CHINANORTH = "chinanorth"
    CHINANORTH2 = "chinanorth2"
