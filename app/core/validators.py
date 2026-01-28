from fastapi import HTTPException


def validate_username(username) -> None:
    if not username.strip():
        raise HTTPException(status_code=400, detail="Username must be provided and cannot be empty.")
    if len(username) < 4:
        raise HTTPException(status_code=400, detail="Username must be at least 4 characters long.")
    if username.isdigit():
        raise HTTPException(status_code=400, detail="Username cannot be a number.")
