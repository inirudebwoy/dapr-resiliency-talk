# README

## prerequisites

- `docker`
- `docker-compose`
- `dapr` https://docs.dapr.io/getting-started/install-dapr-cli/


## Running

### DB

To run the database, you need to have `docker` and `docker-compose` installed. Then, you can run the following command:

```bash
cd db
docker compose up
```

### external service

```bash
fastapi dev --port 5003 resilient-external/app.py
```


### DAPR internal service

```bash
dapr run --app-id resilient-internal --app-port 5002 --resources-path ./common-resources -- python resilient-internal/app.py
```

### DAPR db service

```bash
dapr run --app-id resilient-db --app-port 5001 --resources-path ./common-resources,./resilient-db/.dapr/resources -- python resilient-db/app.py
```


## Executing scenarios

### default 

Default scenario, with no errors.
You may trigger error by shutting down the DB.

Execute the following command:
```bash

curl --max-time 2 -X POST http://localhost:5001/start -d '{"scenario":"default"}' -H "Content-Type: application/json"
```

### high latency network

High latency network scenario.

Execute the following command:
```bash

curl --max-time 2 -X POST http://localhost:5001/start -d '{"scenario":"overload"}' -H "Content-Type: application/json"
```

### failing services

Failing services scenario.

Execute the following command:
```bash

curl --max-time 2 -X POST http://localhost:5001/start -d '{"scenario":"always-fail"}' -H "Content-Type: application/json"
```
