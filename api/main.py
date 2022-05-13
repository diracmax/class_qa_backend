import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def read_root():
    return JSONResponse(
        content={"Hello": "Taro"}
    )


uvicorn.run(app=app, host="0.0.0.0", port=80)
