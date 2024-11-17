"""Update test files."""
import sys

filePath = sys.argv[1]
with open(filePath, 'r', encoding='utf-8') as f:
    text = f.read()

old = '''
  <style:font-face style:name="Segoe UI" svg:font-family="&apos;Segoe UI&apos;" style:font-adornments="Standard" style:font-family-generic="swiss" style:font-pitch="variable"/>
'''

new = '''
  <style:font-face style:name="Calibri" svg:font-family="&apos;Calibri&apos;" style:font-adornments="Standard" style:font-family-generic="swiss" style:font-pitch="variable"/>
'''

if old in text:
    text = text.replace(old, new)
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(text)
