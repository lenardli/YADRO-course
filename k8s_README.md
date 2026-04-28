## Установка Kubernetes 1.35 + CRI-O 1.35 + CALICO

Дополнительный источник при установке: [https://habr.com/ru/articles/725640/](https://habr.com/ru/articles/725640/)

## 1. Основные шаги установки

### 1.1 Подготовка системы на узлах

Перед запуском `kubeadm` привести все узлы к одинаковому базовому состоянию:

1. Настроить статическую IP-конфигурацию.
2. Назначить уникальные hostname:
  - `master`
  - `worker-1`
  - `worker-2`
3. Настроить локальный DNS-резолвинг имя->IP через `/etc/hosts` на всех узлах:
  - `10.184.0.61 master`
  - `10.184.0.62 worker-1`
  - `10.184.0.63 worker-2`
4. Отключить swap.
5. Загрузить модули ядра:
  - `overlay`
  - `br_netfilter`
6. Применить sysctl-параметры:
  - `net.ipv4.ip_forward=1`
  - `net.bridge.bridge-nf-call-iptables=1`
  - `net.bridge.bridge-nf-call-ip6tables=1`

### 1.2 Установка пакетов Kubernetes и CRI-O

Установку выполнить в следующем порядке:

1. Подготовить менеджер пакетов (`apt`) и ключи репозиториев.
2. Добавить зеркальные репозитории:
  - Kubernetes: `https://mirrors.aliyun.com/kubernetes-new/core/stable/v1.35/deb/`
  - CRI-O: `https://mirrors.aliyun.com/kubernetes-new/addons:/cri-o:/stable:/v1.35/deb/`
3. Обновить индекс пакетов (`apt update`).
4. Дополнительно установить пакеты подготовки репозиториев и TLS:
  - `apt-transport-https`
  - `ca-certificates`
  - `curl`
  - `gnupg`
5. Установить необходимые пакеты:
  - `kubeadm (только на master)`
  - `kubelet`
  - `kubectl`
  - `cri-o`
  - `cri-tools`
6. Включить сервисы:
  - `systemctl enable --now crio`
  - `systemctl enable --now kubelet`
7. Зафиксировать версии Kubernetes-компонентов:
  - `apt-mark hold kubelet kubeadm kubectl`

### 1.3 Инициализация control-plane

На master для инициализации использовать файл `/etc/kubernetes/kubeadm-config.yaml`.

Команда запуска:

- `kubeadm init --config /etc/kubernetes/kubeadm-config.yaml`

Содержимое файла:

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
nodeRegistration:
  name: master
  criSocket: unix:///var/run/crio/crio.sock
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
kubernetesVersion: v1.35.4
networking:
  podSubnet: 10.244.0.0/16
```

### 1.4 Присоединение worker-нод

Worker-узлы присоединить через `kubeadm join` с обязательным параметром:

- `--cri-socket unix:///var/run/crio/crio.sock`

---

## 2. Проблемы в процессе и их решение

### Проблема 1: пакеты из официального репозитория `pkgs.k8s.io` не устанавливаются

#### Симптомы

В логах apt:

- Connection timeout при подключении к `pkgs.k8s.io`

#### Причина

Сетевая недопуступность `pkgs.k8s.io`  

Решение  

- Использовать зеркало `mirrors.aliyun.com (сначала пробовался snap, но из-за проблем с безопасностью и проблем с запуском контейнеров был удален)`

### Проблема 2: kubelet пытался использовать containerd вместо CRI-O

#### Симптомы

В логах kubelet:

- попытка подключения к `/run/containerd/containerd.sock`;
- ошибка `no such file or directory`.

#### Причина

На узле kubelet был запущен с endpoint на containerd, хотя runtime должен быть CRI-O.

#### Решение

- Указать `criSocket` как `unix:///var/run/crio/crio.sock` в `kubeadm init` и `kubeadm join`;
- Выполнить `kubeadm reset -f` и повторный `kubeadm join`.

### Проблема 3: `kubeadm` не запускался из-за старой snap-ссылки

#### Симптомы

- `-bash: /snap/bin/kubeadm: No such file or directory`.

#### Причина

В shell оставалась старая привязка к snap-версии.

#### Решение

- Убедиться, что `kubeadm` установлен через apt;
- Сбросить shell cache (`hash -r`);
- Проверить путь и версию команды.

### Проблема 4: `worker-1` был в состоянии `NotReady`

#### Симптомы

- Node status: `Unknown/NotReady`;
- kubelet переставал отправлять heartbeat.

#### Причина

На узле была нарушена локальная kubeadm-конфигурация kubelet.

#### Решение

- Выполнить `kubeadm reset -f`;
- Очистить kubelet/CNI данные;
- Выполнить повторный `kubeadm join`.

### Проблема 5: Calico не запускался на worker из-за pull ошибок

#### Симптомы

- `calico-node` в `Init:ImagePullBackOff`;
- ошибки `toomanyrequests` (Docker Hub rate limit);

#### Причина

Часть образов Calico тянулась с Docker Hub (`docker.io/calico/...`), где срабатывал лимит (`toomanyrequests`).

#### Решение

- Перевести образы Calico на доступный registry (`quay.io`) для:
  - `calico/node`;
  - `calico/cni`;
  - `calico/kube-controllers`.
- Отдельно обновить init-контейнер `mount-bpffs`, который оставался на `docker.io`.
- Проверить, что все `calico-node` перешли в состояние `Running` на всех нодах.

```bash

kubectl -n kube-system set image daemonset/calico-node \

  calico-node=quay.io/calico/node:v3.27.0 \

  upgrade-ipam=quay.io/calico/cni:v3.27.0 \

  install-cni=quay.io/calico/cni:v3.27.0

kubectl -n kube-system set image deployment/calico-kube-controllers \

  calico-kube-controllers=quay.io/calico/kube-controllers:v3.27.0

```

### Проблема 6: тестовый pod запускался, но DNS внутри pod не работал

#### Симптомы

- pod `Running`, интернет по IP (`wget http://1.1.1.1`) работает;
- `nslookup kubernetes.default.svc.cluster.local` -> timeout.
- `nslookup google.com` -> timeout.

#### Причина

Проблема внутрикластерной сети/DNS пути (межподовое взаимодействие и доступ к CoreDNS/API), при том что egress по IP уже работал.

#### Решение

- Проверить сервис `kube-dns` (`10.96.0.10`) и endpoints;
- Проверить `resolv.conf` в pod (`nameserver 10.96.0.10`);
- Проверить логи `kube-proxy` и `CoreDNS`;
- Перезапустить CoreDNS: `kubectl rollout restart deployment -n kube-system coredns`.

### Проблема 7: permission denied при ping внутри контейнера

Симптомы: 

- при выполнении `ping 8.8.8.8` внутри созданного тестового контейнера возникает ошибка:  permission denied (are you root?)

Причина:

- Отсутствие capability NET_RAW у cri-o

Решение:

- [https://habr.com/ru/companies/yadro/articles/914026/](https://habr.com/ru/companies/yadro/articles/914026/)

---

## 3. Команды проверки, которые использовались

- `kubectl get nodes -o wide` — проверить, что все ноды в `Ready`, и увидеть их IP/версии.
- `kubectl get pods -A -o wide` — посмотреть общее состояние всех pod во всех namespace.
- `kubectl -n kube-system get pods -o wide | rg "calico|coredns|kube-proxy"` — быстро проверить ключевые системные компоненты сети и DNS.
- `kubectl describe pod <pod>` — получить подробную диагностику pod (events, причины `Pending`, `CrashLoopBackOff`, `ImagePullBackOff`).
- `kubectl exec -it <pod> -- nslookup ...` — проверить DNS-резолвинг изнутри pod.
- `kubectl exec -it <pod> -- wget -S -O- http://1.1.1.1 --timeout=5` — проверить исходящую сеть из pod по IP (без DNS).
- `journalctl -u kubelet -n 200 --no-pager` — посмотреть последние ошибки/предупреждения kubelet на ноде.
- `crictl --runtime-endpoint unix:///var/run/crio/crio.sock info` — убедиться, что CRI-O runtime отвечает корректно.





