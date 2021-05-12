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

def write_output(name: str, html: str, output_folder: str) -> None:
    with open(os.path.join(output_folder, f'{name}.html'), 'w+') as f:
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

def create_html_file(file_path: str, html: str, output_folder) -> None:
    name, extension = os.path.splitext(os.path.basename(file_path))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    write_output(name, html, output_folder)

def generate_site(folder_path: str, output_folder: str) -> None:
    log.info(f"Generating site from {folder_path}")
    jinja_env = get_jinja_env(folder_path)
    for file_path in list_files(folder_path):
        metadata = read_file(file_path)
        html = generate_html(metadata, jinja_env)
        if not html:
            continue        
        create_html_file(file_path, html, output_folder)


def main():
    if len(sys.argv) < 2:
        raise Exception('Need at least 2 arguments')
    output_folder = sys.argv[2]
    generate_site(sys.argv[1], output_folder)


if __name__ == '__main__':
    logging.basicConfig()
    main()
