import json
import random
import time

from flask import Flask, request

app = Flask(__name__)


@app.route("/orders", methods=["GET"])
def getOrder():
    request_count = request.args.get("request_count")
    print(f"Order received with request count: {request_count}", flush=True)
    return json.dumps({"success": True}), 200, {"ContentType": "application/json"}


@app.route("/overload", methods=["GET"])
def getConstraint():
    # Simulate a long delay
    time.sleep(5)

    # Simulate a 50% chance of failure
    # if random.random() < 0.2:
    #     return (
    #         json.dumps({"success": False, "error": "Service failed"}),
    #         500,
    #         {"ContentType": "application/json"},
    #     )

    return (
        json.dumps({"success": True, "constraint": "Some constraint data"}),
        200,
        {"ContentType": "application/json"},
    )


request_counter = 0


@app.route("/always-fail", methods=["GET"])
def alwaysFail():
    global request_counter
    request_counter += 1

    if request_counter % 5 == 0:
        return json.dumps({"success": True}), 200, {"ContentType": "application/json"}
    else:
        # Generate a random 5xx error code
        error_code = random.choice([500, 501, 502, 503, 504, 505])
        return (
            json.dumps(
                {
                    "success": False,
                    "error": f"Service failed with error code {error_code}",
                }
            ),
            error_code,
            {"ContentType": "application/json"},
        )


app.run(port=5002)
