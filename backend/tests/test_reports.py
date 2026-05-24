from uuid import uuid4

import pytest
from httpx import AsyncClient

from tests.utils.utils import create_test_user, login_user, random_string, user_auth_header


async def create_food_item(
    client: AsyncClient, headers: dict, name: str, category: str = "Produce"
):
    response = await client.post(
        "/v1/food-items",
        headers=headers,
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
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    item_id = await create_food_item(client, headers, "Banana")

    response = await client.post(
        f"/v1/food-items/{item_id}/log-usage",
        headers=headers,
        json={"action": "used", "delete_item": False},
    )
    assert response.status_code == 201
    assert response.json()["detail"] == "Item logged as used."


@pytest.mark.anyio
async def test_log_usage_wasted(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    item_id = await create_food_item(client, headers, "Spinach")

    response = await client.post(
        f"/v1/food-items/{item_id}/log-usage",
        headers=headers,
        json={"action": "wasted", "delete_item": False},
    )
    assert response.status_code == 201
    assert response.json()["detail"] == "Item logged as wasted."


@pytest.mark.anyio
async def test_log_usage_with_delete(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    item_id = await create_food_item(client, headers, "Apple")

    response = await client.post(
        f"/v1/food-items/{item_id}/log-usage",
        headers=headers,
        json={"action": "used", "delete_item": True},
    )
    assert response.status_code == 201

    # Item should be deleted
    get_response = await client.get(f"/v1/food-items/{item_id}", headers=headers)
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_log_usage_item_not_found(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    fake_id = str(uuid4())

    response = await client.post(
        f"/v1/food-items/{fake_id}/log-usage",
        headers=headers,
        json={"action": "used", "delete_item": False},
    )
    assert response.status_code == 404


@pytest.mark.anyio
async def test_log_usage_invalid_action(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    item_id = await create_food_item(client, headers, "Carrot")

    response = await client.post(
        f"/v1/food-items/{item_id}/log-usage",
        headers=headers,
        json={"action": "donated", "delete_item": False},
    )
    assert response.status_code == 422


@pytest.mark.anyio
async def test_frequently_used_report(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    item_id = await create_food_item(client, headers, "Chicken Breast", "Meat")

    # Log "used" 3 times
    for _ in range(3):
        await client.post(
            f"/v1/food-items/{item_id}/log-usage",
            headers=headers,
            json={"action": "used", "delete_item": False},
        )

    response = await client.get("/v1/reports/frequently-used", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Chicken Breast"
    assert data[0]["count"] == 3
    assert data[0]["unit"] == "times"


@pytest.mark.anyio
async def test_frequently_wasted_report(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    item_id = await create_food_item(client, headers, "Strawberries", "Produce")

    # Log "wasted" 2 times
    for _ in range(2):
        await client.post(
            f"/v1/food-items/{item_id}/log-usage",
            headers=headers,
            json={"action": "wasted", "delete_item": False},
        )

    response = await client.get("/v1/reports/frequently-wasted", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Strawberries"
    assert data[0]["count"] == 2
    assert data[0]["unit"] == "times"


@pytest.mark.anyio
async def test_unused_report(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    await create_food_item(client, headers, "Dried Lentils", "Grains")

    response = await client.get("/v1/reports/unused", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == "Dried Lentils"
    assert data[0]["unit"] == "days"


@pytest.mark.anyio
async def test_reports_empty_for_new_user(client: AsyncClient):
    email = f"{random_string()}@example.com"
    await create_test_user(client, email_address=email)
    token = await login_user(client, email_address=email)
    headers = user_auth_header(token)

    used = await client.get("/v1/reports/frequently-used", headers=headers)
    assert used.status_code == 200
    assert used.json() == []

    wasted = await client.get("/v1/reports/frequently-wasted", headers=headers)
    assert wasted.status_code == 200
    assert wasted.json() == []

    unused = await client.get("/v1/reports/unused", headers=headers)
    assert unused.status_code == 200
    assert unused.json() == []


@pytest.mark.anyio
async def test_reports_unauthorized(client: AsyncClient):
    response = await client.get("/v1/reports/frequently-used")
    assert response.status_code == 401
