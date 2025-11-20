from pydantic import BaseModel
import uuid

class OrderItem(BaseModel):
    food_id: uuid.UUID
    quantity: int