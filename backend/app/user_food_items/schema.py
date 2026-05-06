import datetime
import uuid
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.food_items.schema import FoodItemResponse


class UserFoodItemBase(BaseModel):
    quantity: Decimal = Field(Decimal("1"), gt=0, max_digits=6, decimal_places=2)
    unit: str | None = Field(None, max_length=30)
    expiration_date: datetime.date | None = Field(None)


class UserFoodItemCreate(UserFoodItemBase):
    food_item_id: uuid.UUID


class UserFoodItemUpdate(BaseModel):
    quantity: Decimal = Field(Decimal("1"), gt=0, max_digits=6, decimal_places=2)
    unit: str | None = Field(None, max_length=30)
    expiration_date: datetime.date | None = Field(None)


class UserFoodItemResponse(UserFoodItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    food_item: FoodItemResponse
