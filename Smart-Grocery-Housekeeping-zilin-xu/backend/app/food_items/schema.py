from datetime import date

from pydantic import BaseModel, ConfigDict, Field

"""
Added expiration date by Zilin Xu on 5/5/2026
"""

class FoodItemBase(BaseModel):
    """Food Item Base properties to be shared"""

    name: str = Field(..., min_length=4, max_length=50)
    brand: str | None = Field(None, max_length=30)
    barcode: str | None = Field(None, max_length=100)
    category: str | None = Field(None, max_length=30)
    image_url: str | None = Field(None)
    expiration_date: date | None = Field(None)


class FoodItemCreate(FoodItemBase):
    pass


class FoodItemUpdate(BaseModel):
    name: str | None = Field(None, max_length=50)
    brand: str | None = Field(None, max_length=30)
    barcode: str | None = Field(None, max_length=100)
    category: str | None = Field(None, max_length=30)
    image_url: str | None = Field(None)
    expiration_date: date | None = Field(None)


class FoodItemResponse(FoodItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
