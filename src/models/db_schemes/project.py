"""
Mongodb Scheme (how data is structured inside database) for project number
"""

from pydantic import BaseModel, Field, validator, ValidationError, field_validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1) # should be alphanumeric only

    @field_validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValidationError('Project ID must be alphanumeric')

        return value

    # to suppress ObjectId type error
    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def get_indexes(cls):
        # initialize an index for faster retrieval
        return [
            {
                "key":[
                    ("project_id", 1) # 1: ascending order
                ],
                "name": "project_id_index_1",
                "unique": True, # no repeated project_id
            }
        ]