from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "cards" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "cardId" INT NOT NULL,
    "level" INT NOT NULL,
    "exp" INT NOT NULL,
    "totalExp" INT NOT NULL,
    "skillLevel" INT NOT NULL,
    "skillExp" INT NOT NULL,
    "totalSkillExp" INT NOT NULL,
    "masterRank" INT NOT NULL,
    "specialTrainingStatus" VARCHAR(32) NOT NULL,
    "defaultImage" VARCHAR(32) NOT NULL,
    "duplicateCount" INT NOT NULL,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "card_episodes" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "cardEpisodeId" INT NOT NULL,
    "scenarioStatus" VARCHAR(32) NOT NULL,
    "scenarioStatusReasons" JSONB NOT NULL,
    "isNotSkipped" BOOL NOT NULL,
    "cardId" VARCHAR(128)
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL UNIQUE,
    "credential" VARCHAR(512) NOT NULL,
    "signature" VARCHAR(512) NOT NULL,
    "platform" VARCHAR(64) NOT NULL,
    "deviceModel" VARCHAR(128) NOT NULL,
    "operatingSystem" VARCHAR(128) NOT NULL,
    "birthdate" TIMESTAMPTZ,
    "registeredAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "tutorialStatus" VARCHAR(64) NOT NULL DEFAULT 'start',
    "userLiveId" VARCHAR(128),
    "ban" VARCHAR(512),
    "name" VARCHAR(128) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_areas" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "status" VARCHAR(32) NOT NULL,
    "areaId" INT NOT NULL,
    "actionSets" JSONB NOT NULL,
    "areaItems" JSONB NOT NULL,
    "areaPlaylistStatusId" VARCHAR(128)
);
CREATE TABLE IF NOT EXISTS "area_playlist_statuses" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "areaPlaylistId" INT NOT NULL,
    "status" VARCHAR(64) NOT NULL
);
CREATE TABLE IF NOT EXISTS "users_boost" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL UNIQUE,
    "current" INT NOT NULL,
    "recoveryAt" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_characters" (
    "uniqueCharacterId" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "characterId" INT NOT NULL,
    "characterRank" INT NOT NULL DEFAULT 1,
    "exp" INT NOT NULL DEFAULT 0,
    "totalExp" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "user_configs" (
    "userId" BIGSERIAL NOT NULL PRIMARY KEY,
    "defaultMusicType" VARCHAR(14) NOT NULL,
    "displayLoginStatus" BOOL NOT NULL,
    "friendRequestScope" VARCHAR(9) NOT NULL
);
COMMENT ON COLUMN "user_configs"."defaultMusicType" IS 'original: original_music\nsekai: sekai';
COMMENT ON COLUMN "user_configs"."friendRequestScope" IS 'all: all\nid_search: id_search\nreject: reject';
CREATE TABLE IF NOT EXISTS "user_costumes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "costumeId" INT NOT NULL,
    "status" VARCHAR(9) NOT NULL,
    "obtainedAt" TIMESTAMPTZ
);
COMMENT ON COLUMN "user_costumes"."status" IS 'forbidden: forbidden\nsale: sale\navailable: available';
CREATE TABLE IF NOT EXISTS "user_decks" (
    "uniqueDeckId" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "deckId" INT NOT NULL,
    "name" VARCHAR(128) NOT NULL,
    "members" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_episode_statuses" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "storyType" VARCHAR(64) NOT NULL,
    "episodeId" INT NOT NULL,
    "status" VARCHAR(32) NOT NULL,
    "isNotSkipped" BOOL NOT NULL,
    "autoFinish" BOOL NOT NULL DEFAULT False,
    "useAuto" BOOL NOT NULL DEFAULT False,
    "fastForward" BOOL NOT NULL DEFAULT False,
    "voice" BOOL NOT NULL DEFAULT False,
    "continuousPlayStart" BOOL NOT NULL DEFAULT False,
    "playMusicVideo" BOOL NOT NULL DEFAULT False,
    "userId" BIGINT
);
CREATE TABLE IF NOT EXISTS "users_game_data" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL UNIQUE,
    "deck" INT NOT NULL DEFAULT 1,
    "rank" INT NOT NULL DEFAULT 1,
    "exp" INT NOT NULL DEFAULT 0,
    "totalExp" INT NOT NULL DEFAULT 0,
    "coin" INT NOT NULL DEFAULT 0,
    "virtualCoin" INT NOT NULL DEFAULT 0,
    "crystals" INT NOT NULL DEFAULT 10000,
    "eventArchiveCompleteReadRewards" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "users_live" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL UNIQUE,
    "liveId" VARCHAR(128) NOT NULL,
    "musicId" INT NOT NULL,
    "musicDifficultyId" INT NOT NULL,
    "musicVocalId" INT NOT NULL,
    "deckId" INT NOT NULL,
    "boostCount" INT NOT NULL,
    "isAutoPlay" BOOL NOT NULL,
    "perfectCount" INT,
    "greatCount" INT,
    "goodCount" INT,
    "badCount" INT,
    "missCount" INT,
    "score" INT,
    "life" INT,
    "maxCombo" INT,
    "tapCount" INT
);
CREATE TABLE IF NOT EXISTS "user_materials" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "materialId" INT NOT NULL,
    "quantity" INT NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_material_exchanges" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "materialExchangeId" INT NOT NULL,
    "exchangeCount" INT NOT NULL,
    "totalExchangeCount" INT NOT NULL,
    "lastExchangedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "exchangeStatus" VARCHAR(32) NOT NULL,
    "exchangeRemaining" INT,
    "refreshedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "user_musics" (
    "uniqueMusicId" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "musicId" INT NOT NULL,
    "vocals" JSONB NOT NULL,
    "availableDifficulties" JSONB NOT NULL,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "user_music_results" (
    "uniqueResultId" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "musicId" INT NOT NULL,
    "musicDifficulty" VARCHAR(32) NOT NULL,
    "playType" VARCHAR(32) NOT NULL DEFAULT 'solo',
    "playResult" VARCHAR(32) NOT NULL,
    "highScore" INT NOT NULL,
    "fullComboFlg" BOOL NOT NULL,
    "fullPerfectFlg" BOOL NOT NULL,
    "mvpCount" INT NOT NULL DEFAULT 0,
    "superStarCount" INT NOT NULL DEFAULT 0,
    "createdAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "user_shops" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "shopId" INT NOT NULL,
    "userId" BIGINT
);
CREATE TABLE IF NOT EXISTS "user_shop_items" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "shopItemId" INT NOT NULL,
    "status" VARCHAR(64) NOT NULL,
    "level" INT,
    "userShopId" VARCHAR(128)
);
CREATE TABLE IF NOT EXISTS "user_stamps" (
    "id" VARCHAR(128) NOT NULL PRIMARY KEY,
    "stampId" INT NOT NULL,
    "obtainedAt" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "userId" BIGINT NOT NULL
);
CREATE TABLE IF NOT EXISTS "user_units" (
    "uniqueUnitId" VARCHAR(128) NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "unit" VARCHAR(32) NOT NULL,
    "rank" INT NOT NULL DEFAULT 1,
    "exp" INT NOT NULL DEFAULT 0,
    "totalExp" INT NOT NULL DEFAULT 0,
    "userGameDataUserId" BIGINT
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "n3rDbQayqy22z5Zfuh+v5Pv5D3OB/sQ="
)
