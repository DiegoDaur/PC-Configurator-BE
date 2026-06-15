from repository import user_repository
from exception.app_exception import AppException


def get_all():
    return user_repository.get_all()


def get_by_id(user_id):
    user = user_repository.get_by_id(user_id)
    if user is None:
        raise AppException("Utente non trovato!", 404)
    return user


def update(user_id, data, requesting_user_id, is_admin=False):
    if user_repository.get_by_id(user_id) is None:
        raise AppException("Utente non trovato!", 404)

    if user_id != requesting_user_id and not is_admin:
        raise AppException("Non sei autorizzato a modificare questo utente!", 403)

    if "username" in data:
        if len(data["username"]) < 3:
            raise AppException("L'username deve avere almeno 3 caratteri!", 400)
        existing = user_repository.get_by_username(data["username"])
        if existing and existing.id != user_id:
            raise AppException("Username già in uso!", 409)

    if "role" in data:
        if not is_admin:
            raise AppException("Non sei autorizzato a cambiare il ruolo!", 403)
        if data["role"] not in ("user", "admin"):
            raise AppException("Ruolo non valido! Valori accettati: 'user', 'admin'", 400)

    return user_repository.update(user_id, data)


def delete_by_id(user_id):
    if user_repository.get_by_id(user_id) is None:
        raise AppException("Utente non trovato!", 404)
    user_repository.delete_by_id(user_id)
