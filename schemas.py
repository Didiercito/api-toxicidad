from pydantic import BaseModel


class TextoEntrada(BaseModel):
    texto: str


class RespuestaPrediccion(BaseModel):
    texto: str
    toxicidad: int
    probabilidad: float
