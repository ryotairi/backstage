from starlette.requests import Request
from starlette.responses import Response
from ...utils.crypt import encrypt
from ...models.user import User
from ...models.user_area import UserArea
from ...models.user_area_playlist_status import UserAreaPlaylistStatus

async def get_user_areas(request: Request, userId: int) -> Response:
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
    
    areas = await UserArea.filter(userId=userId).all()
    # Load playlist statuses for areas
    area_playlist_map = {}
    playlist_ids = [a.areaPlaylistStatusId for a in areas if a.areaPlaylistStatusId]
    if playlist_ids:
        playlists = await UserAreaPlaylistStatus.filter(id__in=playlist_ids).all()
        area_playlist_map = {p.id: p for p in playlists}
    user_areas_payload = []
    for a in areas:
        area_entry = {
            "areaId": a.areaId,
            "areaItems": a.areaItems,
            "actionSets": a.actionSets,
            "userAreaStatus": {
                "areaId": a.areaId,
                "status": a.status,
            },
        }
        if a.areaPlaylistStatusId and a.areaPlaylistStatusId in area_playlist_map:
            ps = area_playlist_map[a.areaPlaylistStatusId]
            area_entry["userAreaStatus"]["userAreaPlaylistStatus"] = {
                "areaPlaylistId": ps.areaPlaylistId,
                "status": ps.status,
            }
        user_areas_payload.append(area_entry)
    
    return Response(
        content=encrypt({
            "userAreas": user_areas_payload
        }),
        media_type='application/octet-stream'
    )