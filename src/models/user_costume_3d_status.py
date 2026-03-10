from tortoise import Model, fields

from src.enum.user_costume_status import UserCostumeStatus
class UserCostume3DStatus(Model):
    id = fields.IntField(primary_key=True)
    
    userId = fields.BigIntField()
    
    costumeId = fields.IntField()
    status = fields.CharEnumField(UserCostumeStatus)
    obtainedAt = fields.DatetimeField(null=True)
    
    class Meta:
        table = "user_costumes"