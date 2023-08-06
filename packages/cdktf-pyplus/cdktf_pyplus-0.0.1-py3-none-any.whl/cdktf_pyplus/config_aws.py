from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from cdktf_cdktf_provider_aws.provider import AwsProvider

from utils.config_base import StackConfig


@dataclass
class StackConfigAws(StackConfig):
    Region: str = "us-east-1"
    Provider: Type[AwsProvider] = AwsProvider
    AwsDomain: str = "amazonaws.com"


@dataclass
class StackConfigAwsChina(StackConfigAws):
    Region: str = "cn-north-1"
