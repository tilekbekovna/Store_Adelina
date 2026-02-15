"""empty message

Revision ID: f424fcaf4041
Revises: eb30d0ec55a7
Create Date: 2026-02-12 19:36:35.599843
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f424fcaf4041'
down_revision: Union[str, Sequence[str], None] = 'eb30d0ec55a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # ### commands fixed for safe ENUM usage ###
    op.create_table(
        'profile',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('first_name', sa.String(length=30), nullable=False),
        sa.Column('last_name', sa.String(length=50), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.Column('phone_number', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('gold', 'sliver', 'bronze', 'simple', name='statuschoices', create_type=False), nullable=False),
        sa.Column('data_register', sa.Date(), nullable=False),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    op.create_table(
        'refresh_token',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('created_date', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['profile.id']),
    )

    # Fix foreign key in review table
    op.drop_constraint(op.f('review_user_id_fkey'), 'review', type_='foreignkey')
    op.create_foreign_key(None, 'review', 'profile', ['user_id'], ['id'])

def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key first
    op.drop_constraint(None, 'review', type_='foreignkey')
    op.create_foreign_key(op.f('review_user_id_fkey'), 'review', 'profile', ['user_id'], ['id'])

    # Drop tables
    op.drop_table('refresh_token')
    op.drop_table('profile')
