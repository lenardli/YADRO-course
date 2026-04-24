"""Role tests: kubelet package, version pin, and hold."""


def test_kubelet_package_installed(host):
    """Пакет kubelet установлен."""
    assert host.package("kubelet").is_installed


def test_kubelet_version(host):
    """Версия kubelet соответствует каналу репозитория (defaults: v1.35)."""
    cmd = host.run("kubelet --version")
    assert cmd.rc == 0
    assert "1.35" in cmd.stdout


def test_kubelet_package_held(host):
    """Пакет kubelet зафиксирован (hold)."""
    cmd = host.run("dpkg --get-selections | grep kubelet")
    assert cmd.rc == 0
    assert "hold" in cmd.stdout


def test_swap_disabled(host):
    """Swap отключен после выполнения роли kubelet."""
    cmd = host.run("swapon --show --noheadings")
    assert cmd.rc == 0
    assert cmd.stdout.strip() == ""
