from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user_configs" (
    "userId" BIGSERIAL NOT NULL PRIMARY KEY,
    "defaultMusicType" VARCHAR(14) NOT NULL,
    "displayLoginStatus" BOOL NOT NULL,
    "friendRequestScope" VARCHAR(9) NOT NULL
);
COMMENT ON COLUMN "user_configs"."defaultMusicType" IS 'original: original_music\nsekai: sekai';
COMMENT ON COLUMN "user_configs"."friendRequestScope" IS 'all: all\nid_search: id_search\nreject: reject';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_configs";"""


MODELS_STATE = (
    "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"
)
