"""Build a Python script for a novxlib based application.
        
In order to distribute single scripts without dependencies, 
this script "inlines" all modules imported from the novxlib package.

- Discards docstrings and multiline strings in double quotes.
- Discards comment lines.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/novxlib
License: GNU LGPLv3 (https://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
import re
import os
from shutil import copyfile


def inline_module(file, package, packagePath, text, processedModules, copyNovxlib):
    with open(file, 'r', encoding='utf-8') as f:
        print(f'Processing "{file}"...')
        if copyNovxlib:
            target = file.replace('/../novxlib', '')
            targetDir = os.path.split(target)[0]
            os.makedirs(targetDir, exist_ok=True)
            if not os.path.isfile(target):
                copyfile(file, target)
        lines = f.readlines()
        inDocstring = False
        # document parsing always starts in the header
        for line in lines:
            if line.startswith('# do_not_inline'):
                break

            if line.count('"""') == 2:
                # Discard single-line docstring.
                continue

            if line.lstrip().startswith('#'):
                if not line.lstrip().startswith('#!'):
                    # Discard comment line, but keep the shebang.
                    continue

            if line.count('"""') == 1:
                # Beginning or end of a multi-line docstring
                if package in file:
                    # This is not the root script
                    # so discard the module's docstring
                    if inDocstring:
                        # docstring ends
                        inDocstring = False
                    else:
                        # docstring begins
                        inDocstring = True
                else:
                    text = f'{text}{line}'
            elif not inDocstring:
                if package in file:
                    if 'main()' in line:
                        return(text)
                    if '__main__' in line:
                        return(text)
                if 'import ' in line:
                    importModule = re.match(r'from (.+?) import.+', line)
                    if (importModule is not None) and (package in importModule.group(1)):
                        packageName = re.sub(r'\.', r'\/', importModule.group(1))
                        moduleName = f'{packagePath}{packageName}'
                        if not (moduleName in processedModules):
                            processedModules.append(moduleName)
                            text = inline_module(
                                f'{moduleName}.py', package, packagePath, text, processedModules, copyNovxlib)
                    elif line.lstrip().startswith('import'):
                        moduleName = line.replace('import ', '').rstrip()
                        if not (moduleName in processedModules):
                            processedModules.append(moduleName)
                            text = f'{text}{line}'
                    else:
                        text = f'{text}{line}'
                else:
                    text = f'{text}{line}'
        return(text)


def run(sourceFile, targetFile, package, packagePath, copynovxlib=False):
    text = ''
    processedModules = []
    text = inline_module(sourceFile, package, packagePath, text, processedModules, copynovxlib)
    with open(targetFile, 'w', encoding='utf-8', newline='\n') as f:
        print(f'Writing "{targetFile}"...\n')
        f.write(text)

