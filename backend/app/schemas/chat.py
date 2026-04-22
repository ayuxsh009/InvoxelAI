from pydantic import BaseModel, Field


class ChatQueryRequest(BaseModel):
    message: str = Field(min_length=5, max_length=500)


class ChatQueryResponse(BaseModel):
    interpreted_filter: str
    count: int
    invoices: list[dict]
