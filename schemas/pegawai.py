# schemas/pegawai.py
from datetime import date
from pydantic import BaseModel, Field
from typing import List


class PegawaiSchema(BaseModel):
    nama_pegawai: str = Field(..., min_length=3, max_length=255)
    alamat_pegawai: str = Field(..., min_length=3, max_length=255)
    ttl_pegawai: date = Field(...)
    whatsapp_pegawai: str = Field(..., min_length=3, max_length=255)
    email_pegawai: str = Field(..., min_length=3, max_length=50)


class Pegawai(PegawaiSchema):
    id_pegawai: int


# list pegawai API
class Pegawais(BaseModel):
    limit: int = Field(default=5)
    offset: int = Field(default=0)
    data: List[Pegawai]
