import enum

class attributeTypes(enum.Enum):
    NOMINAL = 1
    NUMERICAL = 2
    CATEGORICAL = 3
    VECTOR = 4

def isFlagOnPosition(mask, pos):
    return ((mask >> pos) & 1) != 0

def intToType(int):
    return attributeTypes(int).name

def typeToint(type):
    return attributeTypes[type].value