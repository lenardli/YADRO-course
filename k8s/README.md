# Развертывание приложения в k8s

В каталоге `k8s/` манифесты приложения (`deployment` / `service` / `ingress`), **конфигурациz системного nginx** перед кластером (`nginx-k8s-ingress-proxy.conf`).


| Файл                           | Роль                                                                                                |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| `deployment.yaml`              | Запуск приложения в контейнерах, **2 реплики**, обновления и самовосстановление Pod’ов              |
| `service.yaml`                 | **Внутренний** адрес и балансировка между репликами (**ClusterIP**)                                 |
| `ingress.yaml`                 | путь `/` → сервис приложения через **Ingress Controller** класса `nginx`                            |
| `nginx-k8s-ingress-proxy.conf` | Конфиг **nginx для каждой ноды с подами**, снаружи **:80**, внутрь — ноды **:NodePort** контроллера |


---

### `deployment.yaml`

- `**replicas: 2`.** Минимальная отказоустойчивость: при падении одного Pod’а второй продолжает обслуживать запросы.
- Метка `app: yadro-currency-api` совпадает с селектором Service.
- **Порт контейнера 8000 и переменная** `PORT`**,**  чтобы приложение могло читать порт из окружения.
- **Именованный порт `http`.** На него ссылаются пробы и `targetPort` у Service.
- `**readinessProbe`** **и** `**дivenessProbe`** пробы на ручку `/info` для мониторинга состояния подов и контейнеров.
- `**imagePullPolicy: IfNotPresent`.** - с учетом частой ошибки pull limited в Docker, выбрана политика сначала искать локальный образ, и если его нет, пулить из Docker Hub.
- **Security context:** не-root (65532), `readOnlyRootFilesystem`, снятие всех capabilities, вся файловая система контейнера доступна только для чтение, кроме `/tmp`, который смонтирован в /tmp ноды.
- `**resources.requests` / `limits`** - ограничение ресурсов CPU и RAM для контейнеров.

### `service.yaml`

- `**type: ClusterIP`.** Одно DNS-имя и виртуальный IP **внутри** кластера.

**Селектор по меткам Pod’ов -**  `app: yadro-currency-api`.

- **Порт сервиса 80 и `targetPort: http`.**  Ingress обращается к сервису на **80**, а не к порту контейнера напрямую.

### `ingress.yaml`

- `**ingressClassName: nginx`.** 
- **Путь `/` и `pathType: Prefix`.**
- **Backend:** `service` **и порт 80.**

### `nginx-k8s-ingress-proxy.conf`

- 

- `**upstream k8s_ingress_http`.** Перечень **backend’ов для прокси**.
- `least_conn` — выбор апстрима с меньшей текущей нагрузкой.
- `**keepalive`** — переиспользование соединений к upstream, меньше накладных расходов на TCP.
- `proxy_pass http://k8s_ingress_http`**.** Отправляет запрос на нодовый NodePort nginx-ingress контроллера.

---

## Проверка доступа к приложению

### Внутри кластера

```bash
kubectl port-forward svc/yadro-currency-api 8080:80
```

```bash
curl -sS http://127.0.0.1:8080/info
```

### Снаружи (Ingress)

```bash
http://<IP-address>/info
```

---

