# PLAN
# create diagram showing app1, app2, app3, Dapr, SQL,
# external service. It needs to show what is using DAPR and what is not

# show DB comms and resiliency using this app.py, but simplify it

# show external service comms and resiliency using FastAPI app in app3.py
# https://docs.dapr.io/developing-applications/building-blocks/service-invocation/howto-invoke-non-dapr-endpoints/

# show internal service comms and resiliency using Flask app in app2.py

# How do I present timeouts? retries is easy, circuit breaker too. But timeouts?
# I can modify FastAPI or Flask app to show timeouts.

import json
import os

import requests
from flask import Flask

app = Flask(__name__)

app_port = os.getenv("APP_PORT", "5001")
dapr_port = os.getenv("DAPR_HTTP_PORT", "4001")
base_url = os.getenv("BASE_URL", "http://localhost")
cron_binding_name = "cron"
sql_binding_name = "sqldb"
dapr_url = "%s:%s/v1.0/bindings/%s" % (base_url, dapr_port, sql_binding_name)


# Triggered by Dapr input binding
@app.route("/" + cron_binding_name, methods=["POST"])
def process_batch():

    print("Processing batch..", flush=True)

    for order_line in [
        {"orderid": 1, "customer": "John Doe", "price": 42},
        {"orderid": 2, "customer": "Jane Doe", "price": 43},
    ]:
        sql_output(order_line)

    print("Finished processing batch", flush=True)

    print("Calling internal service", flush=True)
    requests.post(
        f"http://localhost:{dapr_port}/v1.0/invoke/app2/method/orders",
        json={"orderid": 1, "customer": "John Doe", "price": 42},
    )

    print("Calling external service", flush=True)

    requests.post(
        "http://localhost:5003/notifications",
        json={"orderid": 1, "customer": "John Doe", "price": 42},
    )

    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


# insert two hard coded orders into a SQL database
def sql_output(order_line):

    sqlCmd = (
        "insert into orders (orderid, customer, price) values "
        + "(%s, '%s', %s)"
        % (order_line["orderid"], order_line["customer"], order_line["price"])
    )
    # TODO: I have to read on this. I don't know what this is doing
    payload = '{"operation": "exec", "metadata": {"sql" : "%s"} }' % sqlCmd

    try:
        # Insert order using Dapr output binding via HTTP Post
        resp = requests.post(dapr_url, payload)
        resp.raise_for_status()
        print(f"💪 {sqlCmd} executed 💪", flush=True)
        return resp

    except requests.exceptions.RequestException as e:
        print(e, flush=True)

        # error response from DAPR is in JSON format
        # error should include errorCode whcih is the reason.
        # is reason is ERR_INVOKE_OUTPUT_BINDING we are cool
        # log message circuit breaker is open
        # TODO: how to handle circuit breaker open?
        print(e.response.text, flush=True)
        print("💥 Circuit breaker is open 💥", flush=True)
        print("STOP SIGN when circuit breaker prevents call? so open")
        raise SystemExit(e)


app.run(port=app_port)
