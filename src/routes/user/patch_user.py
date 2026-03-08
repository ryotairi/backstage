from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from ...utils.crypt import encrypt
from ...utils.updated_resources import generate_updated_resources
from ...models.user import User


class UserGamedataPayload(BaseModel):
    name: str


class UserRegistrationPayload(BaseModel):
    userId: int
    signature: Optional[object] = None
    platform: Optional[object] = None
    deviceModel: Optional[object] = None
    operatingSystem: Optional[object] = None
    registeredAt: int
    yearOfBirth: int
    monthOfBirth: int
    dayOfBirth: int
    age: int
    billableLimitAgeType: Optional[object] = None


class PatchUserPayload(BaseModel):
    userGamedata: Optional[UserGamedataPayload] = None
    userRegistration: Optional[UserRegistrationPayload] = None


async def patch_user_route(request: Request, userId: int) -> Response:
    auth_user_id = getattr(request.state, "user_id", None)
    if str(userId) != str(auth_user_id):
        return Response(
            content=encrypt({"httpStatus": 403, "errorCode": "session_error", "errorMessage": ""}),
            status_code=403,
            media_type="application/octet-stream",
        )

    body = request.state.decrypted_body
    if not body:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    try:
        parsed = PatchUserPayload(**body)
    except Exception:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    if not parsed.userGamedata and not parsed.userRegistration:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    if parsed.userGamedata:
        await User.filter(userId=auth_user_id).update(name=parsed.userGamedata.name)
    elif parsed.userRegistration:
        # Validate birthdate values before attempting to create datetime
        year = parsed.userRegistration.yearOfBirth
        month = parsed.userRegistration.monthOfBirth
        day = parsed.userRegistration.dayOfBirth
        
        # Only update birthdate if values are valid
        if year >= 1 and year <= 9999 and month >= 1 and month <= 12 and day >= 1 and day <= 31:
            try:
                birthdate = datetime(year=year, month=month, day=day)
                await User.filter(userId=auth_user_id).update(birthdate=birthdate)
            except ValueError:
                # Silently skip if datetime creation fails (e.g., invalid date like Feb 30)
                pass

    updated = await generate_updated_resources(auth_user_id)
    return Response(
        content=encrypt({"updatedResources": updated}),
        media_type="application/octet-stream",
    )
