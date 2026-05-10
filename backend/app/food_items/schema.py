import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class FoodItemBase(BaseModel):
    """Food Item Base properties to be shared"""

    name: str = Field(..., min_length=4, max_length=50)
    brand: str | None = Field(None, max_length=30)
    barcode: str | None = Field(None, max_length=100)
    category: str | None = Field(None, max_length=30)
    image_url: str | None = Field(None)
    quantity: Decimal = Field(Decimal("1"), gt=0, max_digits=6, decimal_places=2)
    unit: str | None = Field(None, max_length=30)
    expiration_date: datetime.date | None = Field(None)


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(BaseModel):
    name: str | None = Field(None, max_length=50)
    brand: str | None = Field(None, max_length=30)
    barcode: str | None = Field(None, max_length=100)
    category: str | None = Field(None, max_length=30)
    image_url: str | None = Field(None)
    quantity: Decimal = Field(Decimal("1"), gt=0, max_digits=6, decimal_places=2)
    unit: str | None = Field(None, max_length=30)
    expiration_date: datetime.date | None = Field(None)


class FoodItemResponse(FoodItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
