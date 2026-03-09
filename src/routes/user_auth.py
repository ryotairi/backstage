from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from uuid import uuid4

from ..utils.crypt import encrypt
from ..utils.updated_resources import generate_updated_resources
from ..config import config
from ..models.user import User


class UserAuthPayload(BaseModel):
    credential: str
    deviceId: str | None


async def user_auth_route(request: Request, userId: int) -> Response:
    body = request.state.decrypted_body
    if not body:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    try:
        parsed = UserAuthPayload(**body)
    except Exception:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    latest_version = config.versions[config.latestVersion]

    user = await User.filter(credential=parsed.credential).first()
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

    refresh = request.query_params.get("refreshUpdatedResources", "True")
    if refresh == "False":
        updated_resources = {}
    else:
        updated_resources = await generate_updated_resources(user.userId)

    return Response(
        content=encrypt({
            "sessionToken": user.credential,
            "appVersion": latest_version.appVersion,
            "multiPlayVersion": latest_version.multiPlayVersion,
            "dataVersion": config.dataVersion,
            "assetVersion": latest_version.assetVersion,
            "removeAssetVersion": "1.3.1.0",
            "assetHash": config.assetHash,
            "appVersionStatus": latest_version.appVersionStatus,
            "isStreamingVirtualLiveForceOpenUser": False,
            "deviceId": parsed.deviceId if parsed.deviceId != None else str(uuid4()),
            "updatedResources": updated_resources,
            "suiteMasterSplitPath": config.suiteMasterSplitPath,
            "obtainedBondsRewardIds": [],
        }),
        media_type="application/octet-stream",
    )
