# `app.k8s_bootstrap.kubelet`

Роль устанавливает `kubelet` из репозитория `pkgs.k8s.io`, отключает swap и фиксирует пакет в состоянии `hold`.

## Используемые зависимости

- `ansible-core` 2.14+;
- ОС Debian/Ubuntu с `apt`;
- доступ в сеть к `pkgs.k8s.io` для ключа и репозитория Kubernetes;
- дополнительные Ansible Collection не требуются (используются модули `ansible.builtin`).

## Переменные роли

| Переменная | Тип | Значение по умолчанию |
| --- | --- | --- |
| `kubernetes_version` | `str` | `"v1.35"` |

## Пример использования роли в плейбуке

```yaml
- name: Install kubelet
  hosts: all
  become: true
  roles:
    - role: app.k8s_bootstrap.kubelet
```

## Переопределение переменных

```yaml
- name: Install kubelet with custom channel
  hosts: all
  become: true
  vars:
    kubernetes_version: "v1.36"
  roles:
    - role: app.k8s_bootstrap.kubelet
```
