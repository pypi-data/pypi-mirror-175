# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import io
import json
import os
from functools import partial

import mock
import pytest

from fake_useragent import errors, settings, utils
from fake_useragent.utils import urlopen_has_ssl_context
from tests.utils import _request, find_unused_port, assets

try:  # Python 2 # pragma: no cover
    from urllib2 import Request
except ImportError:  # Python 3 # pragma: no cover
    from urllib.request import Request


def test_utils_get():
    assert utils.get("http://google.com") is not None

    if urlopen_has_ssl_context:
        with pytest.raises(errors.FakeUserAgentError):
            utils.get("https://expired.badssl.com/")

        assert (
            utils.get(
                "https://expired.badssl.com/",
                verify_ssl=False,
            )
            is not None
        )


def test_utils_get_retries():
    def __retried_request(*args, **kwargs):  # noqa
        __retried_request.attempt += 1

        if __retried_request.attempt < settings.HTTP_RETRIES:
            return Request(
                "http://0.0.0.0:{port}".format(
                    port=find_unused_port(),
                )
            )

        return Request(*args, **kwargs)

    __retried_request.attempt = 0

    with mock.patch(
        "fake_useragent.utils.Request",
        side_effect=__retried_request,
    ):
        assert utils.get("http://google.com") is not None

    assert __retried_request.attempt == 2


def test_utils_get_cache_server():
    jsonLines = utils.get(settings.CACHE_SERVER).decode("utf-8")
    data = {}
    for line in jsonLines.splitlines():
        data.update(json.loads(line))

    expected = {
        "chrome": mock.ANY,
        "opera": mock.ANY,
        "firefox": mock.ANY,
        "safari": mock.ANY,
        "edge": mock.ANY,
        "internet explorer": mock.ANY,
    }

    assert expected == data


def test_utils_load(path):
    _load = utils.load

    with mock.patch(
        "fake_useragent.utils.load",
        side_effect=_load,
    ) as mocked:
        browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
        data = utils.load(browsers, use_cache_server=False)

        mocked.assert_called()

    expected = {
        "chrome": mock.ANY,
        "edge": mock.ANY,
        "firefox": mock.ANY,
        "opera": mock.ANY,
        "safari": mock.ANY,
        "internet explorer": mock.ANY,
    }

    assert expected == data


def test_utils_write(path):
    data = {"foo": "bar"}

    utils.write(path, data)

    with io.open(path, mode="rt", encoding="utf-8") as fp:
        expected = json.loads(fp.read())

    assert expected == data


def test_utils_read(path):
    data = {"foo": "bar"}

    with io.open(path, mode="wt", encoding="utf-8") as fp:
        dumped = json.dumps(data)

        if not isinstance(dumped, utils.text):  # Python 2
            dumped = dumped.decode("utf-8")

        fp.write(dumped)

    expected = utils.read(path)

    assert expected == data


def test_utils_exist(path):
    assert not os.path.isfile(path)

    assert not utils.exist(path)

    with io.open(path, mode="wb") as fp:
        fp.write(b"\n")

    assert os.path.isfile(path)

    assert utils.exist(path)


def test_utils_rm(path):
    assert not os.path.isfile(path)

    with io.open(path, mode="wb") as fp:
        fp.write(b"\n")

    assert os.path.isfile(path)

    utils.rm(path)

    assert not os.path.isfile(path)


def test_utils_update(path):
    browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
    utils.update(path, browsers, use_cache_server=False)

    mtime = os.path.getmtime(path)

    _load = utils.load

    with mock.patch(
        "fake_useragent.utils.load",
        side_effect=_load,
    ) as mocked:
        utils.update(path, browsers, use_cache_server=False)

        mocked.assert_called()

    assert os.path.getmtime(path) != mtime


def test_utils_load_cached(path):
    _load = utils.load

    with mock.patch(
        "fake_useragent.utils.load",
        side_effect=_load,
    ) as mocked:
        browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
        data = utils.load_cached(path, browsers, use_cache_server=False)

        mocked.assert_called()

    expected = {
        "chrome": mock.ANY,
        "edge": mock.ANY,
        "firefox": mock.ANY,
        "opera": mock.ANY,
        "safari": mock.ANY,
        "internet explorer": mock.ANY,
    }

    assert expected == data

    expected = data

    with mock.patch("fake_useragent.utils.load") as mocked:
        browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
        data = utils.load_cached(path, browsers, use_cache_server=False)

        mocked.assert_not_called()

    assert expected == data


def test_utils_load_no_use_cache_server(path):
    denied_urls = [
        "https://useragentstring.com",
    ]

    with mock.patch(
        "fake_useragent.utils.Request",
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
        with pytest.raises(errors.FakeUserAgentError):
            utils.load(browsers, use_cache_server=False)

        with pytest.raises(errors.FakeUserAgentError):
            utils.load_cached(path, browsers, use_cache_server=False)

        with pytest.raises(errors.FakeUserAgentError):
            utils.update(path, browsers, use_cache_server=False)


def test_utils_load_use_cache_server(path):
    denied_urls = [
        "https://useragentstring.com",
    ]

    with mock.patch(
        "fake_useragent.utils.Request",
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
        data = utils.load(browsers, use_cache_server=True)

        expected = {
            "chrome": mock.ANY,
            "edge": mock.ANY,
            "firefox": mock.ANY,
            "opera": mock.ANY,
            "safari": mock.ANY,
            "internet explorer": mock.ANY,
        }

        assert expected == data


def test_utils_load_use_cache_server_down(path):
    denied_urls = [
        "https://useragentstring.com/",
        settings.CACHE_SERVER,
    ]

    with mock.patch(
        "fake_useragent.utils.Request",
        side_effect=partial(_request, denied_urls=denied_urls),
    ):
        browsers = ["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]
        with pytest.raises(errors.FakeUserAgentError):
            utils.load(browsers, use_cache_server=True)
