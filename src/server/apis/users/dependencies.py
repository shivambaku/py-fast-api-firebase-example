from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
from server.utils.firebase import get_firebase_user
from server.utils.models import UserModel


def get_user(cred: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> UserModel:
    token = cred.credentials.split(" ")[-1]
    if not token:
        raise HTTPException(status_code=400, detail="TokenID must be provided")

    try:
        return get_firebase_user(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (
        auth.InvalidIdTokenError,
        auth.ExpiredIdTokenError,
        auth.RevokedIdTokenError,
        auth.UserDisabledError,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.default_message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
        )


UserDepends = Annotated[
    UserModel,
    Depends(get_user),
]
