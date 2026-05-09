from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from tests.utils.utils import random_string


async def create_test_user(client: AsyncClient):
    """A helper function that creates a dummy user."""
    response = await client.post(
        "/v1/users",
        json={
            "email_address": f"{random_string()}@example.com",
            "password": "Password123!",
            "name": "Tester",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


@pytest.mark.anyio
async def test_create_food_item_success(client: AsyncClient):
    user_id = await create_test_user(client)

    response = await client.post(
        f"/v1/users/{user_id}/food-items",
        json={
            "name": "Whole Milk",
            "brand": "Horizon Organic",
            "barcode": "742365008412",
            "category": "Dairy",
            "image_url": "https://images.example.com/products/horizon-whole-milk.jpg",
            "quantity": 1.00,
            "unit": "gallon",
            "expiration_date": "2026-05-20",
        },
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == "Whole Milk"
    assert content["brand"] == "Horizon Organic"
    assert content["barcode"] == "742365008412"
    assert content["category"] == "Dairy"
    assert (
        content["image_url"]
        == "https://images.example.com/products/horizon-whole-milk.jpg"
    )
    assert Decimal(content["quantity"]) == Decimal("1.00")
    assert content["unit"] == "gallon"
    assert content["expiration_date"] == "2026-05-20"
    assert content["user_id"] == user_id
    assert "id" in content


@pytest.mark.anyio
async def test_create_food_item_name_only_success(client: AsyncClient):
    user_id = await create_test_user(client)

    response = await client.post(
        f"/v1/users/{user_id}/food-items",
        json={"name": "Whole Milk", "quantity": 1.00},
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == "Whole Milk"
    assert Decimal(content["quantity"]) == Decimal("1.00")
    assert content["user_id"] == user_id
    assert "id" in content


@pytest.mark.anyio
async def test_read_food_item(client: AsyncClient):
    user_id = await create_test_user(client)

    # Create food item
    create = await client.post(
        f"/v1/users/{user_id}/food-items",
        json={
            "name": "Whole Milk",
            "brand": "Horizon Organic",
            "barcode": "742365008412",
            "category": "Dairy",
            "image_url": "https://images.example.com/products/horizon-whole-milk.jpg",
            "quantity": 1.00,
            "unit": "gallon",
            "expiration_date": "2026-05-20",
        },
    )
    food_item_id = UUID(create.json()["id"])
    assert create.status_code == 201

    response = await client.get(f"/v1/users/{user_id}/food-items/{food_item_id}")
    assert response.status_code == 200
    content = response.json()
    assert Decimal(content["quantity"]) == Decimal("1.00")
    assert content["unit"] == "gallon"
    assert content["expiration_date"] == "2026-05-20"
    assert content["user_id"] == user_id


@pytest.mark.anyio
async def test_read_food_item_not_found(client: AsyncClient):
    user_id = await create_test_user(client)

    response = await client.get(f"/v1/users/{user_id}/food-items/{uuid4()}")

    assert response.status_code == 404
    content = response.json()
    assert (
        content["detail"]
        == "Food item not found or user is not authorized to view item"
    )
