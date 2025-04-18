from pydantic import BaseModel

class RequestData(BaseModel):
    user_id: int
    type: str
    time: int
    amount: float