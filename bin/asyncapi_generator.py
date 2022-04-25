import os
import sys

from stingeripc.asyncapi import AsyncApiCreator
from stingeripc import StingerInterface

libpath = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
)
sys.path.append(libpath)

if __name__ == '__main__':
    inname = sys.argv[1]
    outdir = sys.argv[2]

    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
    }

    converter = AsyncApiCreator()
