def isFlagOnPosition(mask, pos):
    return ((mask >> pos) & 1) != 0