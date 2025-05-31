from pydantic import BaseModel, Field, model_validator, GetCoreSchemaHandler
from pydantic_core import core_schema
from datetime import datetime
from bson import ObjectId

class MyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(cls.validate)
            ],
            serialization=core_schema.to_string_ser_schema()
        )

    @classmethod
    def validate(cls, value):
        if isinstance(value, ObjectId):
            return value
        try:
            return ObjectId(str(value))
        except Exception:
            raise ValueError("Invalid ObjectId")


class Document(BaseModel):
    body: str
    topics: list = []
    metadata: dict = {}
    cluster_id: int
    createdAt: datetime
    updatedAt: datetime
    version: int = Field(default=0, alias="__v")

class Cluster(BaseModel):
    cluster_id: int
    tags: list = []
    createdAt: datetime
    updatedAt: datetime
    version: int = Field(default=0, alias="__v")

class Tag(BaseModel):
    name: str
    createdAt: datetime
    updatedAt: datetime
    version: int = Field(default=0, alias="__v")

#TODO прибрати після обговорення
class Topic(BaseModel):
    name: str
    isRoot: bool = True
    parent: MyObjectId = None
    createdAt: datetime
    updatedAt: datetime
    version: int = Field(default=0, alias="__v")

    @model_validator(mode="after")
    def parent_must_exist(self):
        if  (self.isRoot and self.parent is not None) or \
            (not self.isRoot and self.parent is None):
            raise ValueError("parent field can't be " + str(self.parent) + " when isRoot is " + str(self.isRoot))
        else:
            return self