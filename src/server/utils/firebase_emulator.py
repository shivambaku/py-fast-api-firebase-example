import os

import httpx
from firebase_admin import exceptions

from server.utils.firebase import cred, get_auth
from server.utils.settings import TestSettings

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"

FIRESTORE_EMULATOR_HOST = os.getenv("FIRESTORE_EMULATOR_HOST", None)
FIREBASE_AUTH_EMULATOR_HOST = os.getenv("FIREBASE_AUTH_EMULATOR_HOST", None)


async def seed_test_auth_users():
    auth = get_auth()

    try:
        auth.create_user(
            email=TestSettings.test_1_user_email,
            password=TestSettings.test_password,
        )

        auth.create_user(
            email=TestSettings.test_2_user_email,
            password=TestSettings.test_password,
        )

        user = auth.create_user(
            email=TestSettings.admin_user_email,
            password=TestSettings.test_password,
        )
        auth.set_custom_user_claims(user.uid, {"admin": True})
    except exceptions.FirebaseError:
        pass  # User already exists


async def clear_firestore_emulator():
    async with httpx.AsyncClient() as async_client:
        if FIRESTORE_EMULATOR_HOST:
            response = await async_client.delete(
                f"http://{FIRESTORE_EMULATOR_HOST}/emulator/v1/projects/{cred.project_id}/databases/(default)/documents"
            )
            response.raise_for_status()


async def clear_collection_emulator(collection: str):
    async with httpx.AsyncClient() as ac:
        if FIRESTORE_EMULATOR_HOST:
            response = await ac.delete(
                f"http://{FIRESTORE_EMULATOR_HOST}/emulator/v1/projects/{cred.project_id}/databases/(default)/documents/{collection}"
            )
            response.raise_for_status()


async def sign_in_with_email_and_password_emulator(
    email: str, password: str, return_secure_token: bool = True
):
    firebase_sign_in_with_password_url = f"http://{FIREBASE_AUTH_EMULATOR_HOST}/identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    async with httpx.AsyncClient() as async_client:
        response = await async_client.post(
            url=firebase_sign_in_with_password_url,
            params={"key": "valid-api-key"},
            json={
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token,
            },
        )
        response.raise_for_status()
        return response.json()
