from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from ..utils.crypt import encrypt
from ..utils.updated_resources import generate_updated_resources
from ..models.user import User


class SetTutorialStatusPayload(BaseModel):
    tutorialStatus: str


async def set_tutorial_status_route(request: Request, userId: int) -> Response:
    body = request.state.decrypted_body
    if not body:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    try:
        parsed = SetTutorialStatusPayload(**body)
    except Exception:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    auth_user_id = getattr(request.state, "user_id", None)
    if str(userId) != str(auth_user_id):
        return Response(
            content=encrypt({"httpStatus": 403, "errorCode": "session_error", "errorMessage": ""}),
            status_code=403,
            media_type="application/octet-stream",
        )

    await User.filter(userId=auth_user_id).update(tutorialStatus=parsed.tutorialStatus)

    updated = await generate_updated_resources(auth_user_id)
    return Response(
        content=encrypt({"updatedResources": updated}),
        media_type="application/octet-stream",
    )
