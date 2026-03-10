import json
import time
from math import floor

from src.models.user_config import UserConfig
from src.models.user_costume_3d_status import UserCostume3DStatus
from src.models.user_music_result import UserMusicResult
from src.utils import master_suite

from ..config import config
from ..models.user import User
from ..models.user_stamp import UserStamp
from ..models.user_game_data import UserGameData
from ..models.user_area import UserArea
from ..models.user_area_playlist_status import UserAreaPlaylistStatus
from ..models.user_shop import UserShop
from ..models.user_shop_item import UserShopItem
from ..models.user_boost_status import UserBoostStatus
from ..models.card import Card
from ..models.user_deck import UserDeck
from ..models.user_music import UserMusic
from ..models.user_character import UserCharacter
from ..models.user_unit import UserUnit
from ..models.user_episode_status import UserEpisodeStatus
from ..models.user_material_exchange import UserMaterialExchange
from ..consts.music_cons import DIFFICULTIES
from .payloads import convert_deck_to_sekai_deck

from src.data import game_data as gdata

_reg_data = None


def _get_reg_data():
    global _reg_data
    if _reg_data is None:
        with open("./json/reg.json", "r") as f:
            _reg_data = json.load(f)
    return _reg_data


def _ts(dt) -> int:
    """Convert a datetime to millisecond timestamp."""
    return int(dt.timestamp() * 1000)


