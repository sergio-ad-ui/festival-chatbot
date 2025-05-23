from datetime import datetime
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str  # "user" o "assistant"
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)


class Conversation(BaseModel):
    sender_id: str
    context: Optional[str] = "festival"  # Nuovo campo per il contesto
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


# Nuovi modelli per il sistema multi-contesto
class Context(BaseModel):
    code: str  # "festival", "apt_brescia", ecc.
    name: str
    type: str  # "festival", "apartment", "business", ecc.
    welcome_message: str
    system_prompt: str
    active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ApartmentInfo(BaseModel):
    context_code: str
    category: str  # "check_in", "wifi", "rules", "amenities", ecc.
    content: str
    priority: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class LocalService(BaseModel):
    context_code: str
    type: str  # "restaurant", "pharmacy", "supermarket", "attraction", ecc.
    name: str
    description: str
    address: Optional[str] = None
    distance: Optional[str] = None
    google_maps_url: Optional[str] = None
    phone: Optional[str] = None
    opening_hours: Optional[str] = None
    rating: Optional[float] = None
    price_range: Optional[str] = None  # "€", "€€", "€€€"
    created_at: datetime = Field(default_factory=datetime.now)


class SmartHomeInstruction(BaseModel):
    context_code: str
    device: str  # "ttlock", "wifi", "tv", "air_conditioning", ecc.
    title: str
    instructions: str
    troubleshooting: List[str] = []
    video_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now) 