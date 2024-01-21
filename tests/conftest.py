import pytest
from httpx import AsyncClient
from server.app import app
from server.utils.firebase import get_user_id
from server.utils.firebase_emulator import (
    TestSettings,
    clear_firestore_emulator,
    seed_test_auth_users,
    sign_in_with_email_and_password_emulator,
)


@pytest.fixture()
async def prepare_auth():
    await seed_test_auth_users()


@pytest.fixture()
async def prepare_clean_db():
    await clear_firestore_emulator()


@pytest.fixture()
async def http_client():
    async with AsyncClient(
        app=app, base_url=TestSettings.base_url, follow_redirects=True
    ) as ac:
        yield ac


@pytest.fixture()
async def http_client_for_test_1(prepare_auth):
    async_client = await http_client_and_id_for_user(TestSettings.test_1_user_email)
    yield async_client
    await async_client.aclose()


@pytest.fixture()
async def http_client_for_test_2(prepare_auth):
    async_client = await http_client_and_id_for_user(TestSettings.test_2_user_email)
    yield async_client
    await async_client.aclose()


@pytest.fixture()
async def http_client_for_admin(prepare_auth):
    async_client = await http_client_and_id_for_user(TestSettings.admin_user_email)
    yield async_client
    await async_client.aclose()


@pytest.fixture()
async def test_user_1_id(prepare_auth):
    return get_user_id(TestSettings.test_1_user_email)


@pytest.fixture()
async def test_user_2_id(prepare_auth):
    return get_user_id(TestSettings.test_2_user_email)


@pytest.fixture()
async def test_admin_id(prepare_auth):
    return get_user_id(TestSettings.admin_user_email)


async def http_client_and_id_for_user(email: str):
    response = await sign_in_with_email_and_password_emulator(
        email, TestSettings.test_password
    )
    async_client = AsyncClient(
        app=app, base_url=TestSettings.base_url, follow_redirects=True
    )
    async_client.headers["Authorization"] = f'Bearer {response["idToken"]}'
    return async_client
