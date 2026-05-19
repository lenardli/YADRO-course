# Развертывание приложения в k8s

В каталоге `k8s-deploy-app/` манифесты приложения (`deployment` / `service` / `ingress`), Helm-чарт `yadro-currency-app/`, манифесты Argo CD (`application-app.yml`, `application-imageupdater.yml`), конфигурация системного nginx перед кластером (`nginx-k8s-ingress-proxy.conf`).

Текущий экземпляр Argo CD в UI: [https://10.184.0.61:31951](https://10.184.0.61:31951).


| Файл                           | Роль                                                                                                |
| ------------------------------ | --------------------------------------------------------------------------------------------------- |
| `yadro-currency-app/`          | Helm-чарт: `values.yaml`, шаблоны в `templates/` (в т.ч. `deployment` / `service` / `ingress`)     |
| `application-app.yml`        | Ресурс Argo CD Application (`yadro-currency-api`): Git-источник, ветка `targetRevision`, путь к чарту, namespace default |
| `application-imageupdater.yml` | Ресурс ImageUpdater: semver, `allowTags` под теги вида `v1.0.1-<7 hex>-<14 цифр>`, запись в `values.yaml`, MR в GitLab (`pullRequest.gitlab`), секреты `pullSecret` (Docker Hub) и `git:secret:...` (push/MR) |
| `deployment.yaml`              | Запуск приложения в контейнерах, 2 реплики, обновления и самовосстановление Pod’ов                   |
| `service.yaml`                 | Внутренний адрес и балансировка между репликами (ClusterIP)                                          |
| `ingress.yaml`                 | путь `/` → сервис приложения через Ingress Controller класса `nginx`                                 |
| `nginx-k8s-ingress-proxy.conf` | Конфиг nginx для каждой ноды с подами, снаружи :80, внутрь — ноды :NodePort контроллера              |


---

### Каталог `yadro-currency-app/`

- Назначение — один Helm-чарт приложения: из него Argo CD рендерит манифесты в namespace default.
- `Chart.yaml` — имя чарта, версия чарта и appVersion.
- `values.yaml` — реплики, образ (`image.repository` / `image.tag`), сервис, ingress, ресурсы, пробы, `fullnameOverride` и т.д.
- `templates/` — `deployment.yaml`, `service.yaml`, `ingress.yaml`, вспомогательный `_helpers.tpl`; `NOTES.txt` — подсказки после `helm install`.
- `.helmignore` — файлы, не попадающие в пакет чарта при упаковке.

### `application-app.yml`

- Тип ресурса — `argoproj.io/v1alpha1`, Application, имя `yadro-currency-api`, namespace `argocd`.
- `spec.source` — `repoURL` GitLab, `path:` `k8s-deploy-app/yadro-currency-app`, `targetRevision:` ветка или тег в репозитории с чартом.
- `spec.destination` — кластер `https://kubernetes.default.svc`, namespace `default`.
- `syncPolicy.automated` — автосинк, prune и selfHeal включены.

### `application-imageupdater.yml`

- Тип ресурса — `argocd-image-updater.argoproj.io/v1alpha1`, ImageUpdater, namespace `argocd`; по `namePattern` выбирается приложение `yadro-currency-api`.
- Образ Docker Hub — поле `imageName` (репозиторий/тег); `updateStrategy: semver`, `allowTags` — regexp только для тегов вида `vX.Y.Z-<7 hex>-<14 цифр>`; `forceUpdate: true` помогает, если в `Application.status` ещё нет сводки по образам; `pullSecret` — доступ к registry.
- `manifestTargets.helm` — при обновлении пишутся ключи `image.repository` и `image.tag` в `values.yaml`.
- `writeBackConfig` — `git:secret:...` для push/MR, `gitConfig.repository` и `branch` (база для MR), `writeBackTarget:` `helmvalues:.../values.yaml`, `pullRequest.gitlab` — создание merge request в GitLab.

---

### `deployment.yaml`

- replicas: 2 — минимальная отказоустойчивость: при падении одного Pod’а второй продолжает обслуживать запросы.
- Метка `app: yadro-currency-api` совпадает с селектором Service.
- Порт контейнера 8000 и переменная `PORT`, чтобы приложение могло читать порт из окружения.
- Именованный порт http. На него ссылаются пробы и `targetPort` у Service.
- readinessProbe и livenessProbe: пробы на ручку `/info` для мониторинга состояния подов и контейнеров.
- imagePullPolicy: IfNotPresent — с учетом частой ошибки pull limited в Docker, выбрана политика сначала искать локальный образ, и если его нет, пулить из Docker Hub.
- Security context: не-root (65532), `readOnlyRootFilesystem`, снятие всех capabilities, вся файловая система контейнера доступна только для чтение, кроме `/tmp`, который смонтирован в /tmp ноды.
- resources.requests / limits — ограничение ресурсов CPU и RAM для контейнеров.

### `service.yaml`

- type: ClusterIP — одно DNS-имя и виртуальный IP внутри кластера.
- Селектор по меткам Pod’ов — `app: yadro-currency-api`.
- Порт сервиса 80 и targetPort: http. Ingress обращается к сервису на 80.

### `ingress.yaml`

- ingressClassName: nginx.
- Путь `/` и `pathType: Prefix`.
- Backend: `service` и порт 80.

### `nginx-k8s-ingress-proxy.conf`

- upstream k8s_ingress_http — перечень backend’ов для прокси.
- least_conn — выбор апстрима с меньшей текущей нагрузкой.
- keepalive — переиспользование соединений к upstream, меньше накладных расходов на TCP.
- proxy_pass http://k8s_ingress_http — отправляет запрос на нодовый NodePort nginx-ingress контроллера.

---

## Проверка доступа к приложению

### Внутри кластера

`kubectl port-forward svc/yadro-currency-api 8080:80`

`curl -sS http://127.0.0.1:8080/info`

### Снаружи

`http://<IP-address>/info`
