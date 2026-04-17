from uuid import uuid4
from app.food_data import food_items
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

app = FastAPI()

# Food Item Schema (for initial crud implementation)
class FoodItemBase(BaseModel):
    name: str
    brand: str
    barcode: str 
    category: str 

class FoodItemCreate(FoodItemBase):
    pass

class FoodItemResponse(BaseModel):
    id: str
    image_url: str
    
    
# Routers
@app.get("/")
async def read_msg():
    return {"msg": "Navigate to food-items"}

@app.get("/food-items", response_model=list[FoodItemBase])
async def get_all_food_items():
    """Read all food items."""
    return food_items

@app.get("/food-items/{food_item_id}", response_model=FoodItemBase)
def get_single_food_item(food_item_id: str):
    """Get a specific food item by their ID

    Args:
        food_item_id (str): uuid of the food item.

    Raises:
        HTTPException: Returns a 404 response if food item does not exist.
    """
    for food_item in food_items:
        if food_item.get("id") == food_item_id:
            return food_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found")

@app.post("/food-items", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(food_item: FoodItemCreate):
    # Creates a uuid
    new_id = uuid4()
    new_food_item = {
        "id": str(new_id), # Convert UUID to a string
        "name": food_item.name,
        "brand": food_item.brand,
        "barcode": food_item.barcode,
        "category": food_item.category,
        "image_url": "https://image-of-food.com/products/",
    }
    
    food_items.append(new_food_item)
    return new_food_item