from datetime import datetime

from pydantic import BaseModel, field_validator

class Scrobble(BaseModel):
    track_name: str
    artist_name: str
    album_name: str | None = None
    scrobbled_at: datetime
    mbid: str | None = None
    
    @field_validator("mbid", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        return v if v else None
    
    @field_validator("album_name", mode="before")
    @classmethod
    def empty_album_to_none(cls, v):
        return v if v else None
    
    