"""Remove task dependency from files

Revision ID: 7f34c79eec06
Revises: d7108133e7e4
Create Date: 2026-10-25 22:39:45.748782
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# Revision identifiers, used by Alembic.
revision: str = '7f34c79eec06'
down_revision: Union[str, Sequence[str], None] = 'd7108133e7e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove the task dependency from file_table."""

    # 1. Drop the foreign key before dropping its index.
    op.drop_constraint(
        op.f('file_table_ibfk_1'),
        'file_table',
        type_='foreignkey'
    )

    # 2. Drop the index associated with task_id.
    op.drop_index(
        op.f('ix_file_table_task_id'),
        table_name='file_table'
    )

    # 3. Remove the task_id column.
    op.drop_column(
        'file_table',
        'task_id'
    )


def downgrade() -> None:
    """Restore the task dependency to file_table."""

    # 1. Restore task_id as nullable because existing files
    # no longer have their original task associations.
    op.add_column(
        'file_table',
        sa.Column(
            'task_id',
            mysql.INTEGER(),
            autoincrement=False,
            nullable=True
        )
    )

    # 2. Restore the foreign key.
    op.create_foreign_key(
        op.f('file_table_ibfk_1'),
        'file_table',
        'test_table',
        ['task_id'],
        ['id'],
        ondelete='CASCADE'
    )

    # 3. Restore the index.
    op.create_index(
        op.f('ix_file_table_task_id'),
        'file_table',
        ['task_id'],
        unique=False
    )