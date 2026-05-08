import uuid

from pydantic import BaseModel, ConfigDict, Field


class FoodItemBase(BaseModel):
    """Food Item Base properties to be shared"""

    name: str = Field(..., min_length=4, max_length=50)
    brand: str | None = Field(None, max_length=30)
    barcode: str | None = Field(None, max_length=100)
    category: str | None = Field(None, max_length=30)
    image_url: str | None = Field(None)


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(BaseModel):
    name: str | None = Field(None, max_length=50)
    brand: str | None = Field(None, max_length=30)
    barcode: str | None = Field(None, max_length=100)
    category: str | None = Field(None, max_length=30)
    image_url: str | None = Field(None)


class FoodItemResponse(FoodItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
