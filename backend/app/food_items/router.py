from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from ..food_items.food_data import food_items_data
from ..food_items.schema import FoodItemCreate, FoodItemResponse

router = APIRouter()


@router.get("", response_model=list[FoodItemResponse])
def get_all_food_items():
    """Read all food items."""
    return food_items_data


@router.get("/{food_item_id}", response_model=FoodItemResponse)
def get_single_food_item(food_item_id: str):
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
        status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found"
    )


@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
def create_food_item(food_item: FoodItemCreate):
    # Creates a uuid
    new_id = uuid4()
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
