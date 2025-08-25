from jacobsjinjatoo import templator as jj2
import sys
import yaml
import os
import shutil

from stingeripc import StingerInterface

def main():
    inname = sys.argv[1] # Path to the stinger file
    outdir = sys.argv[2] # Directory to which the files should be written
    with open(inname, "r") as f:
        stinger = StingerInterface.from_yaml(f)
    params = {
        "stinger": stinger,
    }

    if not os.path.exists(outdir):
        os.makedirs(outdir)

    template_dir = os.path.join(os.path.dirname(__file__), "../templates", "rust")

    t = jj2.CodeTemplator(output_dir=os.path.dirname(outdir))
    t.add_template_dir(template_dir)

    def recursive_render_templates(local_dir: str):
        cur_template_dir = os.path.join(template_dir, local_dir)
        for entry in os.listdir(cur_template_dir):
            if entry == 'target':
                # Do not copy 'target' dir
                continue
            entry_full_path = os.path.join(cur_template_dir, entry)
            entry_local_path = os.path.join(local_dir, entry)
            if entry.endswith(".jinja2"):
                print(f"GENER: {entry_local_path}")
                t.render_template(entry_local_path, entry_local_path[:-len(".jinja2")], **params)
            elif os.path.isdir(entry_full_path):
                print(f"MKDIR: {entry_local_path}")
                new_dir = os.path.join(outdir, entry_local_path)
                if not os.path.exists(new_dir):
                    os.makedirs(new_dir)
                recursive_render_templates(entry_local_path)
            elif os.path.isfile(entry_full_path):
                shutil.copyfile(entry_full_path, os.path.join(outdir, entry_local_path))
                print(f"COPY:  {entry_local_path}")

    recursive_render_templates(".")

if __name__ == "__main__":
    main()