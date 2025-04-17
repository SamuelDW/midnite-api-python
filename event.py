from pydantic import BaseModel

class Event(BaseModel):
    user_id: int
    type: str
    time: int
    amount: float