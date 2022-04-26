import os
import sys
import yaml
import yamlloader

libpath = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
)
sys.path.append(libpath)

from stingeripc import StingerInterface, StingerToAsyncApi

if __name__ == '__main__':
    inname = sys.argv[1]
    outdir = sys.argv[2]

    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)

    converter = StingerToAsyncApi(stinger)
    asyncapi_spec = converter.get_asyncapi()

    with open(os.path.join(outdir, "asyncapi.yaml"), "w") as f:
        yaml.dump(asyncapi_spec, f, Dumper=yamlloader.ordereddict.CDumper)
