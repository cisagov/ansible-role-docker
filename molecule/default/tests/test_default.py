import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg", ["docker-ce"])
def test_packages(host, pkg):
    assert host.package(pkg).is_installed


@pytest.mark.parametrize("serv", ["docker"])
def test_services(host, serv):
    assert host.service(serv).is_enabled


@pytest.mark.parametrize("command", ["docker-compose version"])
def test_command(host, command):
    assert host.run(command).rc == 0
