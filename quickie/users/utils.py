def serialize_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }
