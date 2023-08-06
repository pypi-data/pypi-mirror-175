from __future__ import annotations

from dataclasses import dataclass
from typing import Type

from cdktf import TerraformStack
from constructs import Construct


@dataclass
class StackConfig:
    StackClassImpl: Type
    Provider: Type
    StackName: str = ""
    ToBeLoad: bool = True

    def create_stack(self, scope: Construct, prefix: str) -> TerraformStack:
        return self.StackClassImpl(scope, f"{prefix}-{self.StackName}", self)
