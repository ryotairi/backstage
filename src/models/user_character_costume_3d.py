from tortoise import Model, fields


class UserCharacterCostume3D(Model):
    id = fields.IntField(primary_key=True)
    
    userId = fields.BigIntField()
    characterId = fields.IntField()
    unit = fields.CharField(max_length=16)
    
    hairCostume3dId = fields.IntField()
    headCostume3dId = fields.IntField()
    bodyCostume3dId = fields.IntField()
    
    class Meta:
        table = 'user_character_costumes_3d'