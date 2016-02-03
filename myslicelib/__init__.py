import sys

try:
    assert sys.version_info >= (3,5)
except AssertionError:
    exit("MySlice Lib requires Python 3.5")