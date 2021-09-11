from typing import Any, cast, Tuple, Union
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from injector import Injector
from ninja_extra.apps import NinjaExtraConfig

__all__ = ['resolve_container_services', 'get_injector']


def get_injector() -> Injector:
    app = cast(NinjaExtraConfig, apps.get_app_config(NinjaExtraConfig.name))
    if not app:
        raise ImproperlyConfigured(
            f"ninja_extra app is not installed. Did you forget register `ninja_extra` in `INSTALLED_APPS`"
        )
    injector = app.injector
    return injector


def resolve_container_services(*services: type) -> Union[Tuple[Any], Any]:
    assert services, 'Service can not be empty'

    injector = get_injector()

    if len(services) > 1:
        services_resolved = []
        for service in services:
            services_resolved.append(injector.get(service))
        return tuple(services_resolved)
    return injector.get(services[0])
