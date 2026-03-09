from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_music_results" ALTER COLUMN "mvpCount" SET DEFAULT 0;
        ALTER TABLE "user_music_results" ALTER COLUMN "superStarCount" SET DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user_music_results" ALTER COLUMN "mvpCount" DROP DEFAULT;
        ALTER TABLE "user_music_results" ALTER COLUMN "superStarCount" DROP DEFAULT;"""


MODELS_STATE = (
    "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"
    "0BsqtVs2+WX7ofRyL9+D8jAIKa"
)
