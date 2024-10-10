import json
import os

import requests
from flask import Flask, request

app = Flask(__name__)

app_port = os.getenv("APP_PORT", "5001")
dapr_port = os.getenv("DAPR_HTTP_PORT", "4001")
base_url = os.getenv("BASE_URL", "http://localhost")
cron_binding_name = "cron"
sql_binding_name = "sqldb"
dapr_url = "%s:%s/v1.0/bindings/%s" % (base_url, dapr_port, sql_binding_name)

# Global counter for requests to /start endpoint
request_counter = 0


@app.route("/start", methods=["POST"])
def process_batch():
    global request_counter
    request_counter += 1

    data = request.get_json()
    scenario = data.get("scenario", "default")

    for order_line in [
        {"orderid": 1, "customer": "John Doe", "price": 42},
    ]:
        sql_output(order_line)

    endpoint = "orders"
    # scenario for one off network issues.
    if scenario == "overload":
        # scenario for showing retries, and queueing
        endpoint = "overload"
    elif scenario == "always-fail":
        # scenario for showing circuit breaker
        endpoint = "always-fail"

    print(f"🧮 {request_counter=}", flush=True)

    try:
        r = requests.get(
            f"http://localhost:{dapr_port}/v1.0/invoke/resilient-internal/method/{endpoint}",
            params={"request_count": request_counter},
        )
        r.raise_for_status()
    except:
        print("🚨 Internal service failed 🚨", flush=True)
    else:
        print("🚀 Internal service called 🚀", flush=True)

    try:
        r = requests.get(
            f"http://localhost:{dapr_port}/v1.0/invoke/external-service/method/{endpoint}",
            params={"request_count": request_counter},
        )
        r.raise_for_status()
    except:
        print("🚨 External service failed 🚨", flush=True)
    else:
        print("🚀 External service called 🚀", flush=True)

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


def sql_output(order_line):
    sqlCmd = (
        "insert into orders (orderid, customer, price) values "
        + "(%s, '%s', %s)"
        % (order_line["orderid"], order_line["customer"], order_line["price"])
    )
    payload = '{"operation": "exec", "metadata": {"sql" : "%s"} }' % sqlCmd

    resp = requests.post(dapr_url, payload)
    resp.raise_for_status()
    print(f"💪 {sqlCmd} executed 💪", flush=True)
    return resp


app.run(port=app_port)
