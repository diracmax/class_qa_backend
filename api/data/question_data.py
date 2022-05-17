from dataclasses import dataclass
import datetime


@dataclass
class QuestionData:
    id: int
    class_id: str
    user_id: str
    content: str
    created_at: datetime.datetime
