# routes/pegawai.py
from schemas.pegawai import PegawaiSchema, Pegawais
from models.pegawai import Pegawai
from fastapi import APIRouter, Response, status
from config.database import conn

pegawai = APIRouter()


@pegawai.get(
    "/pegawai/all", response_model=Pegawais, description="Menampilkan semua data"
)
async def find_all_pegawai(limit: int = 10, offset: int = 0):
    query = Pegawai.select().offset(offset).limit(limit)
    data = conn.execute(query).fetchall()
    response = {"limit": limit, "offset": offset, "data": data}
    return response


@pegawai.get("/pegawai/{id}", description="Menampilkan detail data")
async def find_pegawai(id: int, response: Response):
    query = Pegawai.select().where(Pegawai.c.id_pegawai == id)
    """
    Kenapa pakai huruf c pada Pegawai.c ?
    karena memakai ImmutableColumnCollection
    untuk melihat apa isinya silahkan uncomment print dibawah ini 
    dan lihat di terminal/cmd
    """
    # print(Pegawai.c)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "data tidak ditemukan", "status": response.status_code}

    response = {"message": f"sukses mengambil data dengan id {id}", "data": data}
    return response


@pegawai.post("/pegawai/", description="Menambah data pegawai")
async def insert_pegawai(pgw: PegawaiSchema, response: Response):

    cek_email = Pegawai.select().filter(Pegawai.c.email_pegawai == pgw.email_pegawai)
    cek_email = conn.execute(cek_email).fetchone()
    if cek_email is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": response.status_code, "message": "email sudah digunakan"}

    query = Pegawai.insert().values(
        nama_pegawai=pgw.nama_pegawai,
        alamat_pegawai=pgw.alamat_pegawai,
        ttl_pegawai=pgw.ttl_pegawai,
        whatsapp_pegawai=pgw.whatsapp_pegawai,
        email_pegawai=pgw.email_pegawai,
    )
    # print(query)
    conn.execute(query)
    data = Pegawai.select().order_by(Pegawai.c.id_pegawai.desc())
    response = {
        "message": f"sukses menambahkan data baru",
        "data": conn.execute(data).fetchone(),
    }
    return response


@pegawai.post("/pegawai/{id}", description="mengubah data pegawai")
async def update_pegawai(id: int, pgw: PegawaiSchema, response: Response):

    cek_email = Pegawai.select().filter(
        Pegawai.c.email_pegawai == pgw.email_pegawai, Pegawai.c.id_pegawai != id
    )
    cek_email = conn.execute(cek_email).fetchone()
    if cek_email is not None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": response.status_code, "message": "email sudah digunakan"}

    query = (
        Pegawai.update()
        .values(
            nama_pegawai=pgw.nama_pegawai,
            alamat_pegawai=pgw.alamat_pegawai,
            ttl_pegawai=pgw.ttl_pegawai,
            telp_pegawai=pgw.telp_pegawai,
            email_pegawai=pgw.email_pegawai,
        )
        .where(Pegawai.c.id_pegawai == id)
    )
    # print(query)
    conn.execute(query)
    data = Pegawai.select().where(Pegawai.c.id_pegawai == id)
    response = {
        "message": f"sukses mengubah data dengan id {id}",
        "data": conn.execute(data).fetchone(),
    }
    return response


@pegawai.delete("/pegawai/{id}", description="menghapus data pegawai")
async def hapus_pegawai(id: int, response: Response):

    query = Pegawai.select().where(Pegawai.c.id_pegawai == id)
    data = conn.execute(query).fetchone()
    if data is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "data tidak ditemukan", "status": response.status_code}

    query = Pegawai.delete().where(Pegawai.c.id_pegawai == id)
    conn.execute(query)
    response = {"message": f"sukses menghapus data dengan id {id}"}
    return response
