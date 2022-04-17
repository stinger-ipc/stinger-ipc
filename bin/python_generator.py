from jacobsjinjatoo import templator as jj2
import sys
import yaml
import os.path

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
    t = jj2.CodeTemplator(output_dir=os.path.dirname(outdir))
    t.add_template_dir(
        os.path.join(os.path.dirname(__file__), "../stingeripc", "templates", "python")
    )
    for output_file in [
        "server.py",
        "client.py",
        "connection.py",
        "__init__.py",
        "requirements.txt",
    ]:
        t.render_template(f"{output_file}.jinja2", output_file, **params)

    if stinger.uses_enums():
        t.render_template("interface_enums.py.jinja2", "interface_enums.py", **params)
