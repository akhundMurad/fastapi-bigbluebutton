from pydantic import BaseModel


class BigbluebuttonServer(BaseModel):
    name: str
    url: str
    secret_key: str
