# `app.k8s_bootstrap.kubeadm`

Роль устанавливает `kubeadm` из репозитория `pkgs.k8s.io` и фиксирует пакет в состоянии `hold`.

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
- name: Install kubeadm on masters
  hosts: all
  become: true
  roles:
    - role: app.k8s_bootstrap.kubeadm
      when: inventory_hostname in groups['masters']
```

## Переопределение переменных

```yaml
- name: Install kubeadm with custom channel
  hosts: all
  become: true
  vars:
    kubernetes_version: "v1.36"
  roles:
    - role: app.k8s_bootstrap.kubeadm
      when: inventory_hostname in groups['masters']
```
