import pytest

from zeit_on_tolino import env_vars


def _set_all_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(env_vars.EnvVars.TOLINO_PARTNER_SHOP, "thalia")
    monkeypatch.setenv(env_vars.EnvVars.TOLINO_USER, "foo")
    monkeypatch.setenv(env_vars.EnvVars.TOLINO_PASSWORD, "baa")
    monkeypatch.setenv(env_vars.EnvVars.ZEIT_PREMIUM_USER, "baz")
    monkeypatch.setenv(env_vars.EnvVars.ZEIT_PREMIUM_PASSWORD, "zap")


def test_verify_env_vars_are_set__success(monkeypatch: pytest.MonkeyPatch) -> None:
    _set_all_env_vars(monkeypatch)
    env_vars.verify_env_vars_are_set()


def test_verify_env_vars_are_set__failure(monkeypatch: pytest.MonkeyPatch) -> None:
    # loop over all existing env vars
    for var_key in env_vars.EnvVars.__annotations__.keys():
        var_name = getattr(env_vars.EnvVars, var_key)

        # set all env vars
        _set_all_env_vars(monkeypatch)
        # delete just one env var
        monkeypatch.delenv(var_name)
        # verify a proper error message is raised
        with pytest.raises(
            env_vars.MissingEnvironmentVariable,
            match=f"The environment variable '{var_name}' is missing. Ensure to export it.",
        ):
            env_vars.verify_env_vars_are_set()


def test_verify_configured_partner_shop_is_supported(monkeypatch: pytest.MonkeyPatch) -> None:
    # supported shop
    monkeypatch.setenv(env_vars.EnvVars.TOLINO_PARTNER_SHOP, "thalia")
    env_vars.verify_configured_partner_shop_is_supported()

    # unsupported shop
    monkeypatch.setenv(env_vars.EnvVars.TOLINO_PARTNER_SHOP, "foo")
    with pytest.raises(ValueError, match="Tolino partner shop 'foo' is not supported. Supported shops are: "):
        env_vars.verify_configured_partner_shop_is_supported()
