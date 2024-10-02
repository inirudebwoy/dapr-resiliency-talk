from fastapi import FastAPI

app = FastAPI()


@app.post("/notifications")
def read_root():
    return {"Hello": "World"}
