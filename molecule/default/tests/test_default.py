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


# testinfra currently incorrectly identifies the service provider in
# our Docker containers because of philpep/testinfra#416, so we have
# to leave this test commented out for now.
# @pytest.mark.parametrize("svc", ["docker"])
# def test_services(host, svc):
#     """Test that the services were enabled."""
#     assert host.service(svc).is_enabled
#     assert host.service(svc).is_running


@pytest.mark.parametrize("command", ["docker-compose version"])
def test_command(host, command):
    """Test that appropriate commands are available."""
    assert host.run(command).rc == 0
