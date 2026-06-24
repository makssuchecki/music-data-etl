from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

class Scrobble(BaseModel):
    track_name: str
    artist_name: str
    album_name: Optional[str] = None
    scrobbled_at: datetime
    mbid: Optional[str] = None

    @field_validator("mbid", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        return v if v else None
    
    @field_validator("album_name", mode="before")
    @classmethod
    def empty_album_to_none(cls, v):
        return v if v else None
    
    