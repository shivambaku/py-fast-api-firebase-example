import os

import firebase_admin
from firebase_admin import auth, credentials

from server.utils.models import UserModel

if os.path.isfile("serviceAccountKey.json"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "serviceAccountKey.json"

cred = credentials.ApplicationDefault()
firebase_app = firebase_admin.initialize_app(cred)


def get_auth():
    return auth


def get_user_id(email: str) -> str:
    user = auth.get_user_by_email(email)
    return user.uid


def get_firebase_user(auth_token: str) -> UserModel:
    claims = auth.verify_id_token(auth_token)
    user_model = UserModel(
        id=claims["user_id"],
        email=claims["email"],
        is_admin="admin" in claims,
    )
    return user_model
