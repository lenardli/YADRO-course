"""Role tests: kubeadm package, version, and hold."""


def test_kubeadm_package_installed(host):
    """Пакет kubeadm установлен."""
    assert host.package("kubeadm").is_installed


def test_kubeadm_version(host):
    """Версия kubeadm соответствует каналу репозитория (defaults: v1.35)."""
    cmd = host.run("kubeadm version -o short")
    assert cmd.rc == 0
    assert "v1.35" in cmd.stdout


def test_kubeadm_package_held(host):
    """Пакет kubeadm зафиксирован (hold)."""
    cmd = host.run("dpkg --get-selections | grep kubeadm")
    assert cmd.rc == 0
    assert "hold" in cmd.stdout