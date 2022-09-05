import os

from zeit_on_tolino.tolino_partner import PartnerDetails


class EnvVars:
    # tolino env vars
    TOLINO_USER: str = "TOLINO_USER"
    TOLINO_PASSWORD: str = "TOLINO_PASSWORD"
    TOLINO_PARTNER_SHOP: str = "TOLINO_PARTNER_SHOP"

    # zeit env vars
    ZEIT_PREMIUM_USER: str = "ZEIT_PREMIUM_USER"
    ZEIT_PREMIUM_PASSWORD: str = "ZEIT_PREMIUM_PASSWORD"


class MissingEnvironmentVariable(Exception):
    pass


def verify_env_vars_are_set() -> None:
    for var_key in EnvVars.__dict__.keys():
        if not var_key.startswith("__"):
            var_name = getattr(EnvVars, var_key)
            if var_name not in os.environ:
                raise MissingEnvironmentVariable(
                    f"The environment variable '{var_name}' is missing. Ensure to export it."
                )


def verify_configured_partner_shop_is_supported() -> None:
    shop = os.environ.get(EnvVars.TOLINO_PARTNER_SHOP)
    if shop not in PartnerDetails.__annotations__.keys():
        supported_shops = [p for p in PartnerDetails.__annotations__.keys()]
        raise ValueError(f"Tolino partner shop '{shop}' is not supported. Supported shops are: {supported_shops}")
