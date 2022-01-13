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

    # Docker package
    if (
        distribution == "debian" and (codename == "bookworm" or codename is None)
    ) or distribution == "kali":
        # Debian Bookworm is not yet supported by the official Docker
        # package repo
        #
        # https://docs.docker.com/engine/install/debian/
        assert host.package("docker.io").is_installed
    elif distribution == "fedora":
        # Only Moby is available for Feodra 32 and 33
        #
        # https://docs.docker.com/engine/install/fedora/
        assert host.package("moby-engine").is_installed
    else:
        assert host.package("docker-ce").is_installed

    # docker-compose package
    assert host.package("docker-compose").is_installed

    # Docker python library
    if distribution == "debian" and codename == "stretch":
        # Our Stretch AMIs are still using Python 2
        assert host.package("python-docker").is_installed
    else:
        assert host.package("python3-docker").is_installed


@pytest.mark.parametrize("svc", ["docker"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled


@pytest.mark.parametrize("command", ["docker-compose version"])
def test_command(host, command):
    """Test that appropriate commands are available."""
    assert host.run(command).rc == 0
