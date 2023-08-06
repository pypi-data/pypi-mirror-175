import json

from cdktf import Fn
from cdktf_cdktf_provider_aws.data_aws_ami import DataAwsAmi
from cdktf_cdktf_provider_aws.data_aws_iam_policy import DataAwsIamPolicy
from cdktf_cdktf_provider_aws.data_aws_subnets import DataAwsSubnets
from cdktf_cdktf_provider_aws.data_aws_vpc import DataAwsVpc
from constructs import Construct
from iam_floyd import PolicyStatementBase

from utils.util import gen_rand_id


def to_filter(args: dict[str, list[str]]) -> list[dict[str, list[str]]]:
    r = []
    for k, v in args.items():
        r.append(
            {
                "name": k,
                "values": v,
            }
        )
    return r


def to_policy_str(s: PolicyStatementBase) -> str:
    return json.dumps(
        {
            "Statement": [s.to_json()],
        }
    )


def get_latest_ami(scope: Construct, filter: dict[str, list[str]]) -> DataAwsAmi:
    return DataAwsAmi(scope, gen_rand_id(), most_recent=True, filter=to_filter(filter))


def get_vpc(scope: Construct, filter: dict[str, list[str]]) -> DataAwsVpc:
    return DataAwsVpc(
        scope,
        gen_rand_id(),
        filter=to_filter(filter),
    )


def get_subnetids(scope: Construct, filter: dict[str, list[str]]) -> list[str]:
    nets = DataAwsSubnets(
        scope,
        gen_rand_id(),
        filter=to_filter(filter),
    )
    ids = []
    for i in range(0, len(nets.ids)):
        ids.append(Fn.element(nets.ids, i))
    return ids


def get_policy(scope: Construct, policy_name: str) -> DataAwsIamPolicy:
    return DataAwsIamPolicy(scope, gen_rand_id(), name=policy_name)
