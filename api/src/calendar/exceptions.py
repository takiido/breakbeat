from fastapi import HTTPException, status


CalendarNotFound = HTTPException(
    status_code = status.HTTP_404_NOT_FOUND,
    detail = "Calendar not found",
)


EventNotFound = HTTPException(
    status_code = status.HTTP_404_NOT_FOUND,
    detail = "Event not found",
)


CalendarAccessDenied = HTTPException(
    status_code = status.HTTP_403_FORBIDDEN,
    detail = "Access denied",
)


EventAccessDenied = HTTPException(
    status_code = status.HTTP_403_FORBIDDEN,
    detail = "Access denied",
)