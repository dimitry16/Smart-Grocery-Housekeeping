from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_msg():
    return {"msg": "Hello World!"}
