from uuid import uuid4

import pytest
from httpx import AsyncClient

from tests.utils.utils import random_string


async def create_test_user(client: AsyncClient):
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


async def create_food_item(client: AsyncClient, user_id: str, name: str, category: str = "Produce"):
    response = await client.post(
        f"/v1/users/{user_id}/food-items",
        json={
            "name": name,
            "category": category,
            "quantity": 1.00,
            "expiration_date": "2026-01-01",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


@pytest.mark.anyio
async def test_log_usage_used(client: AsyncClient):
    user_id = await create_test_user(client)
    item_id = await create_food_item(client, user_id, "Banana")

    response = await client.post(
        f"/v1/users/{user_id}/food-items/{item_id}/log-usage",
        json={"action": "used", "delete_item": False},
    )
    assert response.status_code == 201
    assert response.json()["detail"] == "Item logged as used."


@pytest.mark.anyio
async def test_log_usage_wasted(client: AsyncClient):
    user_id = await create_test_user(client)
    item_id = await create_food_item(client, user_id, "Spinach")

    response = await client.post(
        f"/v1/users/{user_id}/food-items/{item_id}/log-usage",
        json={"action": "wasted", "delete_item": False},
    )
    assert response.status_code == 201
    assert response.json()["detail"] == "Item logged as wasted."


@pytest.mark.anyio
async def test_log_usage_with_delete(client: AsyncClient):
    user_id = await create_test_user(client)
    item_id = await create_food_item(client, user_id, "Apple")

    response = await client.post(
        f"/v1/users/{user_id}/food-items/{item_id}/log-usage",
        json={"action": "used", "delete_item": True},
    )
    assert response.status_code == 201

    # Item should be deleted
    get_response = await client.get(f"/v1/users/{user_id}/food-items/{item_id}")
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_log_usage_item_not_found(client: AsyncClient):
    user_id = await create_test_user(client)
    fake_id = str(uuid4())

    response = await client.post(
        f"/v1/users/{user_id}/food-items/{fake_id}/log-usage",
        json={"action": "used", "delete_item": False},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_log_usage_invalid_action(client: AsyncClient):
    user_id = await create_test_user(client)
    item_id = await create_food_item(client, user_id, "Carrot")

    response = await client.post(
        f"/v1/users/{user_id}/food-items/{item_id}/log-usage",
        json={"action": "donated", "delete_item": False},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_frequently_used_report(client: AsyncClient):
    user_id = await create_test_user(client)
    item_id = await create_food_item(client, user_id, "Chicken Breast", "Meat")

    # Log "used" 3 times
    for _ in range(3):
        await client.post(
            f"/v1/users/{user_id}/food-items/{item_id}/log-usage",
            json={"action": "used", "delete_item": False},
        )

    response = await client.get(f"/v1/users/{user_id}/reports/frequently-used")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Chicken Breast"
    assert data[0]["count"] == 3
    assert data[0]["unit"] == "times"


@pytest.mark.anyio
async def test_frequently_wasted_report(client: AsyncClient):
    user_id = await create_test_user(client)
    item_id = await create_food_item(client, user_id, "Strawberries", "Produce")

    # Log "wasted" 2 times
    for _ in range(2):
        await client.post(
            f"/v1/users/{user_id}/food-items/{item_id}/log-usage",
            json={"action": "wasted", "delete_item": False},
        )

    response = await client.get(f"/v1/users/{user_id}/reports/frequently-wasted")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Strawberries"
    assert data[0]["count"] == 2
    assert data[0]["unit"] == "times"


@pytest.mark.anyio
async def test_unused_report(client: AsyncClient):
    user_id = await create_test_user(client)
    await create_food_item(client, user_id, "Dried Lentils", "Grains")

    response = await client.get(f"/v1/users/{user_id}/reports/unused")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Dried Lentils"
    assert data[0]["unit"] == "days"


@pytest.mark.anyio
async def test_reports_empty_for_new_user(client: AsyncClient):
    user_id = await create_test_user(client)

    used = await client.get(f"/v1/users/{user_id}/reports/frequently-used")
    assert used.status_code == 200
    assert used.json() == []

    wasted = await client.get(f"/v1/users/{user_id}/reports/frequently-wasted")
    assert wasted.status_code == 200
    assert wasted.json() == []

    unused = await client.get(f"/v1/users/{user_id}/reports/unused")
    assert unused.status_code == 200
    assert unused.json() == []


@pytest.mark.anyio
async def test_reports_user_not_found(client: AsyncClient):
    fake_id = str(uuid4())

    response = await client.get(f"/v1/users/{fake_id}/reports/frequently-used")
    assert response.status_code == 404
