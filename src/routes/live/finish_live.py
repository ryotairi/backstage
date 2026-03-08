from typing import Any
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from ...utils.crypt import encrypt
from ...utils.updated_resources import generate_updated_resources
from ...config import config
from ...services.logger import logger
from ...models.user import User
from ...models.user_live import UserLive


class FinishLivePayload(BaseModel):
    score: int
    perfectCount: int
    greatCount: int
    goodCount: int
    badCount: int
    missCount: int
    maxCombo: int
    life: int
    tapCount: int
    musicCategoryName: str
    isMirrored: bool
    ingameCutinCharacterArchiveVoiceGroupIds: list[Any]


async def finish_live_route(request: Request, userId: int, liveId: str) -> Response:
    body = request.state.decrypted_body
    if not body:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    try:
        parsed = FinishLivePayload(**body)
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

    if user.userLiveId != liveId:
        logger.error(
            f"{user.name} ({user.userId}) tried to finish solo live {liveId}, "
            f"but they are in {user.userLiveId}."
        )
        return Response(
            content=encrypt({"httpStatus": 409, "errorCode": "", "errorMessage": ""}),
            status_code=409,
            media_type="application/octet-stream",
        )

    live = await UserLive.filter(liveId=liveId).first()
    if not live:
        logger.error(
            f"{user.name} ({user.userId}) tried to finish solo live {liveId}, "
            f"but that live does not exist."
        )
        return Response(
            content=encrypt({"httpStatus": 400, "errorCode": "", "errorMessage": ""}),
            status_code=400,
            media_type="application/octet-stream",
        )

    logger.info(
        f"{user.name} ({user.userId}) has finished solo live {liveId}. "
        f"PERFECT: {parsed.perfectCount}, GREAT: {parsed.greatCount}, "
        f"GOOD: {parsed.goodCount}, BAD: {parsed.badCount}, MISS: {parsed.missCount}, "
        f"LIFE: {parsed.life}, MAX COMBO: {parsed.maxCombo}, SCORE: {parsed.score}"
    )

    if config.deleteLiveDataAfterFinishing:
        await UserLive.filter(liveId=liveId, userId=auth_user_id).delete()
    else:
        await UserLive.filter(liveId=liveId, userId=auth_user_id).update(
            perfectCount=parsed.perfectCount,
            greatCount=parsed.greatCount,
            goodCount=parsed.goodCount,
            badCount=parsed.badCount,
            missCount=parsed.missCount,
            score=parsed.score,
            life=parsed.life,
            maxCombo=parsed.maxCombo,
            tapCount=parsed.tapCount,
        )

    updated = await generate_updated_resources(auth_user_id)
    return Response(
        content=encrypt({"updatedResources": updated}),
        media_type="application/octet-stream",
    )
