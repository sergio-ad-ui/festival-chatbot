from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str  # "user" o "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class Conversation(BaseModel):
    sender_id: str
    messages: List[Message] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_updated: datetime = Field(default_factory=datetime.now)


class FestivalInfo(BaseModel):
    category: str  # Esempio: "location", "orari", "artisti", "map", ecc.
    content: str
    priority: int = 0  # Priorità per l'ordinamento
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class MapPoint(BaseModel):
    name: str
    description: str
    latitude: float
    longitude: float
    type: str  # "stage", "food", "toilet", "entrance", ecc.


class Event(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    artists: List[str] = [] 