async def generate_updated_resources(user_id: int) -> dict:
    reg = _get_reg_data()

    user = await User.filter(userId=user_id).first()
    if not user:
        raise ValueError(f"User {user_id} not found")

    stamps = await UserStamp.filter(userId=user_id).all()
    game_data = await UserGameData.filter(userId=user_id).first()
    if not game_data:
        raise ValueError(f"UserGameData for {user_id} not found")

    areas = await UserArea.filter(userId=user_id).all()
    # Load playlist statuses for areas
    area_playlist_map = {}
    playlist_ids = [a.areaPlaylistStatusId for a in areas if a.areaPlaylistStatusId]
    if playlist_ids:
        playlists = await UserAreaPlaylistStatus.filter(id__in=playlist_ids).all()
        area_playlist_map = {p.id: p for p in playlists}

    shops = await UserShop.filter(userId=user_id).all()
    shop_items_map = {}
    shop_ids = [s.id for s in shops]
    if shop_ids:
        all_shop_items = await UserShopItem.filter(userShopId__in=shop_ids).all()
        for item in all_shop_items:
            shop_items_map.setdefault(item.userShopId, []).append(item)

    boost_data = await UserBoostStatus.filter(userId=user_id).first()
    if not boost_data:
        raise ValueError(f"UserBoostStatus for {user_id} not found")

    cards = await Card.filter(userId=user_id).all()
    decks = await UserDeck.filter(userId=user_id).all()
    musics = await UserMusic.filter(userId=user_id).all()
    characters = await UserCharacter.filter(userId=user_id).all()
    units = await UserUnit.filter(userId=user_id).all()

    user_registration = {
        "userId": user.userId,
        "signature": user.signature,
        "platform": user.platform,
        "deviceModel": user.deviceModel,
        "operatingSystem": user.operatingSystem,
        "registeredAt": _ts(user.registeredAt),
    }

    if user.birthdate:
        user_registration.update({
            "yearOfBirth": user.birthdate.year,
            "monthOfBirth": user.birthdate.month,
            "dayOfBirth": user.birthdate.day,
            "age": floor((time.time() - user.birthdate.timestamp()) / (60 * 60 * 24 * 365)),
        })

    user_cards = [
        {
            "userId": card.userId,
            "cardId": card.cardId,
            "level": card.level,
            "exp": card.exp,
            "totalExp": card.totalExp,
            "skillLevel": card.skillLevel,
            "skillExp": card.skillExp,
            "totalSkillExp": card.totalSkillExp,
            "masterRank": card.masterRank,
            "specialTrainingStatus": card.specialTrainingStatus,
            "defaultImage": card.defaultImage,
            "duplicateCount": card.duplicateCount,
            "createdAt": _ts(card.createdAt),
            "episodes": [],
        }
        for card in cards
    ]

    user_decks = [
        convert_deck_to_sekai_deck({
            "userId": deck.userId,
            "deckId": deck.deckId,
            "name": deck.name,
            "members": deck.members,
        })
        for deck in decks
    ]

    user_musics = [
        {
            "userId": music.userId,
            "musicId": music.musicId,
            "userMusicDifficultyStatuses": [
                {
                    "musicId": music.musicId,
                    "musicDifficulty": difficulty,
                    "musicDifficultyStatus": "available" if difficulty in music.availableDifficulties else "forbidden",
                    "userMusicResults": [],
                }
                for difficulty in DIFFICULTIES
            ],
            "userMusicVocals": [
                {
                    "userId": user.userId,
                    "musicId": music.musicId,
                    "vocalId": x,
                    "createdAt": _ts(music.createdAt),
                    "updatedAt": _ts(music.updatedAt),
                }
                for x in music.vocals
            ],
            "userMusicAchievements": [],
            "createdAt": _ts(music.createdAt),
            "updatedAt": _ts(music.updatedAt),
        }
        for music in musics
    ]
    
    results = await UserMusicResult.filter(userId=user.userId)
    
    user_music_results = [
        {
            "userId": result.userId,
            "musicId": result.musicId,
            "musicDifficulty": result.musicDifficulty,
            "playType": result.playType,
            "playResult": result.playResult,
            "highScore": result.highScore,
            "fullComboFlg": result.fullComboFlg,
            "fullPerfectFlg": result.fullPerfectFlg,
            "mvpCount": result.mvpCount,
            "superStarCount": result.superStarCount,
            "createAt": _ts(result.createdAt), # it should be like that
            "updatedAt": _ts(result.updatedAt),
        }
        for result in results
    ]

    user_characters = [
        {
            "characterId": x.characterId,
            "characterRank": x.characterRank,
            "exp": x.exp,
            "totalExp": x.totalExp,
        }
        for x in characters
    ]

    user_units = [
        {
            "userId": x.userId,
            "unit": x.unit,
            "rank": x.rank,
            "exp": x.exp,
            "totalExp": x.totalExp,
        }
        for x in units
    ]

    archive_event_episode_statuses = await UserEpisodeStatus.filter(
        userId=user.userId, storyType="archive_event_story"
    ).all()

    card_episode_statuses = await UserEpisodeStatus.filter(
        userId=user.userId, storyType="card_story"
    ).all()

    character_profile_episode_statuses = await UserEpisodeStatus.filter(
        userId=user.userId, storyType="character_profile_story"
    ).all()

    event_episode_statuses = await UserEpisodeStatus.filter(
        userId=user.userId, storyType="event_story"
    ).all()

    special_episode_statuses = await UserEpisodeStatus.filter(
        userId=user.userId, storyType="special_story"
    ).all()

    unit_episode_statuses = await UserEpisodeStatus.filter(
        userId=user.userId, storyType="unit_story"
    ).all()

    material_exchanges = await UserMaterialExchange.filter(userId=user_id).all()

    def _ep_list(eps):
        return [
            {
                "storyType": x.storyType,
                "episodeId": x.episodeId,
                "status": x.status,
                "isNotSkipped": x.isNotSkipped,
            }
            for x in eps
        ]

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

    user_shops_payload = []
    for s in shops:
        items = shop_items_map.get(s.id, [])
        shop_entry = {
            "shopId": s.shopId,
            "userShopItems": [
                {
                    "shopItemId": item.shopItemId,
                    **({"level": item.level} if item.level is not None else {}),
                    "status": item.status,
                }
                for item in items
            ],
        }
        user_shops_payload.append(shop_entry)
    
    costumes = await UserCostume3DStatus.filter(userId=user_id)
    
    userConfig = await UserConfig.filter(userId=user_id).first()

    result = {
        **reg.get("updatedResources", {}),
        "userLoginBonuses": [
            # {"userId": user.userId, "loginBonusId": 1, "loginBonusType": "normal", "progress": 1}
        ],
        "userConfig": {
            "defaultMusicType": userConfig.defaultMusicType.value,
            "isDisplayLoginStatus": userConfig.displayLoginStatus,
            "friendRequestScope": userConfig.friendRequestScope.value,
            "naOptoutAdvertisingType": "on",
            "naOptoutSupportAndAnalyticsType": "on",  
        },
        "userPracticeTickets": [],
        "userSkillPracticeTickets": [],
        "userMaterials": [],
        "userGachas": [],
        "userGachaBonusPoints": [],
        "userCostume3dStatuses": [
            {
                "costume3dId": costume.costumeId,
                "status": costume.status.value,
                **({"obtainedAt": _ts(costume.obtainedAt)} if costume.obtainedAt else {}),
            }
            for costume in costumes
        ] + [
            {
                "costume3dId": c['id'],
                "status": "forbidden"
            }
            for c in master_suite.mastersuite['costume3ds']
            if c['id'] not in {costume.costumeId for costume in costumes}
        ],
        "userCostume3dShopItems": [],
        "userCharacterCostume3ds": [],
        "unreadUserTopics": [],
        "userHomeBanners": [],
        "userGachaCeilExchanges": [],
        "userGachaCeilItems": [],
        "userGachaCeilExchangeSubstituteCosts": [],
        "userBoostItems": [],
        "userStampFavoriteTabs": [],
        "userStampFavorites": [],
        
        "now": int(time.time() * 1000),
        "refreshableTypes": [],
        "userRegistration": user_registration,
        "userGamedata": {
            "userId": user.userId,
            "name": user.name,
            "deck": game_data.deck,
            "rank": game_data.rank,
            "exp": game_data.exp,
            "totalExp": game_data.totalExp,
            "coin": game_data.coin,
            "virtualCoin": game_data.virtualCoin,
        },
        "userChargedCurrency": {
            "paid": 0,
            "free": game_data.crystals,
            "paidUnitPrices": [],
        },
        "userBoost": {
            "current": boost_data.current,
            "recoveryAt": _ts(boost_data.recoveryAt),
        },
        "userTutorial": {
            "tutorialStatus": user.tutorialStatus,
        },
        "userAreas": user_areas_payload,
        "userCards": user_cards,
        "userDecks": user_decks,
        "userMusics": user_musics,
        "userMusicResults": user_music_results,
        "userMusicAchievements": [],
        "userShops": user_shops_payload,
        "userBonds": [],
        "userUnitEpisodeStatuses": _ep_list(unit_episode_statuses),
        "userSpecialEpisodeStatuses": _ep_list(special_episode_statuses),
        "userEventEpisodeStatuses": _ep_list(event_episode_statuses),
        "userArchiveEventEpisodeStatuses": _ep_list(archive_event_episode_statuses),
        "userCharacterProfileEpisodeStatuses": _ep_list(character_profile_episode_statuses),
        "userCardEpisodeStatuses": _ep_list(card_episode_statuses),
        "userEventArchiveCompleteReadRewards": game_data.eventArchiveCompleteReadRewards,
        "userUnits": user_units,
        "userPresents": [],
        "userStamps": [
            {
                "stampId": x.stampId,
                "obtainedAt": _ts(x.obtainedAt),
            }
            for x in stamps
        ],
        "userMaterialExchanges": [
            {
                "userId": x.userId,
                "materialExchangeId": x.materialExchangeId,
                "exchangeCount": x.exchangeCount,
                "totalExchangeCount": x.totalExchangeCount,
                "lastExchangedAt": _ts(x.lastExchangedAt),
                "exchangeStatus": x.exchangeStatus,
                **({"exchangeRemaining": x.exchangeRemaining} if x.exchangeRemaining is not None else {}),
                "refreshedAt": _ts(x.refreshedAt),
            }
            for x in material_exchanges
        ],
        "userCharacters": user_characters,
        "userBeginnerMissionBehavior": {
            "userBeginnerMissionBehaviorType": "beginner_mission_v2",
        },
        "userProfile": {
            "userId": user.userId,
            "profileImageType": "leader",
        },
        "userAvatar": {
            "avatarSkinColorId": 1,
        },
        "userAvatarCostumes": [{"avatarCostumeId": 1}],
        "userAvatarSkinColors": [{"avatarSkinColorId": 1}],
        "userRankMatchResult": {
            "liveId": "",
            "liveStatus": "none",
        },
        "userLiveCharacterArchiveVoice": {
            "characterArchiveVoiceGroupIds": [],
        },
        "userViewableAppeal": {"appealIds": [1]},
        "userBillingRefunds": [],
        "userUnprocessedOrders": [],
        "userInformations": [info.model_dump() for info in config.informations],
        "userPenlights": [{"penlightId": 1, "favoriteFlg": True}],
    }

    if user.userLiveId:
        result["userLiveId"] = user.userLiveId

    return result
