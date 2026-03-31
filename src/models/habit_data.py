from dataclasses import dataclass

@dataclass
class HabitData:
    name: str
    icon: str
    streak: int
    frequency: str
    reminder_time: str | None = None
    completed: bool = False
