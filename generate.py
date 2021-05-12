# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import json
import sys

from jinja2 import Environment, FileSystemLoader

log = logging.getLogger(__name__)


OUTPUT_FOLDER = 'test/output'


def list_files(folder_path):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

def read_file(file_path):
    with open(file_path, 'r') as f:
        raw_metadata = ""
        for line in f:
            if line.strip() == '---':
                break
            raw_metadata += line
        content = ""
        for line in f:
            content += line
    return json.loads(raw_metadata), content

def write_output(name, html):
    # TODO should not use sys.argv here, it breaks encapsulation
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    with open(os.path.join(OUTPUT_FOLDER, f'{name}.html'), 'w') as f:
        f.write(html)

def generate_site(folder_path):
    log.info("Generating site from %r", folder_path)
    jinja_env = Environment(loader=FileSystemLoader(f'{folder_path}/layout'))
    for file_path in list_files(folder_path):
        metadata, content = read_file(file_path)
        template_name = metadata['layout']
        template = jinja_env.get_template(template_name)
        data = dict(metadata, content=content)
        html = template.render(data)
        name = os.path.splitext(os.path.basename(file_path))[0]
        write_output(name, html)
        log.info("Writing %r with template %r", name, template_name)


def main():
    generate_site(sys.argv[1])


if __name__ == '__main__':
    logging.basicConfig()
    main()
