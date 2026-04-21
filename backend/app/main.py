from fastapi import FastAPI

from app.food_items import router

app = FastAPI()

app.include_router(router.router, prefix="/v1/food-items", tags=["Food Items"])


# Routers
@app.get("/")
def read_msg():
    return {"message": "Navigate to /food-items"}
