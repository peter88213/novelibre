import glob
import os
from shutil import copyfile

ROOT_DIR = '../..'
SOURCE_DIR = 'novelibre/.github/ISSUE_TEMPLATE'
FILES = [
    'config.yml',
]

os.chdir(ROOT_DIR)
for plugin in glob.iglob('nv_*', recursive=False):
    target_dir = f'{plugin}/.github/ISSUE_TEMPLATE'
    os.makedirs(target_dir, exist_ok=True)
    for file in FILES:
        source = os.path.join(SOURCE_DIR, file)
        target = os.path.join(target_dir, file)
        copyfile(source, target)
    print(plugin)
print('Done.')
