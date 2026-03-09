from typing import Any
from uuid import uuid4
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from src.models.user_music_result import UserMusicResult
from src.utils.master_suite import get_difficulty
from src.utils.play_result import compare_play_result_gt

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
    ingameCutinCharacterArchiveVoiceGroupIds: list[Any] | None


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
    
    difficulty = get_difficulty(live.musicDifficultyId)
    
    # TODO compare sum of taps with difficulty['totalNoteCount'] 

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
    
    fullPerfect = parsed.perfectCount == difficulty['totalNoteCount']
    fullCombo = not fullPerfect and (parsed.perfectCount + parsed.greatCount == difficulty['totalNoteCount'])
    
    playResult = 'clear'
    if parsed.life == 0:
        playResult = 'not_clear'
    elif fullPerfect:
        playResult = 'full_perfect'
    elif fullCombo:
        playResult = 'full_combo'
    
    result = await UserMusicResult.filter(musicId=live.musicId).first()
    
    if not result:
        await UserMusicResult.create(
            uniqueResultId=str(uuid4()),
            musicId=live.musicId,
            musicDifficulty=difficulty['musicDifficulty'],
            userId=userId,
            playType='solo',
            playResult=playResult,
            highScore=parsed.score,
            fullComboFlg=fullCombo,
            fullPerfectFlg=fullPerfect
        )
    else:
        await UserMusicResult.filter(userId=userId, musicId=live.musicId, musicDifficulty=difficulty['musicDifficulty']).update(
            playResult=compare_play_result_gt(playResult, result.playResult),
            highScore=max(result.highScore, parsed.score),
            fullComboFlg=(result.fullComboFlg or fullCombo),
            fullPerfectFlg=(result.fullPerfectFlg or fullPerfect)
        )

    updated = await generate_updated_resources(auth_user_id)
    return Response(
        content=encrypt({"updatedResources": updated}),
        media_type="application/octet-stream",
    )
