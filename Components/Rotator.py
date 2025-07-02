#! python3


def rotatorright(thirty2bit: str, rotateby: int=1):

    return thirty2bit[-rotateby:] + thirty2bit[:-rotateby]
