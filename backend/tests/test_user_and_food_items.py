from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from httpx import AsyncClient

from tests.utils.utils import random_string, random_units, random_upc


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


@pytest.mark.anyio
async def test_read_food_items_success(client: AsyncClient):
    user_id = await create_test_user(client)

    # Create 5 random food items
    for i in range(5):
        content = await client.post(
            f"/v1/users/{user_id}/food-items",
            json={
                "name": random_string(),
                "brand": random_string(),
                "barcode": random_upc(),
                "category": random_string(),
                "image_url": f"https://image-of-food.com/products/{i}/front.jpg",
                "quantity": 1.0 + i,
                "unit": random_units(),
                "expiration_date": f"2026-04-{i + 1:02d}",
            },
        )
        assert content.status_code == 201

    response = await client.get(f"/v1/users/{user_id}/food-items")
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 5


@pytest.mark.anyio
async def test_update_food_item_success(client: AsyncClient):
    user_id = await create_test_user(client)

    create = await client.post(
        f"/v1/users/{user_id}/food-items",
        json={
            "name": random_string(),
            "brand": random_string(),
            "barcode": random_upc(),
            "category": random_string(),
            "image_url": "https://image-of-food.com/products/1/front.jpg",
            "quantity": 1.00,
            "unit": "gallon",
            "expiration_date": "2026-05-20",
        },
    )
    food_item_id = create.json()["id"]
    assert create.status_code == 201

    updated_data = {
        "name": "Updated Name",
        "brand": "Updated Brand",
        "barcode": "098275621346",
        "category": "Updated Category",
        "image_url": "https://image-of-food.com/products/2/front.jpg",
        "quantity": 2.00,
        "unit": "liter",
        "expiration_date": "2025-06-21",
    }
    response = await client.patch(
        f"/v1/users/{user_id}/food-items/{food_item_id}",
        json=updated_data,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == updated_data["name"]
    assert content["brand"] == updated_data["brand"]
    assert content["barcode"] == updated_data["barcode"]
    assert content["category"] == updated_data["category"]
    assert content["image_url"] == updated_data["image_url"]
    assert Decimal(content["quantity"]) == Decimal(updated_data["quantity"])
    assert content["unit"] == updated_data["unit"]
    assert content["expiration_date"] == updated_data["expiration_date"]


@pytest.mark.anyio
async def test_partial_update_food_item_success(client: AsyncClient):
    user_id = await create_test_user(client)

    create = await client.post(
        f"/v1/users/{user_id}/food-items",
        json={
            "name": random_string(),
            "quantity": 1.00,
            "unit": "gallon",
        },
    )
    food_item_id = create.json()["id"]
    original_data = create.json()
    assert create.status_code == 201

    updated_data = {
        "name": "Updated Name",
        "quantity": 2.00,
    }
    response = await client.patch(
        f"/v1/users/{user_id}/food-items/{food_item_id}",
        json=updated_data,
    )

    assert response.status_code == 200
    content = response.json()
    assert content["name"] == updated_data["name"]
    assert Decimal(content["quantity"]) == Decimal(updated_data["quantity"])

    assert content["unit"] == original_data["unit"]
