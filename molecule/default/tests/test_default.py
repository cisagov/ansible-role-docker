"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename
    if (distribution == "debian" and codename is None) or distribution == "kali":
        # Debian Bullseye is not yet supported by the official Docker
        # package repo
        assert host.package("docker.io").is_installed
    elif distribution == "fedora":
        assert host.package("moby-engine").is_installed
    else:
        assert host.package("docker-ce").is_installed


@pytest.mark.parametrize("svc", ["docker"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled


@pytest.mark.parametrize("pkg", ["docker-compose", "docker"])
def test_pip_packages(host, pkg):
    """Test that the appropriate pip packages were installed."""
    assert pkg in host.pip_package.get_packages(pip_path="pip3")


@pytest.mark.parametrize("command", ["docker-compose version"])
def test_command(host, command):
    """Test that appropriate commands are available."""
    assert host.run(command).rc == 0
