import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.user_food_items.schema import UserFoodItemResponse


class UserBase(BaseModel):
    name: str | None = Field(min_length=2, max_length=30)
    email: EmailStr = Field(max_length=255)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=30)
    email: EmailStr | None = Field(default=None, max_length=255)


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str


class UserInventoryResponse(UserResponse):
    model_config = ConfigDict(from_attributes=True)

    user_food_items: list[UserFoodItemResponse] = []
