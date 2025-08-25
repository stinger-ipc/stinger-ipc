import os
import sys
from jacobsjinjatoo import templator as jj2

from stingeripc import StingerInterface

def main():
    inname = sys.argv[1]
    outdir = sys.argv[2]
    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
    }
    t = jj2.CodeTemplator(output_dir=os.path.dirname(outdir))
    t.add_template_dir(
        os.path.join(os.path.dirname(__file__), "../templates", "markdown")
    )
    for output_file in [
        "index.md",
    ]:
        t.render_template(f"{output_file}.jinja2", output_file, **params)

if __name__ == '__main__':
    main()