# README

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
