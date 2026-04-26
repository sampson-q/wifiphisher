"""Typed runtime context for session-scoped mutable state."""

from dataclasses import dataclass, field
from time import time
from uuid import uuid4


@dataclass
class RuntimeContext:
    """Holds runtime state that was previously kept in globals."""

    session_id: str = field(default_factory=lambda: uuid4().hex)
    started_at: float = field(default_factory=time)
    cli_args: object = None
    discovered_aps: dict = field(default_factory=dict)

    def set_cli_args(self, cli_args):
        """Set parsed CLI arguments for the current session."""
        self.cli_args = cli_args

    def reset_discovered_aps(self):
        """Clear cached discovered APs."""
        self.discovered_aps = {}

