"""add message table

Revision ID: c7172cb47cde
Revises: ed8339c7e616
Create Date: 2024-12-17 14:09:14.894334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'c7172cb47cde'
down_revision: Union[str, None] = 'ed8339c7e616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('payment_link', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('qr_data', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('is_sent', sa.Boolean(), nullable=False),
    sa.Column('send_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###
