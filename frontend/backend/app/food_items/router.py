from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from ..food_items.food_data import food_items_data
from ..food_items.schema import (
    FoodItemCreate,
    FoodItemResponse,
    FoodItemUpdate,
)

router = APIRouter()


@router.get("", response_model=list[FoodItemResponse])
async def get_all_food_items() -> list:
    """Read all food items."""
    return food_items_data


@router.get("/{food_item_id}", response_model=FoodItemResponse)
async def get_single_food_item(food_item_id: str) -> dict:
    """Get a specific food item by their ID.

    Raises:
        HTTPException: 404 response if food item does not exist.
    """
    for food_item in food_items_data:
        if food_item.get("id") == food_item_id:
            return food_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found"
    )


@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(food_item: FoodItemCreate) -> dict:
    """Create a food item."""

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


@router.patch("/{food_item_id}")
async def partial_update_food_item(
    food_item_id: str, food_item_data: FoodItemUpdate
) -> dict:
    """Partially updates a food item by its ID.

    - Only include fields that you want to update in the request body.

    - Omit any fields that remain unchanged.

    Raises:
        HTTPException: 404 response if food item does not exist.
    """
    for food_item in food_items_data:
        if food_item["id"] == food_item_id:
            # Only update fields that were sent in request
            food_item.update(food_item_data.model_dump(exclude_unset=True))
            return food_item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
    )


@router.delete("/{food_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_food_item(food_item_id: str):
    """Delete food item by ID.

    Raises:
        HTTPException: 404 response if food item does not exist.
    """
    for food_item in food_items_data:
        if food_item.get("id") == food_item_id:
            food_items_data.remove(food_item)
            return {}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found."
    )
