from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response
from ....utils.crypt import encrypt
from ....utils.updated_resources import generate_updated_resources
from ....models.user import User
from ....models.user_episode_status import UserEpisodeStatus

class PostUserStoryLog(BaseModel):
    noSkip: bool
    useSkip: bool
    autoFinish: bool
    useAuto: bool
    fastForward: bool
    continuousPlayStart: bool
    playMusicVideo: bool
    voice: bool

async def post_user_story_log(request: Request, userId: int, storyType: str, episodeId: int) -> Response:
    auth_user_id = getattr(request.state, "user_id", None)
    if str(userId) != str(auth_user_id):
       return Response(
           content=encrypt({"httpStatus": 403, "errorCode": "session_error", "errorMessage": ""}),
           status_code=403,
           media_type="application/octet-stream",
       ) 

    user = await User.filter(userId=userId).first()
    if not user:
        return Response(
            content=encrypt({
                "httpStatus": 404,
                "errorCode": "",
                "errorMessage": "User not found",
            }),
            status_code=404,
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
        parsed = PostUserStoryLog(**body)
    except Exception:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )
    
    updated_resources = await generate_updated_resources(user_id=userId)
    
    await UserEpisodeStatus.filter(userId=userId, storyType=storyType, episodeId=episodeId).update(
        autoFinish=parsed.autoFinish,
        useAuto=parsed.useAuto,
        fastForward=parsed.fastForward,
        voice=parsed.voice,
        continuousPlayStart=parsed.continuousPlayStart,
        playMusicVideo=parsed.playMusicVideo
    )
    
    return Response(
        content=encrypt({
            'updatedResources': updated_resources,
            'obtainedResources': [],
        }),
        media_type='application/octet-stream'
    )