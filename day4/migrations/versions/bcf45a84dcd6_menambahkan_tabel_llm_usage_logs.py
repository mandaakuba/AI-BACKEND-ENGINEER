"""Menambahkan tabel llm_usage_logs

Revision ID: bcf45a84dcd6
Revises: 
Create Date: 2026-06-29 15:07:17.418338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcf45a84dcd6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Kita biarkan perintah untuk bikin tabel llm_usage_logs saja
    op.create_table('llm_usage_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=True),
    sa.Column('prompt_text', sa.String(length=500), nullable=False),
    sa.Column('tokens_used', sa.Integer(), nullable=False),
    sa.Column('latency_ms', sa.Float(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_llm_usage_logs_id'), 'llm_usage_logs', ['id'], unique=False)
    op.create_index(op.f('ix_llm_usage_logs_user_id'), 'llm_usage_logs', ['user_id'], unique=False)
    
    # PERINTAH DROP TABLE ORDERS DAN CUSTOMERS SUDAH GUE HAPUS DI SINI


def downgrade() -> None:
    """Downgrade schema."""
    # Kalau kita mau ngebatalin (downgrade) revisi ini, 
    # cukup hapus tabel llm_usage_logs aja.
    op.drop_index(op.f('ix_llm_usage_logs_user_id'), table_name='llm_usage_logs')
    op.drop_index(op.f('ix_llm_usage_logs_id'), table_name='llm_usage_logs')
    op.drop_table('llm_usage_logs')
    
    # PERINTAH CREATE TABLE CUSTOMERS DAN ORDERS (YANG SALAH) SUDAH GUE HAPUS DI SINI