import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge_v2.xml')
objects = tree.getroot().find('Objects')

# 查找 Factory 库
factory_libs = [e for e in objects if e.tag == 'MachiningRuleLibrary' and 'Factory_Plate' in e.get('ExternalId', '')]

print(f"Factory libraries in v2: {len(factory_libs)}")
for lib in factory_libs[:3]:
    ext_id = lib.get('ExternalId', 'N/A')
    content_type = lib.find('ContentType')
    print(f"\n  {ext_id}:")
    print(f"    ContentType: {(content_type.text if content_type is not None else 'MISSING')}")
    print(f"    Machines: {'Present' if lib.find('Machines') is not None else 'MISSING'}")
    print(f"    ProductMaterials: {'Present' if lib.find('ProductMaterials') is not None else 'MISSING'}")
