from starlette.requests import Request
from starlette.responses import Response
from ...utils.crypt import encrypt
from ...utils.updated_resources import generate_updated_resources
from ...models.user import User

async def post_user_param(request: Request, userId: int) -> Response:
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
    
    return Response(
        content=encrypt({}),
        media_type='application/octet-stream'
    )