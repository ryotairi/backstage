import json
import uuid
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import Response

from src.data import game_data
from src.enum.user_costume_status import UserCostumeStatus
from src.models.user_costume_3d_status import UserCostume3DStatus

from ...utils.crypt import encrypt
from ...utils.credentials import create_credential, create_signature
from ...utils.random import generate_user_id
from ...utils.updated_resources import generate_updated_resources
from ...consts.game_data_cons import UNITS
from ...services.logger import logger
from ...models.user import User
from ...models.user_game_data import UserGameData
from ...models.user_boost_status import UserBoostStatus
from ...models.card import Card
from ...models.user_deck import UserDeck
from ...models.user_music import UserMusic
from ...models.user_shop import UserShop
from ...models.user_shop_item import UserShopItem
from ...models.user_episode_status import UserEpisodeStatus
from ...models.user_material_exchange import UserMaterialExchange
from ...models.user_character import UserCharacter
from ...models.user_unit import UserUnit
from ...models.user_area import UserArea
from ...models.user_area_playlist_status import UserAreaPlaylistStatus

from datetime import datetime, timedelta

_initial_areas = None
_reg_data = None

def _get_initial_areas():
    global _initial_areas
    if _initial_areas is None:
        with open("./json/initialUserAreas.json", "r") as f:
            _initial_areas = json.load(f)
    return _initial_areas


def _get_reg_data():
    global _reg_data
    if _reg_data is None:
        with open("./json/reg.json", "r") as f:
            _reg_data = json.load(f)
    return _reg_data


class RegisterUserPayload(BaseModel):
    platform: str
    deviceModel: str
    operatingSystem: str


