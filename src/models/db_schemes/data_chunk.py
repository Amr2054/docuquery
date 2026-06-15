"""
Mongodb Scheme for chunks
"""

from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    # _id is private so to read the id we use id only as a name
    # and use alias _id and adapt mongo functions to handle alias
    id: Optional[ObjectId] = Field(None, alias="_id")

    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0) # greater than 0
    chunk_project_id: ObjectId # connection to project_id

    # to suppress ObjectId type error
    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def get_indexes(cls):
        # initialize an index for faster retrieval
        return [
            {
                "key":[
                    ("chunk_project_id", 1) # 1: ascending order
                ],
                "name": "chunk_project_id_index_1",
                "unique": False, # multiple chunks share same project_id
            }
        ]