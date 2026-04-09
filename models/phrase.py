from dataclasses import dataclass
from datetime import datetime

@dataclass
class Phrase:
    id: int | None
    title: str
    content: str
    category: str
    tags: str          # با کاما جدا میشه
    created_at: str
    updated_at: str

    @staticmethod
    def empty():
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return Phrase(
            id=None,
            title="",
            content="",
            category="عمومی",
            tags="",
            created_at=now,
            updated_at=now
        )
