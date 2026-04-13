"""Refactor the API version info handling for all plugin directories.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/novelibre
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import glob
import os
import re

ROOT_DIR = '../..'

requirementRegex = re.compile(r'\(https\:\/\/github\.com\/peter88213\/novelibre\/\) version .*?\+')
newLine = '(https://github.com/peter88213/novelibre/) version $ApiVersion+'


def refactor_readme(plugin):
    readmeFile = f'{plugin}/docs/template/README.md'
    if os.path.isfile(readmeFile):
        with open(readmeFile, 'r', encoding='utf-8') as f:
            text = f.read()
            text = requirementRegex.sub(newLine, text)
        print(plugin)
        with open(readmeFile, 'w', encoding='utf-8') as f:
            f.write(text)


def get_api_version(plugin):
    srcFile = f'{plugin}/src/{plugin}.py'
    with open(srcFile, 'r', encoding='utf-8') as f:
        text = f.read()
    apiVersion = re.search(r"API_VERSION = '(.*?)'", text).group(1)
    return apiVersion


os.chdir(ROOT_DIR)
for plugin in glob.iglob('nv_*', recursive=False):
    # refactor_readme(plugin)
    print(plugin, get_api_version(plugin))
print('Done.')
