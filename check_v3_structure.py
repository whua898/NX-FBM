import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge_v3.xml')
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
        print(f"First child:")
        first_item = items[0]
        ext_id = first_item.text
        lib_elem = None
        for e in objects:
            if e.get('ExternalId') == ext_id:
                lib_elem = e
                break
        
        if lib_elem is not None:
            name = (lib_elem.find('name').text if lib_elem.find('name') is not None else 'N/A')
            print(f"  Name: {name}")
            print(f"  ContentType: {(lib_elem.find('ContentType').text if lib_elem.find('ContentType') is not None else 'MISSING')}")
            print(f"  Machines: {'Present' if lib_elem.find('Machines') is not None else 'MISSING'}")
            print(f"  ProductMaterials: {'Present' if lib_elem.find('ProductMaterials') is not None else 'MISSING'}")
            print(f"  History: {'Present' if lib_elem.find('History') is not None else 'MISSING'}")
            
            # 检查第一个子规则
            sub_children = lib_elem.find('children')
            if sub_children is not None and len(sub_children.findall('item')) > 0:
                first_rule_id = sub_children.find('item').text
                rule_elem = None
                for e in objects:
                    if e.get('ExternalId') == first_rule_id:
                        rule_elem = e
                        break
                
                if rule_elem is not None:
                    print(f"\n  First Rule ({first_rule_id[:40]}...):")
                    print(f"    Tag: {rule_elem.tag}")
                    print(f"    Machines: {'Present' if rule_elem.find('Machines') is not None else 'MISSING'}")
                    print(f"    ProductMaterials: {'Present' if rule_elem.find('ProductMaterials') is not None else 'MISSING'}")
                    print(f"    History: {'Present' if rule_elem.find('History') is not None else 'MISSING'}")
                    print(f"    DecorationObjects: {'Present' if rule_elem.find('DecorationObjects') is not None else 'MISSING'}")