async def register_user_route(request: Request) -> Response:
    body = request.state.decrypted_body
    if not body:
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    try:
        parsed = RegisterUserPayload(**body)
    except Exception:
        logger.error(f"Failed to parse RegisterUserRoute payload: {body}")
        return Response(
            content=encrypt({"httpStatus": 422, "errorCode": "", "errorMessage": ""}),
            status_code=422,
            media_type="application/octet-stream",
        )

    reg = _get_reg_data()
    initial_areas = _get_initial_areas()

    user_id = generate_user_id()
    user = await User.create(
        deviceModel=parsed.deviceModel,
        operatingSystem=parsed.operatingSystem,
        platform=parsed.platform,
        name=game_data.initialPlayerName,
        credential=create_credential(user_id),
        signature=create_signature(user_id),
        userId=user_id,
    )

    await UserGameData.create(
        userId=user.userId,
        coin=0,
        deck=1,
        exp=0,
        totalExp=0,
        rank=1,
        virtualCoin=0,
        eventArchiveCompleteReadRewards=reg.get("updatedResources", {}).get(
            "userEventArchiveCompleteReadRewards", []
        ),
    )

    await UserBoostStatus.create(
        userId=user.userId,
        current=15,
        recoveryAt=datetime.now() + timedelta(days=1),
    )

    for card_id in game_data.initialFreeCards:
        await Card.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            cardId=card_id,
            level=1,
            exp=0,
            totalExp=0,
            skillLevel=1,
            skillExp=0,
            totalSkillExp=0,
            masterRank=0,
            specialTrainingStatus="not_doing",
            defaultImage="original",
            duplicateCount=0,
        )

    for area in initial_areas:
        user_area_data = {
            "id": str(uuid.uuid4()),
            "areaId": area["areaId"],
            "actionSets": area["actionSets"],
            "areaItems": area["areaItems"],
            "status": area["userAreaStatus"]["status"],
            "userId": user.userId,
        }

        if area.get("userAreaStatus", {}).get("userAreaPlaylistStatus"):
            playlist_status = await UserAreaPlaylistStatus.create(
                id=str(uuid.uuid4()),
                areaPlaylistId=area["userAreaStatus"]["userAreaPlaylistStatus"]["areaPlaylistId"],
                status=area["userAreaStatus"]["userAreaPlaylistStatus"]["status"],
            )
            user_area_data["areaPlaylistStatusId"] = playlist_status.id

        await UserArea.create(**user_area_data)

    cards = await Card.filter(userId=user.userId).all()

    await UserDeck.create(
        uniqueDeckId=str(uuid.uuid4()),
        userId=user.userId,
        deckId=1,
        name="Group 01",
        members=[card.cardId for card in cards[:5]],
    )

    for music_id in game_data.initialMusics:
        vocals_data = next(
            (v.vocals for v in game_data.initialMusicsVocals if v.musicId == music_id),
            [],
        )
        await UserMusic.create(
            musicId=music_id,
            userId=user.userId,
            uniqueMusicId=str(uuid.uuid4()),
            vocals=vocals_data,
            availableDifficulties=["easy", "normal", "hard", "expert"],
        )

    updated_resources = reg.get("updatedResources", {})

    for shop in updated_resources.get("userShops", []):
        shop_obj = await UserShop.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            shopId=shop["shopId"],
        )
        for item in shop.get("userShopItems", []):
            await UserShopItem.create(
                id=str(uuid.uuid4()),
                shopItemId=item["shopItemId"],
                status=item["status"],
                level=item.get("level"),
                userShopId=shop_obj.id,
            )

    for ep in updated_resources.get("userUnitEpisodeStatuses", []):
        await UserEpisodeStatus.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            episodeId=ep["episodeId"],
            storyType="unit_story",
            isNotSkipped=False,
            status=ep["status"],
        )

    for ep in updated_resources.get("userSpecialEpisodeStatuses", []):
        await UserEpisodeStatus.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            episodeId=ep["episodeId"],
            storyType="special_story",
            isNotSkipped=False,
            status=ep["status"],
        )

    for ep in updated_resources.get("userEventEpisodeStatuses", []):
        await UserEpisodeStatus.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            episodeId=ep["episodeId"],
            storyType="event_story",
            isNotSkipped=False,
            status=ep["status"],
        )

    for ep in updated_resources.get("userArchiveEventEpisodeStatuses", []):
        await UserEpisodeStatus.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            episodeId=ep["episodeId"],
            storyType="archive_event_story",
            isNotSkipped=False,
            status=ep["status"],
        )

    for ep in updated_resources.get("userCharacterProfileEpisodeStatuses", []):
        await UserEpisodeStatus.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            episodeId=ep["episodeId"],
            storyType="character_profile_story",
            isNotSkipped=False,
            status=ep["status"],
        )

    for exchange in updated_resources.get("userMaterialExchanges", []):
        await UserMaterialExchange.create(
            id=str(uuid.uuid4()),
            userId=user.userId,
            exchangeCount=0,
            materialExchangeId=exchange["materialExchangeId"],
            exchangeStatus="exchangeable",
            exchangeRemaining=exchange.get("exchangeRemaining"),
            totalExchangeCount=0,
        )

    for i in range(1, 27):
        await UserCharacter.create(
            characterId=i,
            userId=user.userId,
            uniqueCharacterId=str(uuid.uuid4()),
        )

    for unit_name in UNITS:
        await UserUnit.create(
            uniqueUnitId=str(uuid.uuid4()),
            userId=user.userId,
            userGameDataUserId=user.userId,
            unit=unit_name,
        )
    
    for costumeId in game_data.initialAvailableCostumes:
        await UserCostume3DStatus.create(
            userId=user.userId,
            costumeId=costumeId,
            status=UserCostumeStatus.available,
            obtainedAt=datetime.now()
        )
    
    for costumeId in game_data.initialSaleCostumes:
        await UserCostume3DStatus.create(
            userId=user.userId,
            costumeId=costumeId,
            status=UserCostumeStatus.sale
        )

    user_registration = {
        "userId": user.userId,
        "signature": user.signature,
        "platform": user.platform,
        "deviceModel": user.deviceModel,
        "operatingSystem": user.operatingSystem,
        "registeredAt": int(user.registeredAt.timestamp() * 1000),
    }

    updated = await generate_updated_resources(user.userId)

    logger.info(
        f"New registration: {user.userId} ({json.dumps({'platform': parsed.platform, 'deviceModel': parsed.deviceModel, 'operatingSystem': parsed.operatingSystem})})"
    )

    return Response(
        content=encrypt({
            "userRegistration": user_registration,
            "credential": user.credential,
            "updatedResources": updated,
        }),
        media_type="application/octet-stream",
    )
