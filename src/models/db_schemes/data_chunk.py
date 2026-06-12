"""
Mongodb Scheme for chunks
"""

from pydantic import BaseModel, Field, validator, ValidationError, field_validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId]

    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0) # greater than 0
    chunk_project_id: ObjectId # connection to project_id

    # to suppress ObjectId type error
    class Config:
        arbitrary_types_allowed = True