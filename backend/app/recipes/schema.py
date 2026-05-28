from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class RecipeCreate(BaseModel):
    id: str | None = Field(None)  # Add this so you can lookup the recipe ID
    title: str | None = Field(None, max_length=50)
    description: str | None = Field(None, max_length=2000)
    image_url: str | None = Field(None)
    source_url: str | None = Field(None)
    recipe_ingredients: list[str]


class RecipeResponse(BaseModel):
    title: str | None = Field(None, max_length=50)
    description: str | None = Field(None, max_length=2000)
    image_url: str | None = Field(None)
    source_url: str | None = Field(None)
    recipe_ingredients: list[str]


class RecipeListResponse(BaseModel):
    recipes: list[RecipeResponse]
