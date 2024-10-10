import random
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

request_counter = 0


@app.get("/orders")
async def get_order(request: Request):
    request_count = request.query_params.get("request_count")
    print(f"Order received with request count: {request_count}", flush=True)
    return JSONResponse(content={"success": True}, status_code=200)


@app.get("/overload")
async def get_constraint(request: Request):
    request_count = request.query_params.get("request_count")
    print(f"Overload request received with request count: {request_count}", flush=True)

    # Simulate a long delay
    time.sleep(5)

    # Simulate a 50% chance of failure
    # if random.random() < 0.2:
    #     return JSONResponse(
    #         content={"success": False, "error": "Service failed"},
    #         status_code=500,
    #     )

    return JSONResponse(
        content={"success": True, "constraint": "Some constraint data"},
        status_code=200,
    )


@app.get("/always-fail")
async def always_fail(request: Request):
    global request_counter
    request_counter += 1
    request_count = request.query_params.get("request_count")
    print(f"Overload request received with request count: {request_count}", flush=True)

    if request_counter % 4 == 0:
        return JSONResponse(content={"success": True}, status_code=200)
    else:
        # Generate a random 5xx error code
        error_code = random.choice([500, 501, 502, 503, 504, 505])
        return JSONResponse(
            content={
                "success": False,
                "error": f"Service failed with error code {error_code}",
            },
            status_code=error_code,
        )
