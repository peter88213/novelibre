"""Search the project's Python code for long lines.

Copyright (c) Peter Triesberger
For further information see https://github.com/peter88213/
Published under the MIT License 
(https://opensource.org/licenses/mit-license.php)
"""
import sys
import os

LINE_LENGTH_LIMIT = 80
RESULT_FILE = 'long_lines.txt'


def main(startDir):
    foundGlobal = []
    foundLocal = []
    for root, filePath, files in os.walk(startDir):
        for file in files:
            if file.endswith(".py"):
                module = os.path.join(root, file)
                print(module)
                found = False
                foundLocal = [f'\n{module}\n{"-" * len(module)}\n']
                with open(module, 'r', encoding='utf-8') as f:
                    lines = f.read().split('\n')
                for i, line in enumerate(lines):
                    if len(line) > LINE_LENGTH_LIMIT:
                        foundLocal.append(f'[{i + 1}]\t{line}')
                        found = True
                if found:
                    foundGlobal.extend(foundLocal)
    if foundGlobal:
        foundGlobal.append('')
        with open(RESULT_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(foundGlobal))
        print(f'"{RESULT_FILE}" writtten.')
    else:
        if os.path.isfile(RESULT_FILE):
            os.remove(RESULT_FILE)
        print('No long lines found.')


if __name__ == '__main__':
    try:
        startDir = sys.argv[1]
    except IndexError:
        startDir = '../../src'
    main(startDir)
