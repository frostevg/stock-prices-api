from pydantic import BaseModel


class Symbol(BaseModel):
    symbol: str
    company_name: str

