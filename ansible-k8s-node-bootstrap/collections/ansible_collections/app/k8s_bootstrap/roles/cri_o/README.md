# `app.k8s_bootstrap.cri_o`

Роль устанавливает CRI-O из OpenSUSE Build Service (OBS) на Debian/Ubuntu хосты для подготовки Kubernetes-узла.

## Используемые зависимости

- `ansible-core` 2.14+;
- ОС Debian/Ubuntu с `apt`;
- доступ в сеть к `download.opensuse.org` для ключа и репозитория CRI-O;
- дополнительные Ansible Collection не требуются (используются модули `ansible.builtin`).

## Переменные роли

| Переменная | Тип | Значение по умолчанию |
| --- | --- | --- |
| `crio_version` | `str` | `"v1.35"` |

## Пример использования роли в плейбуке

```yaml
- name: Install CRI-O
  hosts: all
  become: true
  roles:
    - role: app.k8s_bootstrap.cri_o
```

## Переопределение переменных

```yaml
- name: Install CRI-O with custom channel
  hosts: all
  become: true
  vars:
    crio_version: "v1.33"
  roles:
    - role: app.k8s_bootstrap.cri_o
```
