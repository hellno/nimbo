from typing import Union

import pydantic

from nimbo.core.config.aws_config import AwsConfig
from nimbo.core.config.common import CloudProvider, load_yaml_from_file
from nimbo.core.config.common import RequiredCase
from nimbo.core.config.gcp_config import GcpConfig
from nimbo.core.constants import NIMBO_CONFIG_FILE


# noinspection PyUnresolvedReferences
def make_config() -> Union[AwsConfig, GcpConfig]:
    config = load_yaml_from_file(NIMBO_CONFIG_FILE)

    # Provider field validation is postponed. If provider is not specified,
    # assume AwsConfig for running commands like --help and generate-config.
    if "provider" not in config:
        return AwsConfig(**config)
    else:
        config["provider"] = config["provider"].upper()

    try:
        provider = CloudProvider(config["provider"])
    except ValueError:
        permitted_values = ", ".join([f"'{p.value}'" for p in CloudProvider])
        raise pydantic.ValidationError(
            [
                pydantic.error_wrappers.ErrorWrapper(
                    Exception(
                        f"value is not a valid enumeration member; permitted: "
                        f"{permitted_values}"
                    ),
                    "provider",
                )
            ],
            AwsConfig,
        )

    if provider == CloudProvider.AWS:
        return AwsConfig(**config)

    return GcpConfig(**config)
