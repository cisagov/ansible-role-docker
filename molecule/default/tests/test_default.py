"""Module containing the tests for the default scenario."""

import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["docker-ce"])
def test_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize("serv", ["docker"])
def test_services(host, serv):
    """Test that appropriate services are running."""
    assert host.service(serv).is_enabled


@pytest.mark.parametrize("command", ["docker-compose version"])
def test_command(host, command):
    """Test that appropriate commands are available."""
    assert host.run(command).rc == 0
