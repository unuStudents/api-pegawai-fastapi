from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.pegawai import pegawai

app = FastAPI()


def cors_headers(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    return app


app.include_router(pegawai)


@app.get("/")
async def root():
    return "work!"
