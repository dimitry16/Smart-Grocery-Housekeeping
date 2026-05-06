# Name: Yasser Hernandez (hernayas)
# Citation for the ode below:
# Date: 04/15/2025
# Adapted from "ORM Quick Start"
# Source URL: https://docs.sqlalchemy.org/en/20/orm/quickstart.html

from app.database.sqlconnector import Base
from typing import List, Optional
from sqlalchemy import ForeignKey, Numeric, Text
from sqlalchemy import String
import sqlalchemy
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


import uuid
import datetime


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email_address: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(30))

    user_food_items: Mapped[List["UserFoodItems"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserFoodItems(Base):
    __tablename__ = "user_food_items"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    food_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_items.id"), nullable=False
    )

    quantity: Mapped[Numeric] = mapped_column(
        sqlalchemy.Numeric(6, 2), nullable=False, default=1
    )
    unit: Mapped[Optional[str]] = mapped_column(String(30))
    expiration_date: Mapped[Optional[datetime.date]] = mapped_column(sqlalchemy.Date)

    user: Mapped["User"] = relationship(back_populates="user_food_items")
    food_items: Mapped["FoodItems"] = relationship()


class FoodItems(Base):
    __tablename__ = "food_items"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    brand: Mapped[Optional[str]] = mapped_column(String(30))
    barcode: Mapped[Optional[str]] = mapped_column(String(100), unique=True)
    category: Mapped[Optional[str]] = mapped_column(String(30))
    image_url: Mapped[Optional[str]] = mapped_column(Text)


class Recipes(Base):
    __tablename__ = "recipes"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(600))
    image_url: Mapped[Optional[str]] = mapped_column(Text)
    source_url: Mapped[Optional[str]] = mapped_column(Text)

    recipe_ingredients: Mapped[List["RecipeIngredients"]] = relationship(
        back_populates="recipe", cascade="all, delete-orphan"
    )


class RecipeIngredients(Base):
    __tablename__ = "recipe_ingredients"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    recipe_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False
    )
    food_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("food_items.id"), nullable=False
    )

    quantity: Mapped[Numeric] = mapped_column(
        sqlalchemy.Numeric(10, 2), nullable=False, default=1
    )
    unit: Mapped[Optional[str]] = mapped_column(String(30))

    recipe: Mapped["Recipes"] = relationship(back_populates="recipe_ingredients")
    food_items: Mapped["FoodItems"] = relationship()
