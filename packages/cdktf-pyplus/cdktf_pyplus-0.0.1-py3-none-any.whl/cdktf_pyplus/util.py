import random
import string
from collections import defaultdict
from importlib import import_module
from pathlib import Path
from pkgutil import iter_modules

from cdktf import App

from utils.config_base import StackConfig


def get_profile_config_map(profiles_path: str) -> dict[str, list[StackConfig]]:
    result: dict[str, list[StackConfig]] = defaultdict(lambda: [])
    package_dir = str(Path(profiles_path).resolve())
    module_attr_map: dict[str, set[str]] = defaultdict(lambda: set())
    for (_, module_name, _) in iter_modules([package_dir]):
        module = import_module(f"{profiles_path}.{module_name}")
        for attribute_name in dir(module):
            attribute: StackConfig = getattr(module, attribute_name)
            if isinstance(attribute, StackConfig) and attribute.ToBeLoad:
                if attribute.StackName in module_attr_map[module_name]:
                    msg = f"Config {attribute_name}.StackName('{attribute.StackName}') duplicated in profile - {module_name}"
                    raise Exception(msg)
                module_attr_map[module_name].add(attribute.StackName)
                result[module_name].append(attribute)
    return result


def read_shell_script(dir: str, s: str) -> str:
    src_dir = Path(dir).resolve().parent
    with Path(src_dir).joinpath(s).open() as f:
        data = f.read()
    return data.replace("${", "$${")


def gen_rand_id() -> str:
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(16))
    return result_str


def attach_profiles(app: App, profile_dir: str) -> App:
    for k, v in get_profile_config_map(profile_dir).items():
        for cfg in v:
            cfg.create_stack(app, k)
    return app
