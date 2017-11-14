from . import app
import hug
from hug_sentry import SentryExceptionHandler
from unittest.mock import Mock
import pytest


def test_sentry_handler():
    client = Mock()
    handler = SentryExceptionHandler(client)
    app.__hug__.http.add_exception_handler(Exception, handler)

    with pytest.raises(ZeroDivisionError):
        hug.test.get(app, 'fail', amount=2)

    assert client.captureException.called

    data = client.captureException.call_args[1]['data']
    assert 'user' in data
    assert 'request' in data
    assert data['request']['method'] == 'GET'
    assert data['request']['query_string'] == 'amount=2'


def test_sentry_handler_with_routing_parameters():
    client = Mock()
    handler = SentryExceptionHandler(client)
    app.__hug__.http.add_exception_handler(Exception, handler)

    with pytest.raises(Exception):
        hug.test.get(app, 'routing_fail/' + str(2))

    assert client.captureException.called

    data = client.captureException.call_args[1]['data']
    assert 'user' in data
    assert 'request' in data
    assert data['request']['method'] == 'GET'


def test_clean_environment():
    handler = SentryExceptionHandler(Mock())
    env = {'IRRELEVANT': 'remove me'}

    cleaned_env = handler.clean_environment(env)
    assert 'IRRELEVANT' not in cleaned_env


def test_clean_environment_doesnt_mutate_orignal():
    handler = SentryExceptionHandler(Mock())
    env = {'IRRELEVANT': 'remove me'}

    handler.clean_environment(env)
    assert 'IRRELEVANT' in env


def test_clean_environment_keeps_server_attributes():
    handler = SentryExceptionHandler(Mock())
    env = {
        'SERVER_A': 'a',
        'SERVER_B': 'b'
    }

    cleaned_env = handler.clean_environment(env)
    assert cleaned_env == env


def test_clean_environment_keeps_remote_addr():
    handler = SentryExceptionHandler(Mock())
    env = {'REMOTE_ADDR': '192.168.99.100'}

    cleaned_env = handler.clean_environment(env)
    assert cleaned_env == env


def test_guess_user_ip_from_request():
    handler = SentryExceptionHandler(Mock())
    request = Mock()

    request.env = {}
    request.headers = {}
    assert handler.guess_user_ip_from_request(request) == '127.0.0.1'

    request.env = {'REMOTE_ADDR': '192.168.99.100'}
    assert handler.guess_user_ip_from_request(request) == '192.168.99.100'

    request.headers = {'X-FORWARDED-FOR': '10.0.8.2'}
    assert handler.guess_user_ip_from_request(request) == '10.0.8.2'
