from typing import List

from pydantic import BaseModel

class Playlist(BaseModel):
    emotion: str
    genres: List[str] = None
    tempo: float = 0.5
    length: int = 20
    orderBy: str = "Popularity"



