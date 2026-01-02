from typing import Any
from unittest import mock

import pytest
from asgiref.sync import async_to_sync
from django.contrib.sites.models import Site
from pytest_django.fixtures import SettingsWrapper

from channels_extensions.sites import CurrentSiteMiddleware

pytestmark = pytest.mark.django_db


class TestCurrentSiteMiddleware:
    def test_adds_site_to_scope(self, settings: SettingsWrapper) -> None:
        scope: dict[str, Any] = {}
        receive = mock.AsyncMock()
        send = mock.AsyncMock()
        inner = mock.AsyncMock()
        expected_site, _ = Site.objects.get_or_create(domain="example.com")
        settings.SITE_ID = expected_site.pk
        expected_scope = scope | {"site": expected_site}

        middleware = CurrentSiteMiddleware(inner)
        async_to_sync(middleware)(scope, receive, send)

        inner.assert_awaited_once_with(expected_scope, receive, send)

    def test_site_already_in_scope(self, settings: SettingsWrapper) -> None:
        scope: dict[str, Any] = {"site": Site.objects.get_or_create(domain="example.com")[0]}
        receive = mock.AsyncMock()
        send = mock.AsyncMock()
        inner = mock.AsyncMock()

        settings.SITE_ID = scope["site"].pk

        middleware = CurrentSiteMiddleware(inner)
        async_to_sync(middleware)(scope, receive, send)

        inner.assert_awaited_once_with(scope, receive, send)
