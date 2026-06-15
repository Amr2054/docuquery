from typing import Optional
from pydantic import BaseModel

# How the input data coming from endpoint should look like
class ProcessRequest(BaseModel):
    file_id: str = None # optional
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0

