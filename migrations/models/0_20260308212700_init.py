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
    "mvpCount" INT NOT NULL,
    "superStarCount" INT NOT NULL,
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
    "eJztXW1v2zgS/iuBv7QL+BaJ83r3zUmzuzk0SREne4stFgIt0TYRSdRStBtj0f9+JC1Zoi"
    "zapqrYksl+aUzOI5GPKM5wZkT+0wmwB/345xtAvM5/jv7phCCA7A+pvHvUAVGUlfICCoa+"
    "EHSZhCgBw5gS4FJWOAJ+DFmRB2OXoIgiHLLScOr7vBC7TBCF46xoGqK/p9CheAzpBBJW8f"
    "UvVoxCD77BOP0ZvTojBH25nUg0T5Q7dB6JspsJIL8ISX67oeNifxqEmXQ0pxMcLsVZa3jp"
    "GIaQAAq9XAd4+5KOpkWLtrICSqZw2UgvK/DgCEx9muvwliy4OOQMopDGoosBeHN8GI7phP"
    "086V19X/Qm6+tCjHfh9/7TzW/9p49M6ifeF8wexOLxPCRVvUXdd3ERQMHiMoLbjMxpDMld"
    "CaHXaHwX0nJKM0yBVtaPKrSmBRmv2Wiqidgxv8+//t3rnZ5e9o5PL67Ozy4vz6+Or5isaN"
    "Rq1eUa8q/vfr17eJZp5wWc64xb/p6UcaskNgO0jNjeydnl2dXpxdmSz2XJOhpXKfPhDPoa"
    "jC3lTSUMvkUadCXSppJFMQX+rRZjeYiptMWvyPc/a76ZMsho6vRGXB5iKm3irRvoc7eCM5"
    "XAAMQUkicQvmqwJ4NMpS6OoIuA/8zvwO47oIBOY50Vh/IC9SxCdsCotAw57W2xCjntKRch"
    "vEpmOGnnXQDYo9MgtoizfCZ8TiMfuazLN3i6eEu3fOFXgaa+9C6BvH/9EvY+sQqKAqhYsu"
    "WBBfa8BPlz+kdDuWRd8B5Df95ZODTWEPd8d387eO7ff+E9CeL4b18w1H++5TU9UTovlH68"
    "KAzl5UWO/nf3/NsR/3n05+PDrWAQx3RMxB0zuec/O7xNYEqxE+JvDvByvpe0NCXmO/cbjV"
    "5zzg5eMATu6ze2unZWanAPq2RXq4JeUCwBIZuNvIRc3sycG+02QjH71VF42dLq7iZnmwMX"
    "ktbpdhhONzd7+Nr+IQln6nQduzAEBOEKxtkK0loRZZw+QRCz+69S+9/B48M21OYuUGD4JW"
    "Q9/+ohl3aPfBTTv96L785XcemKfK/hl3MgacCU14/3/T+KlN98frwuqjZ+gesC/yh+wJSt"
    "XaMIlvnjMfYhCBXTbQFaIHzIsM0c0+tc7I+PnyWOr+8KDveHl/vrWzYXC8KZEKKafnj1LK"
    "F0xG83OyQaam+TQ21KrCG21EssjJUVI0qUr7WeeKiqYVaTUruXGk0lKj0ZXXu1mWrR582O"
    "Su6Iw13HJAn0YEgRKPHlr5kPJVQ7Labzk21MJialnBRFXcFoQuOQWTtEy48lgSyZSzIjH9"
    "ARJoEOl3lMO6m8ONuCyYszJZG8quhfnSEX3nNtqOdelWDtZLPG9XtGKI54n7kvfx5TqDU+"
    "S6CW2CWxQ0TohHtHdd2uErAGt+vuLfaWeFnTbq+4WfOPkcAx4qHDKg70Itb60BvgQ5di8a"
    "ySMMtP39e2itzd1MeuDQj9AffPeytpvlz5jGalDmA1pTLKbOdEnk3xvwaPqbzhurhB/p0+"
    "m0E7Ch+PqOtu8vM4gIk1zNljQ2Q2L71xPqBYP2pmo2UFDvlcoxW7zQAtG5y1BW3ZhMxaMI"
    "BUK6ooo2wocZtQohhrFAZ6ROdBludtef7igzmnZLHI0bPmVXiz7fqGGaXyA+qsMVELkmsN"
    "Vv7onSgBOAv9avO7DsR4zb/X2kaCDDTVWDDPRq3HxdSgyfMa402zZl5k7XQp8jicIRdv1h"
    "xpszlsNkdnbyt5d0oI1PrkI4cwVbUQ6OIZJPMqsao8sp2RqpZEppRxxwYpOG6LMCWkzk3M"
    "BDYqN8dNZfe4CFhAl63WDE2Vge0SocE68VD92+66AazWjGtHbtMpru9LyJQGzY/HV3C7I/"
    "CkOew1fDuW4+Yw1Zq9WPbMWYPsnU/QfVWZOqJus5XjMbG9Gzi8rVVsmwxnzRpr1uzcrPEU"
    "w1a9vYNqvDad2NqUjE0L++HMugAGw2RRum0kOQexcWRVHLlBej3ZUmC9q14W2qzpky0rbG"
    "jzsBR8TDGZP3NaNDiVQO2cW+tPAIcVNgCBdvMPE0PD9acv2s0mZAO8vs0m9rAC2kPm184W"
    "QA0yk35lT/gT04sqC2lZv9E4ip0xk3W8VLgxZpHNZrDZDLt9v4sODk33hrGBBqIXnSE2KG"
    "ODMjYo8x6cuRiFOnHSRNxIrmaI0Cnwb/QoK6CMZM4lc7aK9UuWveqRloPscN4/Zv+awxuc"
    "wZD2iTtBM3iDg8iHFD5B4D3Bb+kpVtu6tbe4lHV3t8DdzfdP6CjWcKKuu3n95qdydukmDU"
    "S7dGsIhzteuvnaO5n4P7aLyd59su8TbJ3GyNWKCOQQpsYDBAWf0GiEXNa8uT59RazRRP6O"
    "XeDrc5iDmUqfzc/Rpkx80Kd7ao0MMpU6FPenFPOPhbXjd3mgjd5JrEaQjKCrPSSLsHaF8W"
    "obk2N+GJIudzLIVOYw9rSJy2MM5W0ItGnLQwxlLUBxrEubhDGUt9jFZTu9KzlbyhvKl49G"
    "OnSl4oayFYC3GxwMsc5LmYMYyhoFke5UlocYxFqDXPD3jFu+M/TtmzsBoehbqTt+Ra67Me"
    "88SCAOTDA28/wwMs+b4Lw/pMxKWfXI75me/68U3DLCa0w2WrCgq5RWcKYSmCQUVWOxHGwq"
    "lT6IaUpGhaM5SuDt3PPogE/nSKcN/dM5VpHtDMTW/3FMyswTDNg9eUv0p3EJa9AiQ95obc"
    "QG+qTaqUAS1E47DZh2mrR+5CHnjmrRKCq7m1eKXG7vm5Hcq1I+Nu1Gcq/M/LBrRrtm3MGa"
    "0eYqVUiA52kyWlnHGcImFxcVWemZDDOARHeXWV0I6p2DobrA/vj/AEE8/9A9+hBiEgCf/8"
    "WUg8f/h28RJPRDm56QywP+VYxCCWhNwgaYhNKH75FX7bFKQPtY9/pYReObZug/wXjxkNTm"
    "fiKypdHvECG+d9t/0eoqxn8eaa1/a/1b678N1n/hawOd174Eat21Sc6uD7R3JMtjdnkoNf"
    "bxD1jqu2Ay06Q6XGYoOyoXXE7QeDLQzBeUMKZOkiN2F5HU9otfEnhZ+2lDEWo/blhh9svi"
    "S4Vq3Mpgy66s3GfaiYh5iKmvezyNIBlQQHTJWwWaSqF1qB2A58U61A7ysTbNoTaY4Kij8K"
    "SJuu5GF1rMxGxS9WG4yPiz1PLiZABTta3d4LdWp2LD5sY7CoN186Oo326OdNhSIbAT5QFN"
    "lOx56k+WS5CpE6Z5+/XXf1iED2fQ1xh5S/l26ZtalfRAYdusia1KqEpjbw/Uvc9k2CS9TE"
    "GgXrSIyi00Mpez2vhAtDF/mHqqOEOYqofxkLJrV3EoyUjrUWqao9DmuRzqkvQlRMrEN1G3"
    "WfGxR7T/TDfe1ip5bhnO6kKb5bbzLLdp8oppDFqbBJP/AtSeUqOxcYQ9pWY7puwpNdUcIu"
    "kBdS8VNcYqvl3eJXNMxz4kyJ10SgzHpGat2Qgymca4SpQD0x5vkX1cCknMm6RhsOQg7bRZ"
    "eufnWxgtTEpptYi6wjekUYluUZOYiLeTwJPj423WKMfH6jUKryueiRZSWJbNp/7sNgfZ14"
    "e275ZlehinKH3/P5z4AWA="
)
