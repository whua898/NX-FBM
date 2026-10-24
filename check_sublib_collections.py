import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge.xml')
objects = tree.getroot().find('Objects')

# 查找 MillDrill 的第一个子库
milldrill = None
for elem in objects:
    if elem.get('ExternalId') == '1748121186':
        milldrill = elem
        break

if milldrill is not None:
    children = milldrill.find('children')
    if children is not None:
        first_child_id = children.find('item').text
        print(f"First child ID: {first_child_id}")
        
        # 查找该子库
        first_child = None
        for elem in objects:
            if elem.get('ExternalId') == first_child_id:
                first_child = elem
                break
        
        if first_child is not None:
            print(f"Child name: {(first_child.find('name').text if first_child.find('name') is not None else 'N/A')}")
            
            # 检查 collections
            coll = first_child.find('collections')
            if coll is not None:
                items = coll.findall('item')
                print(f"Collections items ({len(items)}):")
                for item in items:
                    print(f"  - {item.text}")
            
            # 检查是否有 History/DecorationObjects
            print(f"History: {'Present' if first_child.find('History') is not None else 'MISSING'}")
            print(f"DecorationObjects: {'Present' if first_child.find('DecorationObjects') is not None else 'MISSING'}")
