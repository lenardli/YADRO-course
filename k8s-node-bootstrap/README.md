# Ansible-проект `k8s-node-bootstrap`

Проект автоматизирует базовую подготовку Kubernetes-узлов (control-plane и worker) с помощью ролей коллекции `app.k8s_bootstrap`.

В рамках bootstrap выполняются роли:

- `app.k8s_bootstrap.cri_o` - установка контейнерного рантайма CRI-O;
- `app.k8s_bootstrap.kubelet` - установка kubelet;
- `app.k8s_bootstrap.kubeadm` - установка kubeadm (только на хостах из группы `masters`).

## Используемые зависимости

- 

## Переменные проекта

Ниже перечислены пользовательские переменные ролей, которые можно переопределять в `group_vars`/`host_vars` или в самом плейбуке.


| Переменная           | Где используется                                         | Тип   | Значение по умолчанию |
| -------------------- | -------------------------------------------------------- | ----- | --------------------- |
| `crio_version`       | `app.k8s_bootstrap.cri_o`                                | `str` | `"v1.32"`             |
| `kubernetes_version` | `app.k8s_bootstrap.kubelet`, `app.k8s_bootstrap.kubeadm` | `str` | `"v1.35"`             |


## Пример использования роли в плейбуке

Файл `k8s-node-bootstrap.yml`:

```yaml
- name: Bootstrap Kubernetes node (CRI-O, kubelet, kubeadm)
  hosts: all
  become: true
  roles:
    - role: app.k8s_bootstrap.cri_o
    - role: app.k8s_bootstrap.kubelet
    - role: app.k8s_bootstrap.kubeadm
      when: inventory_hostname in groups['masters']
```

Запуск из корня проекта:

```bash
ansible-playbook k8s-node-bootstrap.yml
```

## Переопределение переменных

```yaml
- name: Bootstrap Kubernetes node with custom versions
  hosts: all
  become: true
  vars:
    crio_version: "v1.33"
    kubernetes_version: "v1.35"
  roles:
    - role: app.k8s_bootstrap.cri_o
    - role: app.k8s_bootstrap.kubelet
    - role: app.k8s_bootstrap.kubeadm
      when: inventory_hostname in groups['masters']
```

