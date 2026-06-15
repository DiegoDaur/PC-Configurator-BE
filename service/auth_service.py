import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone

from model.user import User
from repository import user_repository
from exception.app_exception import AppException

SECRET_KEY = os.environ.get("JWT_SECRET", "pc_configurator_secret_key_change_in_prod")
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24


def register(data):
    _validate_register(data)

    if user_repository.get_by_email(data["email"]):
        raise AppException("Email già registrata!", 409)

    if user_repository.get_by_username(data["username"]):
        raise AppException("Username già in uso!", 409)

    hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

    new_user = User(
        id=None,
        username=data["username"],
        email=data["email"],
        password=hashed.decode("utf-8"),
        role=data.get("role", "user"),
    )

    return user_repository.create(new_user)


def login(data):
    _validate_login(data)

    user = user_repository.get_by_email(data["email"])

    if user is None:
        raise AppException("Credenziali non valide!", 401)

    password_ok = bcrypt.checkpw(
        data["password"].encode("utf-8"),
        user.password.encode("utf-8")
    )

    if not password_ok:
        raise AppException("Credenziali non valide!", 401)

    token = _generate_token(user)

    return {"user": user, "token": token}


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise AppException("Token scaduto, effettua di nuovo il login!", 401)
    except jwt.InvalidTokenError:
        raise AppException("Token non valido!", 401)


def _generate_token(user):
    payload = {
        "user_id": user.id,
        "email":   user.email,
        "role":    user.role,
        "exp":     datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRY_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def _validate_register(data):
    for campo in ["username", "email", "password"]:
        if campo not in data or not str(data[campo]).strip():
            raise AppException(f"Campo '{campo}' obbligatorio!", 400)

    if "@" not in data["email"] or "." not in data["email"]:
        raise AppException("Formato email non valido!", 400)

    if len(data["password"]) < 6:
        raise AppException("La password deve contenere almeno 6 caratteri!", 400)

    if len(data["username"]) < 3:
        raise AppException("L'username deve contenere almeno 3 caratteri!", 400)


def _validate_login(data):
    for campo in ["email", "password"]:
        if campo not in data or not str(data[campo]).strip():
            raise AppException(f"Campo '{campo}' obbligatorio!", 400)
