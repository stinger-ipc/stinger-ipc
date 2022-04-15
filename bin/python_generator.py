
from jacobsjinjatoo import templator as jj2
import sys
import yaml
import os.path

libpath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))
sys.path.append(libpath)

from stingeripc import StingerInterface

if __name__ == '__main__':
    inname = sys.argv[1]
    outdir = sys.argv[2]
    with open(inname, 'r') as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
    }
    t = jj2.CodeTemplator(output_dir=os.path.dirname(outdir))
    t.add_template_dir(os.path.join(os.path.dirname(__file__), "../stingeripc", "templates", "python"))
    t.render_template("server.py.jinja2", "server.py", **params)
    t.render_template("client.py.jinja2", "client.py", **params)
    t.render_template("connection.py.jinja2", "connection.py", **params)
    t.render_template("__init__.py.jinja2", "__init__.py", **params)
