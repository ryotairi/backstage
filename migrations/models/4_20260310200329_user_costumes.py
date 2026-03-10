from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user_costumes" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "userId" BIGINT NOT NULL,
    "costumeId" INT NOT NULL,
    "status" VARCHAR(9) NOT NULL,
    "obtainedAt" TIMESTAMPTZ
);
COMMENT ON COLUMN "user_costumes"."status" IS 'forbidden: forbidden\nsale: sale\navailable: available';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "user_costumes";"""


MODELS_STATE = (
    "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"
)
