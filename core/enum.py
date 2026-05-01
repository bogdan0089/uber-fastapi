from enum import Enum




class Role(Enum):
    PASSENGER = "passenger"
    DRIVER = "driver"
    ADMIN = "admin"


class Status(Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


