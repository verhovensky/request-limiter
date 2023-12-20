## Request Limiter
Simple request limiter based on Redis cache and Celery

### Using docker:

1) Clone repository and create .env file and fill in variables \
Examples provided in example_env file

2) Use docker compose
```shell
docker compose -f docker-compos.prod.yml
```

3) App URL
```
http://127.0.0.1:8000
```

```shell
Swagger URL
http://127.0.0.1:8000/docs

Flower URL
http://127.0.0.1:5556/
```


### Development

For local development

1) Clone repository and create .env file and fill in variables
Examples provided in example_env file

2) Create venv (IDE / manually)

3) In the root of project run commands
```shell
python -m pip install poetry && poetry install
```
4) Run app in IDE / manually
```shell
python -m uvicorn main:app --reload
```
5) Run Redis container
```shell
docker compose -f docker-compos.dev.yml
```

6) Run services, first Celery
```shell
celery -A worker.celery worker -Q celery,high_priorit --loglevel=debug
```

7) Then Flower
```shell
celery -A worker.celery flower --port=5555 --loglevel=debug
```

### TODOs
* More Unit Tests (services)
* Flower Basic HTTP Auth / 2FA protection
* YAML configs for loading tests with Artillery
* JSON Logging
* Refactor to using aiojobs tasks (remove sync decorator)
* Admin panel
* Task result storage view (?)
* RabbitMQ integration (?)