from starlette.requests import Request
from starlette.responses import Response
from ...utils.crypt import encrypt
from ...utils.updated_resources import generate_updated_resources
from ...models.user import User

from typing import Optional
from pydantic import BaseModel

class UserHomeRefreshPayload(BaseModel):
    refreshableTypes: list
    isAdult: bool

async def user_home_refresh(request: Request, userId: int) -> Response:
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
        parsed = UserHomeRefreshPayload(**body)
    except Exception:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )
    
    updated_resources = await generate_updated_resources(user_id=userId)
    
    return Response(
        content=encrypt({
            'updatedResources': updated_resources,
            'userConvertedGachaCeilItems': [],
            'userReceivedEventMissionRewards': [],
            'userReceivedFriendInvitationCampaignMissionRewards': [],
            'userLoginBonuses': [],
            'newPendingUserFriends': [],
            'receivableRewardStreamingVirtualLiveSchedules': [],
            'userReportThanksMessage': None,
            'userObtainedMaterialAutoExchangeMusicVocals': [],
            'shouldReflectWebPayment': False,
            'receivableUnprocessedSerialCodeCampaignIds': [],    
        }),
        media_type='application/octet-stream'
    )