import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge.xml')
objects = tree.getroot().find('Objects')

# 检查所有 MachiningRuleLibrary 是否有 History
libs = [e for e in objects if e.tag == 'MachiningRuleLibrary']

print(f"Total MachiningRuleLibrary count: {len(libs)}")

with_history = 0
without_history = 0

for lib in libs[:20]:  # 只检查前 20 个
    name = (lib.find('name').text if lib.find('name') is not None else 'N/A')[:40]
    has_history = lib.find('History') is not None
    has_decoration = lib.find('DecorationObjects') is not None
    
    if has_history:
        with_history += 1
    else:
        without_history += 1
        print(f"  ❌ {name}: No History, DecorationObjects={'Yes' if has_decoration else 'No'}")

print(f"\nWith History: {with_history}")
print(f"Without History: {without_history}")
