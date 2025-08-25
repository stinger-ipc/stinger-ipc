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
        "pyproject.toml",
    ]:
        t.render_template(f"{output_file}.jinja2", output_file, **params)

    generated_src_dir = os.path.join(outdir, stinger.name.lower())
    os.makedirs(generated_src_dir, exist_ok=True)
    for output_file in [
        "server.py",
        "client.py",
        "connection.py",
        "__init__.py",
        "method_codes.py",
    ]:
        print(f"CREATE {output_file}")
        t.render_template(f"{output_file}.jinja2", os.path.join(stinger.name.lower(), output_file), **params)

    print(f"CREATE interface_types.py")
    t.render_template("interface_types.py.jinja2", os.path.join(stinger.name.lower(), f"{stinger.get_enum_module_name()}.py"), **params)
