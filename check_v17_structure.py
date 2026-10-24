import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge_v17.xml')
objects = tree.getroot().find('Objects')

# 查找 MillDrill 库
milldrill = None
for elem in objects:
    if elem.get('ExternalId') == '1748121186':
        milldrill = elem
        break

if milldrill is not None:
    children = milldrill.find('children')
    if children is not None:
        items = children.findall('item')
        print(f"MillDrill children count: {len(items)}")
        print(f"First 5 children:")
        for i, item in enumerate(items[:5]):
            ext_id = item.text
            lib_elem = None
            for e in objects:
                if e.get('ExternalId') == ext_id:
                    lib_elem = e
                    break
            
            name = (lib_elem.find('name').text if lib_elem is not None and lib_elem.find('name') is not None else 'N/A')
            print(f"  {i+1}. {ext_id[:40]}... - {name}")
            
            if lib_elem is not None and 'Factory_Dynamic' in ext_id:
                print(f"     ContentType: {(lib_elem.find('ContentType').text if lib_elem.find('ContentType') is not None else 'MISSING')}")
                print(f"     Machines: {'Present' if lib_elem.find('Machines') is not None else 'MISSING'}")
                print(f"     ProductMaterials: {'Present' if lib_elem.find('ProductMaterials') is not None else 'MISSING'}")
                print(f"     History: {'Present' if lib_elem.find('History') is not None else 'MISSING'}")
