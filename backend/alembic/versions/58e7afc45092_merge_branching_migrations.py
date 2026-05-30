"""merge branching migrations

Revision ID: 58e7afc45092
Revises: 51ab6a0e2152, b7e2a1f3d890
Create Date: 2026-05-29 19:36:37.838926

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "58e7afc45092"
down_revision: Union[str, Sequence[str], None] = ("51ab6a0e2152", "b7e2a1f3d890")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
