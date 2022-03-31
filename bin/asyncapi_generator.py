import yaml
import yamlloader
from jacobsjinjatoo import templator as jj2

from stingeripc.asyncapi import AsyncApiCreator

if __name__ == '__main__':
    inname = sys.argv[1]
    outdir = sys.argv[2]
    outname_template = "%s-{}.asyncapi.yaml" % (os.path.splitext(os.path.basename(inname))[0])
    outname_server = os.path.join(outdir, outname_template.format("server"))
    outname_client = os.path.join(outdir, outname_template.format("client"))
    outname_common = os.path.join(outdir, outname_template.format("common"))
    idef = yaml.load(open(inname), Loader=yaml.Loader)
    converter = AsyncApiCreator()
    converter.add_stinger(idef)
    a2s_server = converter.get_asyncapi(SpecType.SERVER)
    yaml.dump(a2s_server, open(outname_server, 'w'), Dumper=yamlloader.ordereddict.CDumper)
    a2s_client = converter.get_asyncapi(SpecType.CLIENT)
    yaml.dump(a2s_client, open(outname_client, 'w'), Dumper=yamlloader.ordereddict.CDumper)
    params = {
        "a2s": converter,
        "stinger": idef,
    }
    t = jj2.CodeTemplator(output_dir=os.path.dirname(sys.argv[2]))
    t.add_template_dir(os.path.join(os.path.dirname(__file__), "templates", "python"))
    t.render_template("server.py.jinja2", "server.py", **params)