from fastapi import HTTPException, status


InvalidCredentials = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Invalid email or password",
)


InvalidToken = HTTPException(
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Invalid or expired token",
)


EmailTaken = HTTPException(
    status_code = status.HTTP_400_BAD_REQUEST,
    detail = "Email already registered",
)


UsernameTaken = HTTPException(
    status_code = status.HTTP_400_BAD_REQUEST,
    detail = "Username already taken",
)


InactiveUser = HTTPException(
    status_code = status.HTTP_403_FORBIDDEN,
    detail = "Inactive user",
)
