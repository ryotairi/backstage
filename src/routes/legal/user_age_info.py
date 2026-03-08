import math
import time
from starlette.requests import Request
from starlette.responses import Response

from ...utils.crypt import encrypt
from ...models.user import User


async def user_age_info_route(request: Request, userId: int) -> Response:
    auth_user_id = getattr(request.state, "user_id", None)
    if str(userId) != str(auth_user_id):
        return Response(
            content=encrypt({"httpStatus": 403, "errorCode": "session_error", "errorMessage": ""}),
            status_code=403,
            media_type="application/octet-stream",
        )

    user = await User.filter(userId=auth_user_id).first()
    if not user:
        return Response(
            content=encrypt({"httpStatus": 403, "errorCode": "session_error", "errorMessage": ""}),
            status_code=403,
            media_type="application/octet-stream",
        )

    result = {"userId": user.userId}
    if user.birthdate:
        result["yearOfBirth"] = user.birthdate.year
        result["monthOfBirth"] = user.birthdate.month
        result["dayOfBirth"] = user.birthdate.day
        result["age"] = math.floor(
            (time.time() - user.birthdate.timestamp()) / (60 * 60 * 24 * 365)
        )
    else:
        result["yearOfBirth"] = None
        result["monthOfBirth"] = None
        result["dayOfBirth"] = None
        result["age"] = None

    return Response(
        content=encrypt(result),
        media_type="application/octet-stream",
    )
