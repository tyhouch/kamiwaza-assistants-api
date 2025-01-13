"""Create assistant table

Revision ID: 6360e9e2b60e
Revises: 
Create Date: 2025-01-13 12:17:57.458275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6360e9e2b60e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assistants',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('object', sa.String(), nullable=True),
    sa.Column('created_at', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('description', sa.String(length=512), nullable=True),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('instructions', sa.Text(), nullable=True),
    sa.Column('tools', sa.JSON(), nullable=True),
    sa.Column('tool_resources', sa.JSON(), nullable=True),
    sa.Column('meta_data', sa.JSON(), nullable=True),
    sa.Column('temperature', sa.Float(), nullable=True),
    sa.Column('top_p', sa.Float(), nullable=True),
    sa.Column('response_format', sa.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assistants')
    # ### end Alembic commands ###