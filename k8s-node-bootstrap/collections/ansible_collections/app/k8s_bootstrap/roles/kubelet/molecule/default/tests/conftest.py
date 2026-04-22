"""PyTest fixtures for Molecule + testinfra (avoid clashing with pytest-testinfra's testinfra_hosts)."""

import os

import pytest


@pytest.fixture(scope="module")
def ansible_hosts():
    try:
        import testinfra
    except ImportError:
        pytest.skip("Test requires testinfra", allow_module_level=True)
    path = os.environ.get("MOLECULE_INVENTORY_FILE")
    if not path:
        pytest.skip("Run from molecule", allow_module_level=True)
    from testinfra.utils.ansible_runner import AnsibleRunner

    return AnsibleRunner(path).get_hosts("all")


@pytest.fixture(scope="module")
def host(ansible_hosts):
    return ansible_hosts[0]