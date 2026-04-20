from uuid import UUID
from typing import Annotated
from app.database.sqlconnector import get_db
from app.database.models import FoodItems as FoodItemsModel
from fastapi import APIRouter, Depends, HTTPException, status
from ..schema import FoodItemCreate, FoodItemResponse, FoodItemUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("", response_model=list[FoodItemResponse])
async def get_all_food_items(db: Annotated[AsyncSession, Depends(get_db)]):
    """Read all food items (in ascending order)"""
    result = await db.execute(select(FoodItemsModel).order_by(FoodItemsModel.name.asc()))
    food_items = result.scalars().all()
    return food_items

@router.post("", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def create_food_item(
    food_item: FoodItemCreate, db: Annotated[AsyncSession, Depends(get_db)]
):
    """Create a Food Item"""
    new_food_item = FoodItemsModel(**food_item.model_dump())
    db.add(new_food_item)
    await db.commit()
    await db.refresh(new_food_item)
    return new_food_item

@router.get("/{food_item_id}", response_model=FoodItemResponse)
async def get_food_item(food_item_id: UUID, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(FoodItemsModel)
        .where(FoodItemsModel.id == food_item_id),
    )
    food_item = result.scalars().first()
    if food_item:
        return food_item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food Item not found.")
