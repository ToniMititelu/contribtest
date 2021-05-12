# generate site from static pages, loosely inspired by Jekyll
# run like this:
#   ./generate.py test/source output
# the generated `output` should be the same as `test/expected_output`

import os
import logging
import json
import sys

from jinja2 import Environment, FileSystemLoader
from typing import Dict, Union

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


OUTPUT_FOLDER = 'test/output'


def list_files(folder_path: str):
    for name in os.listdir(folder_path):
        base, ext = os.path.splitext(name)
        if ext != '.rst':
            continue
        yield os.path.join(folder_path, name)

def read_file(file_path) -> Dict[str, str]:
    separator_found = False
    with open(file_path, 'r') as f:
        raw_metadata = content = ""
        for line in f:
            if line.strip() == '---':
                separator_found = True
                continue
            if separator_found:
                content += line
            else:
                raw_metadata += line
    return dict(json.loads(raw_metadata), content=content)

def write_output(name: str, html: str) -> None:
    with open(os.path.join(OUTPUT_FOLDER, f'{name}.html'), 'w+') as f:
        f.write(html)

def get_jinja_env(folder_path: str) -> Environment:
    return Environment(loader=FileSystemLoader(f'{folder_path}/layout'), trim_blocks=True)

def generate_html(metadata: str, jinja_env: Environment) -> Union[str, None]:
    try:
        template_layout = metadata['layout']
    except KeyError:
        log.error('Missing layout, can not generate template without one!')
        return

    template = jinja_env.get_template(template_layout)
    log.info(f"Generating template from {template_layout} layout")
    return template.render(metadata)  

def create_html_file(file_path: str, html: str) -> None:
    name, extension = os.path.splitext(os.path.basename(file_path))
    write_output(name, html)

def generate_site(folder_path: str) -> None:
    log.info(f"Generating site from {folder_path}")
    jinja_env = get_jinja_env(folder_path)
    for file_path in list_files(folder_path):
        metadata = read_file(file_path)
        html = generate_html(metadata, jinja_env)
        if not html:
            continue        
        create_html_file(file_path, html)


def main():
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    generate_site(sys.argv[1])


if __name__ == '__main__':
    logging.basicConfig()
    main()
