import uuid
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from ...utils.crypt import encrypt
from ...utils.updated_resources import generate_updated_resources
from ...models.user import User
from ...models.user_live import UserLive


class StartLivePayload(BaseModel):
    musicId: int
    musicDifficultyId: int
    musicVocalId: int
    deckId: int
    boostCount: int
    isAuto: bool
    musicCategoryName: str


async def start_live_route(request: Request, userId: int) -> Response:
    body = request.state.decrypted_body
    if not body:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    try:
        parsed = StartLivePayload(**body)
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

    user = await User.filter(userId=auth_user_id).first()
    if not user:
        return Response(
            content=encrypt({"httpStatus": 403, "errorCode": "session_error", "errorMessage": ""}),
            status_code=403,
            media_type="application/octet-stream",
        )

    live_id = str(uuid.uuid4())
    await UserLive.create(
        userId=auth_user_id,
        liveId=live_id,
        boostCount=parsed.boostCount,
        deckId=parsed.deckId,
        isAutoPlay=parsed.isAuto,
        musicDifficultyId=parsed.musicDifficultyId,
        musicId=parsed.musicId,
        musicVocalId=parsed.musicVocalId,
    )

    await User.filter(userId=auth_user_id).update(userLiveId=live_id)

    updated = await generate_updated_resources(user.userId)
    return Response(
        content=encrypt({"updatedResources": updated}),
        media_type="application/octet-stream",
    )
