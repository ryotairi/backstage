from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_episode_statuses" ADD "continuousPlayStart" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "user_episode_statuses" ADD "useAuto" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "user_episode_statuses" ADD "fastForward" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "user_episode_statuses" ADD "autoFinish" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "user_episode_statuses" ADD "playMusicVideo" BOOL NOT NULL DEFAULT False;
        ALTER TABLE "user_episode_statuses" ADD "voice" BOOL NOT NULL DEFAULT False;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_episode_statuses" DROP COLUMN "continuousPlayStart";
        ALTER TABLE "user_episode_statuses" DROP COLUMN "useAuto";
        ALTER TABLE "user_episode_statuses" DROP COLUMN "fastForward";
        ALTER TABLE "user_episode_statuses" DROP COLUMN "autoFinish";
        ALTER TABLE "user_episode_statuses" DROP COLUMN "playMusicVideo";
        ALTER TABLE "user_episode_statuses" DROP COLUMN "voice";"""


MODELS_STATE = (
    "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"
    "4zkF0ttH2zLNP9OEXpx786C5dY"
)
