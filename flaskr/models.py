from pydantic import BaseModel
from datetime import datetime

class DisasterData(BaseModel):
    id: int
    event_type: str
    location: str
    timestamp: datetime
    severity: int
