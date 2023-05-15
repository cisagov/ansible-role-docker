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

    if distribution in ["debian", "fedora", "kali", "ubuntu"]:
        assert all(
            [
                host.package(pkg).is_installed
                for pkg in [
                    "containerd.io",
                    "docker-ce",
                    "docker-ce-cli",
                    "docker-compose-plugin",
                    "pass",
                    "python3-docker",
                ]
            ]
        )
    elif distribution in ["amzn"]:
        assert all([host.package(pkg).is_installed for pkg in ["docker"]])
    else:
        assert False, f"Unknown distribution {distribution}"


@pytest.mark.parametrize("svc", ["docker"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled


def test_commands(host):
    """Test that appropriate commands are available."""
    assert host.run("docker compose version").rc == 0
