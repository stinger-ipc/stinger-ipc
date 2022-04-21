from jacobsjinjatoo import templator as jj2
import sys
import yaml
import os

libpath = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")
)
sys.path.append(libpath)

from stingeripc import StingerInterface

if __name__ == "__main__":
    inname = sys.argv[1]
    outdir = sys.argv[2]
    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
    }

    source_code_dir = os.path.join(outdir, "src")
    if not os.path.exists(source_code_dir):
        os.makedirs(source_code_dir)

    template_dir = os.path.join(os.path.dirname(__file__), "../stingeripc", "templates", "rust")

    t = jj2.CodeTemplator(output_dir=os.path.dirname(outdir))
    t.add_template_dir(template_dir)
    t.render_template("Cargo.toml.jinja2", "Cargo.toml", **params)

    source_code_template_dir = os.path.join(template_dir, "src")
    for f in os.listdir(source_code_template_dir):
        source_code_path = os.path.join("src", f)
        if f.endswith(".jinja2"):
            t.render_template(source_code_path, source_code_path[:-len(".jinja2")], **params)