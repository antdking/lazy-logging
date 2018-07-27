from unittest.mock import MagicMock

import pytest

from lazy_log import lazy_log


@pytest.fixture
def magic_mock(mocker):
    mocked = mocker.MagicMock()
    # we do this so we can still access calls
    mocked.return_value = mocked
    yield mocked


@pytest.fixture
def make_magic_mock(mocker):
    def _make_magic_mock(method_name):
        magic_mock = mocker.MagicMock()
        magic_mock.return_value = magic_mock
        setattr(magic_mock, method_name, mocker.MagicMock())
        return magic_mock

    return _make_magic_mock


@pytest.mark.parametrize('method_name', [
    '__repr__',
    '__str__',
    '__bytes__',
    '__hash__',
    '__bool__',
    '__dir__',
    '__len__',
    '__length_hint__',
    '__complex__',
    '__int__',
    '__float__',
    '__round__',
    '__index__',
])
def test_special_methods_proxied(make_magic_mock, method_name):
    magic_mock = make_magic_mock(method_name)
    proxied = lazy_log(magic_mock)

    getattr(proxied, method_name)()

    getattr(magic_mock, method_name).assert_called_once()


@pytest.mark.parametrize('method_name, params', [
    ('__format__', ['!a']),
    # ('__getattr', ['attr_name']),  # This cannot be tested :/
    ('__getitem__', ['key_name']),
    ('__missing__', ['key_name']),
    ('__round__', [2]),
])
def test_special_methods_proxied_with_parameters(make_magic_mock, method_name, params):
    magic_mock = make_magic_mock(method_name)
    proxied = lazy_log(magic_mock)

    getattr(proxied, method_name)(*params)

    getattr(magic_mock, method_name).assert_called_once_with(*params)


def test_custom_attributes_proxied():
    class stub:
        some_attribute = 42
    proxied = lazy_log(stub)

    assert 42 == proxied.some_attribute


def test_custom_methods_proxied(make_magic_mock):
    magic_mock = make_magic_mock('some_method_name')
    proxied = lazy_log(magic_mock)

    getattr(proxied, 'some_method_name')('some_parameter')

    magic_mock.some_method_name.assert_called_once_with('some_parameter')
