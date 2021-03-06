import pytest
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from redirink.insights.models import Insight, Visitor
from redirink.insights.tests.factories import InsightFactory, VisitorFactory
from redirink.links.models import Link
from redirink.links.tests.factories import LinkFactory
from redirink.users.models import User
from redirink.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def api_rf():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def rq(api_rf) -> Request:
    return api_rf.get("/mocked-request-path/")


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def link() -> Link:
    return LinkFactory()


@pytest.fixture
def token(user) -> Token:
    return Token.objects.get_or_create(user=user)


@pytest.fixture
def insight() -> Insight:
    return InsightFactory()


@pytest.fixture
def visitor() -> Visitor:
    return VisitorFactory()
