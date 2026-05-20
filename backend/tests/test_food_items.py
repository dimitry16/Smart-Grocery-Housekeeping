from decimal import Decimal
from uuid import uuid4

import pytest
from httpx import AsyncClient

from tests.utils.utils import (
    create_test_user,
    login_user,
    user_auth_header,
)


@pytest.mark.anyio
async def test_create_food_item_success(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client)
    headers = user_auth_header(token)

    response = await client.post(
        "v1/food-items",
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
        headers=headers,
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
    assert content["user_id"] == user["id"]
    assert "id" in content


@pytest.mark.anyio
async def test_create_food_item_name_only_success(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client)
    headers = user_auth_header(token)

    response = await client.post(
        "v1/food-items", json={"name": "Whole Milk", "quantity": 1.00}, headers=headers
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == "Whole Milk"
    assert Decimal(content["quantity"]) == Decimal("1.00")
    assert content["user_id"] == user["id"]
    assert "id" in content


@pytest.mark.anyio
async def test_create_food_item_unauthorized(client: AsyncClient):

    response = await client.post(
        "v1/food-items",
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
    assert response.status_code == 401
    content = response.json()
    assert content["detail"] == "Not authenticated"


@pytest.mark.anyio
async def test_read_food_item_success(client: AsyncClient):
    user = await create_test_user(client)
    token = await login_user(client)
    headers = user_auth_header(token)

    # Create food item
    create = await client.post(
        "v1/food-items",
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
        headers=headers,
    )

    food_item_id = create.json()["id"]

    response = await client.get(f"v1/food-items/{food_item_id}", headers=headers)
    assert response.status_code == 200

    content = response.json()

    assert Decimal(content["quantity"]) == Decimal("1.00")
    assert content["unit"] == "gallon"
    assert content["expiration_date"] == "2026-05-20"
    assert content["id"] == food_item_id
    assert content["user_id"] == user["id"]


@pytest.mark.anyio
async def test_read_food_item_not_found(client: AsyncClient):
    await create_test_user(client)
    token = await login_user(client)
    headers = user_auth_header(token)

    food_item_id = uuid4()

    response = await client.get(f"v1/food-items/{food_item_id}", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Food item not found."
