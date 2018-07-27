from contextlib import suppress

import pytest

from lazy_log import lazy_log


def test_target_is_only_run_once(mocker):
    magic_mock = mocker.MagicMock()
    proxied = lazy_log(magic_mock)

    proxied.get_result()
    proxied.get_result()

    magic_mock.assert_called_once_with()


def test_attributes_cannot_be_set():
    class stub: pass
    proxied = lazy_log(stub)

    with pytest.raises(AttributeError):
        proxied.something = "this will not set"

    assert not hasattr(stub, 'something')
    assert not hasattr(proxied, 'something')


def test_attempting_to_set_attribute_does_not_cause_evaluation(mocker):
    magic_mock = mocker.MagicMock()
    proxied = lazy_log(magic_mock)

    with suppress(AttributeError):
        proxied.something = "this will not set"

    magic_mock.assert_not_called()


def test_attribute_cannot_be_deleted():
    class stub:
        something = "this cannot be deleted"
    proxied = lazy_log(stub)

    with pytest.raises(AttributeError):
        del proxied.something

    assert proxied.something == 'this cannot be deleted'
    assert stub.something == 'this cannot be deleted'
