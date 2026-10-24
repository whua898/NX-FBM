import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge_v2.xml')
objects = tree.getroot().find('Objects')

# 检查 MillDrill 库
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
            # 查找对应的库名称
            lib_elem = None
            for e in objects:
                if e.get('ExternalId') == ext_id:
                    lib_elem = e
                    break
            
            name = (lib_elem.find('name').text if lib_elem is not None and lib_elem.find('name') is not None else 'N/A')
            print(f"  {i+1}. {ext_id[:40]}... - {name}")
            
            # 检查 Factory 库的结构
            if lib_elem is not None and 'Factory_Plate' in ext_id:
                print(f"     ContentType: {(lib_elem.find('ContentType').text if lib_elem.find('ContentType') is not None else 'MISSING')}")
                print(f"     Machines: {'Present' if lib_elem.find('Machines') is not None else 'MISSING'}")
                print(f"     ProductMaterials: {'Present' if lib_elem.find('ProductMaterials') is not None else 'MISSING'}")
                
                # 检查第一个子规则
                sub_children = lib_elem.find('children')
                if sub_children is not None:
                    first_rule_id = sub_children.find('item').text
                    rule_elem = None
                    for e in objects:
                        if e.get('ExternalId') == first_rule_id:
                            rule_elem = e
                            break
                    
                    if rule_elem is not None:
                        print(f"     First rule ({first_rule_id[:40]}...):")
                        print(f"       Tag: {rule_elem.tag}")
                        print(f"       Machines: {'Present' if rule_elem.find('Machines') is not None else 'MISSING'}")
                        print(f"       ProductMaterials: {'Present' if rule_elem.find('ProductMaterials') is not None else 'MISSING'}")
                        print(f"       History: {'Present' if rule_elem.find('History') is not None else 'MISSING'}")
                        print(f"       DecorationObjects: {'Present' if rule_elem.find('DecorationObjects') is not None else 'MISSING'}")
