hoge: int = 100
hoge = hoge + 2
hoge, _ = (100, 0)


def foo():
    hoge = 3
    return hoge


"""
ERRORS:
    :2:0:RAC001 variable "hoge" (defined in line 1) has been reassigned.
    :3:0:RAC001 variable "hoge" (defined in line 1) has been reassigned.
"""
