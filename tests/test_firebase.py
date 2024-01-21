from server.utils.firebase_emulator import (
    clear_firestore_emulator,
    seed_test_auth_users,
    sign_in_with_email_and_password_emulator,
)
from server.utils.settings import TestSettings


async def test_sign_in_with_email_and_password():
    await clear_firestore_emulator()
    await seed_test_auth_users()

    email = TestSettings.test_1_user_email
    password = TestSettings.test_password

    response = await sign_in_with_email_and_password_emulator(email, password)
    assert response["email"] == email
    assert response["localId"] is not None
    assert response["idToken"] is not None
