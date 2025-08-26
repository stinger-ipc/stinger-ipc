from jacobsjinjatoo import templator as jj2
from jacobsjinjatoo import stringmanip
import sys
import os.path

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
        os.path.join(os.path.dirname(__file__), "../templates", "python")
    )
    for output_file in [
        "pyproject.toml",
    ]:
        t.render_template(f"{output_file}.jinja2", output_file, **params)

    generated_src_dir = os.path.join(outdir, f"{stringmanip.lower_camel_case(stinger.name).lower()}ipc")
    os.makedirs(generated_src_dir, exist_ok=True)
    for output_file in [
        "server.py",
        "client.py",
        "connection.py",
        "__init__.py",
        "method_codes.py",
    ]:
        t.render_template(f"{output_file}.jinja2", os.path.join(stinger.name.lower(), output_file), **params)

    t.render_template("interface_types.py.jinja2", os.path.join(stinger.name.lower(), f"{stinger.get_enum_module_name()}.py"), **params)

if __name__ == "__main__":
    main()