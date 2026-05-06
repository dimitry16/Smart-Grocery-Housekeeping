from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.food_items import router

app = FastAPI()

app.include_router(router.router, prefix="/v1/food-items", tags=["Food Items"])

# CORS Middleware edited by Zilin Xu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite's default port
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
@app.get("/")
async def read_msg():
    return {"message": "Navigate to /food-items"}
