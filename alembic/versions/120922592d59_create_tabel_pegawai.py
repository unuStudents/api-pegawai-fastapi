"""create tabel pegawai

Revision ID: 120922592d59
Revises: 
Create Date: 2022-05-21 19:51:02.375248

"""
from datetime import tzinfo
from enum import unique
from tkinter.messagebox import NO
from alembic import op
import faker
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '120922592d59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    pegawai = op.create_table(
        'data_pegawai',
        sa.Column('id_pegawai', sa.Integer, primary_key=True),
        sa.Column('nama_pegawai', sa.String(255), nullable=False),
        sa.Column('alamat_pegawai', sa.String(255)),
        sa.Column('ttl_pegawai', sa.Date()),
        sa.Column('whatsapp_pegawai', sa.String(15)),
        sa.Column('email_pegawai', sa.String(50), unique=True),
    )
    op.bulk_insert(
        pegawai,
        [
            {
                'nama_pegawai':faker.name(),
                'alamat_pegawai':faker.address(),
                'ttl_pegawai':faker.date_of_birth(tzinfo=None, minimum_age=19, maximum_age=30),
                'ttl_pegawai':faker.whatsapp(),
                'ttl_pegawai':faker.email(),
            } for x in range(800)
        ]
    )


def downgrade():
    op.drop_table('data_pegawai')
