from uuid import uuid4
from ..food_data import food_items_data
from fastapi import APIRouter, HTTPException, status
from ..food_items.schema import FoodItemCreate, FoodItemResponse, FoodItemUpdate


router = APIRouter()


@router.get("", response_model=list[FoodItemResponse])
async def get_all_food_items():
    """Read all food items."""
    return food_items_data


@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(food_item: FoodItemCreate):
    # Creates a uuid
    new_id = str(uuid4())
    new_food_item = {
        "id": str(new_id),  # Convert UUID to a string
        "name": food_item.name,
        "brand": food_item.brand,
        "barcode": food_item.barcode,
        "category": food_item.category,
        "image_url": "https://image-of-food.com/products/",
    }

    food_items_data.append(new_food_item)
    return new_food_item


@router.get("/{food_item_id}", response_model=FoodItemResponse)
async def get_single_food_item(food_item_id: str):
    """Get a specific food item by their ID

    Args:

        food_item_id (str): uuid of the food item.

    Raises:
        HTTPException: Returns a 404 response if food item does not exist.
    """
    for food_item in food_items_data:
        if food_item.get("id") == food_item_id:
            return food_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
    )


@router.patch("/{food_item_id}")
async def update_food_item(food_item_id: str, food_item_update_data: FoodItemUpdate):
    for food_item in food_items_data:
        if food_item["id"] == food_item_id:
            food_item["name"] = food_item_update_data.name
            food_item["brand"] = food_item_update_data.brand
            food_item["barcode"] = food_item_update_data.barcode
            food_item["category"] = food_item_update_data.category
            food_item["image_url"] = food_item_update_data.image_url
            return food_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
    )


@router.delete("/{food_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(food_item_id: str):
    for food_item in food_items_data:
        if food_item["id"] == food_item_id:
            food_items_data.remove(food_item)
            return {}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
    )
