# Kubernetes: Deployment и Service

## Как это связано между собой

1. **Deployment** создаёт Pod’ы с контейнером приложения и задаёт:
   - образ (`image`), число реплик (`replicas`);
   - переменные окружения (например `PORT`);
   - **liveness/readiness probes** по HTTP на `/info`, чтобы kubelet понимал, жив ли контейнер и можно ли слать ему трафик.

2. У каждого Pod’а в шаблоне есть **метка** `app: yadro-currency-api` (поле `template.metadata.labels`).

3. **Service** с типом `ClusterIP`:
   - **не знает** про Deployment по имени;
   - выбирает все Pod’ы с метками из `spec.selector` (`app: yadro-currency-api`);
   - даёт им **один виртуальный IP и DNS-имя** внутри кластера и балансирует трафик между репликами.

**Направление трафика:** клиент → **Service** (DNS/IP) → один из Pod’ов. Deployment к Service сам не обращается — он только поддерживает нужное число Pod’ов.

## Перед запуском

1. Образ должен быть **доступен узлам кластера** (публичный registry или свой + `imagePullSecrets`).
2. В `deployment.yaml` в поле `spec.template.spec.containers[0].image` укажите **тот же образ и тег**, что после `docker push` (можно синхронизировать с переменной `IMAGE_TAG` из корневого `.env`, заменив хвост тега в строке образа).

## Применить манифесты

Из корня репозитория или из каталога `k8s/`:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

Проверка:

```bash
kubectl get pods,svc -l app=yadro-currency-api
kubectl logs -l app=yadro-currency-api --tail=50
```

## Проверка доступа к `/info`

Сервис доступен только **изнутри** кластера (ClusterIP). С машины с `kubectl`:

```bash
kubectl port-forward svc/yadro-currency-api 8080:80
```

В другом терминале:

```bash
curl -sS http://127.0.0.1:8080/info
```

Или одноразовый Pod с curl:

```bash
kubectl run curl-test --rm -it --restart=Never --image=curlimages/curl:latest -- \
  curl -sS http://yadro-currency-api.default.svc.cluster.local/info
```

(если используете не `default`, замените имя namespace в URL).

## Дальше

- Увеличить `spec.replicas` в Deployment для отказоустойчивости.
- Добавить Ingress и Ingress Controller для доступа **снаружи** кластера.
