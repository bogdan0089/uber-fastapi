from enum import Enum




class Role(Enum):
    passenger = "passenger"
    driver = "driver"



class Status(Enum):
    waiting = "waiting"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


