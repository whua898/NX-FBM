import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge.xml')
objects = tree.getroot().find('Objects')

libs = [e for e in objects if e.tag == 'MachiningRuleLibrary']

with_decoration = 0
without_decoration = 0

for lib in libs:
    has_decoration = lib.find('DecorationObjects') is not None
    
    if has_decoration:
        with_decoration += 1
    else:
        without_decoration += 1

print(f"Total libraries: {len(libs)}")
print(f"With DecorationObjects: {with_decoration}")
print(f"Without DecorationObjects: {without_decoration}")

# 找一个有 DecorationObjects 的例子
if with_decoration > 0:
    for lib in libs:
        if lib.find('DecorationObjects') is not None:
            name = (lib.find('name').text if lib.find('name') is not None else 'N/A')[:40]
            print(f"\nExample with DecorationObjects: {name}")
            decoration = lib.find('DecorationObjects')
            print(f"  Content: {(decoration.text or '')[:100]}")
            break
