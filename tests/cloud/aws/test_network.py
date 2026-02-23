"""Tests for AWS network types."""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ValidationError

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


class VpcModel(BaseModel):
    vpc_id: VpcId


class SubnetModel(BaseModel):
    subnet_id: SubnetId


class SgModel(BaseModel):
    sg_id: SecurityGroupId


class NatModel(BaseModel):
    nat_id: NatGatewayId


class IgwModel(BaseModel):
    igw_id: InternetGatewayId


class EipModel(BaseModel):
    eip_id: ElasticIpAllocationId


class EniModel(BaseModel):
    eni_id: EniId


class CfModel(BaseModel):
    dist_id: CloudFrontDistributionId


class R53Model(BaseModel):
    zone_id: Route53HostedZoneId


@pytest.mark.parametrize("value", ["vpc-1234567890abcdef0", "vpc-12345678"])
def test_valid_vpc_id(value: str) -> None:
    model = VpcModel(vpc_id=value)
    assert model.vpc_id == value


@pytest.mark.parametrize("value", ["vpc-", "vpc-UPPER", "ec2-12345678", ""])
def test_invalid_vpc_id(value: str) -> None:
    with pytest.raises(ValidationError):
        VpcModel(vpc_id=value)


@pytest.mark.parametrize("value", ["subnet-1234567890abcdef0", "subnet-12345678"])
def test_valid_subnet_id(value: str) -> None:
    model = SubnetModel(subnet_id=value)
    assert model.subnet_id == value


@pytest.mark.parametrize("value", ["subnet-", "subnet-UPPER", ""])
def test_invalid_subnet_id(value: str) -> None:
    with pytest.raises(ValidationError):
        SubnetModel(subnet_id=value)


@pytest.mark.parametrize("value", ["sg-1234567890abcdef0", "sg-12345678"])
def test_valid_security_group_id(value: str) -> None:
    model = SgModel(sg_id=value)
    assert model.sg_id == value


@pytest.mark.parametrize("value", ["sg-", "sg-UPPER", ""])
def test_invalid_security_group_id(value: str) -> None:
    with pytest.raises(ValidationError):
        SgModel(sg_id=value)


def test_vpc_id_serialization() -> None:
    model = VpcModel(vpc_id="vpc-1234567890abcdef0")
    assert model.model_dump() == {"vpc_id": "vpc-1234567890abcdef0"}
    json_str = model.model_dump_json()
    restored = VpcModel.model_validate_json(json_str)
    assert restored.vpc_id == model.vpc_id


@pytest.mark.parametrize("value", ["nat-1234567890abcdef0", "nat-12345678"])
def test_valid_nat_gateway_id(value: str) -> None:
    model = NatModel(nat_id=value)
    assert model.nat_id == value


@pytest.mark.parametrize("value", ["nat-", "nat-UPPER", ""])
def test_invalid_nat_gateway_id(value: str) -> None:
    with pytest.raises(ValidationError):
        NatModel(nat_id=value)


@pytest.mark.parametrize("value", ["igw-1234567890abcdef0", "igw-12345678"])
def test_valid_internet_gateway_id(value: str) -> None:
    model = IgwModel(igw_id=value)
    assert model.igw_id == value


@pytest.mark.parametrize("value", ["igw-", "igw-UPPER", ""])
def test_invalid_internet_gateway_id(value: str) -> None:
    with pytest.raises(ValidationError):
        IgwModel(igw_id=value)


@pytest.mark.parametrize("value", ["eipalloc-1234567890abcdef0", "eipalloc-12345678"])
def test_valid_elastic_ip_allocation_id(value: str) -> None:
    model = EipModel(eip_id=value)
    assert model.eip_id == value


@pytest.mark.parametrize("value", ["eipalloc-", "eipalloc-UPPER", ""])
def test_invalid_elastic_ip_allocation_id(value: str) -> None:
    with pytest.raises(ValidationError):
        EipModel(eip_id=value)


@pytest.mark.parametrize("value", ["eni-1234567890abcdef0", "eni-12345678"])
def test_valid_eni_id(value: str) -> None:
    model = EniModel(eni_id=value)
    assert model.eni_id == value


@pytest.mark.parametrize("value", ["eni-", "eni-UPPER", ""])
def test_invalid_eni_id(value: str) -> None:
    with pytest.raises(ValidationError):
        EniModel(eni_id=value)


@pytest.mark.parametrize("value", ["E1A2B3C4D5E6F7", "EABCDEFGHIJK"])
def test_valid_cloudfront_distribution_id(value: str) -> None:
    model = CfModel(dist_id=value)
    assert model.dist_id == value


@pytest.mark.parametrize("value", ["E12345", "e1234567890A", "XABCDEFGHIJK", ""])
def test_invalid_cloudfront_distribution_id(value: str) -> None:
    with pytest.raises(ValidationError):
        CfModel(dist_id=value)


def test_cloudfront_distribution_id_serialization() -> None:
    model = CfModel(dist_id="E1A2B3C4D5E6F7")
    assert model.model_dump() == {"dist_id": "E1A2B3C4D5E6F7"}


@pytest.mark.parametrize("value", ["Z1234567890ABC", "ZA"])
def test_valid_route53_hosted_zone_id(value: str) -> None:
    model = R53Model(zone_id=value)
    assert model.zone_id == value


@pytest.mark.parametrize("value", ["Z", "A1234567890", "z1234567890ABC", ""])
def test_invalid_route53_hosted_zone_id(value: str) -> None:
    with pytest.raises(ValidationError):
        R53Model(zone_id=value)


def test_route53_hosted_zone_id_serialization() -> None:
    model = R53Model(zone_id="Z1234567890ABC")
    assert model.model_dump() == {"zone_id": "Z1234567890ABC"}
