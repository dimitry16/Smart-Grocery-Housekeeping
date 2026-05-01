import uuid

import pytest
from httpx import AsyncClient

from tests.utils.utils import random_string, random_upc


@pytest.mark.anyio
async def test_create_food_item_success(client: AsyncClient):
    response = await client.post(
        "/v1/food-items",
        json={
            "name": "Whole Milk",
            "brand": "Horizon Organic",
            "barcode": "742365008412",
            "category": "Dairy",
            "image_url": "https://images.example.com/products/horizon-whole-milk.jpg",
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
    assert "id" in content


@pytest.mark.anyio
async def test_create_food_item_name_only_success(client: AsyncClient):
    response = await client.post(
        "/v1/food-items",
        json={
            "name": "Whole Milk",
        },
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == "Whole Milk"
    assert "id" in content


@pytest.mark.anyio
async def test_read_food_item(client: AsyncClient):
    # Create food item
    create = await client.post(
        "/v1/food-items",
        json={
            "name": "Whole Milk",
            "brand": "Horizon Organic",
            "barcode": "742365008412",
            "category": "Dairy",
            "image_url": "https://images.example.com/products/horizon-whole-milk.jpg",
        },
    )
    food_item_id = create.json()["id"]
    assert create.status_code == 201

    response = await client.get(f"/v1/food-items/{food_item_id}")
    assert response.status_code == 200
    content = response.json()
    assert content["id"] == food_item_id


@pytest.mark.anyio
async def test_read_food_item_not_found(client: AsyncClient):
    response = await client.get(f"/v1/food-items/{uuid.uuid4()}")

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Food Item not found."


@pytest.mark.anyio
async def test_read_food_items_success(client: AsyncClient):
    # Create 5 random food items
    for i in range(5):
        content = await client.post(
            "/v1/food-items",
            json={
                "name": random_string(),
                "brand": random_string(),
                "barcode": random_upc(),
                "category": random_string(),
                "image_url": f"https://image-of-food.com/products/{i}/front.jpg",
            },
        )

    response = await client.get("/v1/food-items")
    assert response.status_code == 200
    content = response.json()
    assert len(content) >= 5
