import os
import sys
from ruamel.yaml import YAML
from stingeripc.loading import parse_yaml_file
from stingeripc.config import StingerConfig

libpath = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
)
sys.path.append(libpath)

from stingeripc import StingerInterface, StingerToAsyncApi

if __name__ == '__main__':
    inname = sys.argv[1]
    outdir = sys.argv[2]

    config = StingerConfig()
    stinger = StingerInterface.from_yaml(inname, config)

    converter = StingerToAsyncApi(stinger)
    asyncapi_spec = converter.get_asyncapi()

    yaml = YAML()
    yaml.default_flow_style = False
    with open(os.path.join(outdir, "asyncapi.yaml"), "w") as f:
        yaml.dump(asyncapi_spec, f)
