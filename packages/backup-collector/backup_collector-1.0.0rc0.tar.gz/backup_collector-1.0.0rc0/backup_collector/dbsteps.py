from enum import IntEnum, auto

class DBStep(IntEnum):
    CREATE = auto() #1
    CONNECT = auto()
    COLLECT = auto()
    DELETE = auto()  #4

class DBSend(IntEnum):
    CREATE = auto() #1
    CONNECT = auto()
    SEND = auto() #3
