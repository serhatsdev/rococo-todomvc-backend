from dataclasses import dataclass
from rococo.models import VersionedModel

@dataclass
class Todo(VersionedModel):
    """
    A model representing a Todo item.
    """

    person_id: str = None
    title: str = None
    is_completed: bool = False
