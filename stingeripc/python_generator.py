from jacobsjinjatoo import templator as jj2
import sys
import yaml
import os.path
import topics
import payload

if __name__ == '__main__':
    inname = sys.argv[1]
    outdir = sys.argv[2]
    idef = yaml.load(open(inname), Loader=yaml.Loader)
    params = {
        "stinger": idef,
        "topics": topics.TopicCreator(),
        "payload": payload.payload_parser, 
    }
    t = jj2.CodeTemplator(output_dir=os.path.dirname(outdir))
    t.add_template_dir(os.path.join(os.path.dirname(__file__), "templates", "python"))
    t.render_template("server.py.jinja2", "server.py", **params)
