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

    if distribution in ["debian"]:
        if codename in ["stretch"]:
            assert all(
                [
                    host.package(pkg).is_installed
                    for pkg in [
                        "docker-ce",
                        "docker-compose",
                        "python-docker",
                    ]
                ]
            )
        elif codename in ["buster", "bullseye"]:
            assert all(
                [
                    host.package(pkg).is_installed
                    for pkg in [
                        "docker-ce",
                        "docker-compose-plugin",
                        "python3-docker",
                    ]
                ]
            )
        elif codename in ["bookworm"]:
            assert all(
                [
                    host.package(pkg).is_installed
                    for pkg in ["docker.io", "docker-compose", "python3-docker"]
                ]
            )
        else:
            assert False, f"Unknown codename {codename}"
    elif distribution in ["kali"]:
        assert all(
            [
                host.package(pkg).is_installed
                for pkg in ["docker.io", "docker-compose", "python3-docker"]
            ]
        )
    elif distribution in ["ubuntu"]:
        assert all(
            [
                host.package(pkg).is_installed
                for pkg in [
                    "docker-ce",
                    "docker-compose-plugin",
                    "python3-docker",
                ]
            ]
        )
    elif distribution in ["amzn", "fedora"]:
        assert all(
            [
                host.package(pkg).is_installed
                for pkg in ["docker-compose", "moby-engine", "python3-docker"]
            ]
        )
    else:
        assert False, f"Unknown distribution {distribution}"


@pytest.mark.parametrize("svc", ["docker"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled


@pytest.mark.parametrize("command", ["docker-compose version"])
def test_commands(host, command):
    """Test that appropriate commands are available."""
    distribution = host.system_info.distribution
    codename = host.system_info.codename

    if distribution in ["debian"]:
        if codename in ["buster", "bullseye"]:
            assert host.run("docker compose version").rc == 0
        elif codename in ["stretch", "bookworm"]:
            assert host.run("docker-compose version").rc == 0
        else:
            assert False, f"Unknown codename {codename}"
    elif distribution in ["amzn", "fedora", "kali"]:
        assert host.run("docker-compose version").rc == 0
    elif distribution in ["ubuntu"]:
        assert host.run("docker compose version").rc == 0
    else:
        assert False, f"Unknown distribution {distribution}"
