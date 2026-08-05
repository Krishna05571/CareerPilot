from fastapi import FastAPI

app = FastAPI(
    title="CareerPilot API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "CareerPilot Backend Running 🚀"
    }