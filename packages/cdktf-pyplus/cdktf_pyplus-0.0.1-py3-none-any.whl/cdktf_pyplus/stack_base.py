from __future__ import annotations

from cdktf import TerraformStack
from cdktf_cdktf_provider_random.id import Id
from cdktf_cdktf_provider_random.provider import RandomProvider
from constructs import Construct


class StackWithAutoId(TerraformStack):
    def to_rand_name(self, s: str) -> str:
        return f"{s}-{self.ns}-{self.id_.hex}"

    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)
        self.ns = ns
        self.id_ = Id(
            self,
            f"rand-id-{ns}",
            byte_length=8,
            provider=RandomProvider(self, f"rand-provider-{ns}"),
        )
