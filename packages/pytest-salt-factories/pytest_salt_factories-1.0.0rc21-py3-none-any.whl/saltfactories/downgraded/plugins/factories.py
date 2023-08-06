"""
Salt Daemon Factories PyTest Plugin.

..
    PYTEST_DONT_REWRITE
"""
from __future__ import generator_stop
import logging
import os
import pprint
from typing import Any
from typing import Dict
import pytest
from pytest_tempdir.plugin import TempDir
from pytestsysstats.plugin import StatsProcesses
import saltfactories
from saltfactories.manager import FactoriesManager
from saltfactories.plugins.event_listener import EventListener

try:
    from pytest import FixtureRequest
except ImportError:
    from _pytest.fixtures import FixtureRequest
log = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def _salt_factories_config(request: FixtureRequest) -> Dict[str, Any]:
    """
    Return a dictionary with the keyword arguments for FactoriesManager.
    """
    log_server = request.config.pluginmanager.get_plugin('saltfactories-log-server')
    return {
        'code_dir': saltfactories.CODE_ROOT_DIR.parent,
        'inject_coverage': True,
        'inject_sitecustomize': True,
        'log_server_host': log_server.log_host,
        'log_server_port': log_server.log_port,
        'log_server_level': log_server.log_level,
        'system_install': os.environ.get('SALT_FACTORIES_SYSTEM_INSTALL', '0') == '1',
    }


@pytest.fixture(scope='session')
def salt_factories_config() -> Dict[str, Any]:
    """
    Default salt factories configuration fixture.
    """
    return {}


@pytest.fixture(scope='session')
def salt_factories(
    tempdir: TempDir,
    event_listener: EventListener,
    stats_processes: StatsProcesses,
    salt_factories_config: Dict[str, Any],
    _salt_factories_config: Dict[str, Any],
) -> FactoriesManager:
    """
    Instantiate the salt factories manager.
    """
    if not isinstance(salt_factories_config, dict):
        raise pytest.UsageError(
            "The 'salt_factories_config' fixture MUST return a dictionary"
        )
    if salt_factories_config:
        log.debug(
            'Salt Factories Manager Default Config:\n%s',
            pprint.pformat(_salt_factories_config),
        )
        log.debug(
            'Salt Factories Manager User Config:\n%s',
            pprint.pformat(salt_factories_config),
        )
    factories_config = _salt_factories_config.copy()
    factories_config.update(salt_factories_config)
    log.debug(
        'Instantiating the Salt Factories Manager with the following keyword arguments:\n%s',
        pprint.pformat(factories_config),
    )
    factories_config.setdefault('root_dir', tempdir)
    return FactoriesManager(
        stats_processes=stats_processes,
        event_listener=event_listener,
        **factories_config,
    )
