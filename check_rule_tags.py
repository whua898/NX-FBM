import xml.etree.ElementTree as ET

tree = ET.parse('machining_knowledge.xml')
objects = tree.getroot().find('Objects')

# 查找真正的 MachiningRule（不是 MachiningRuleLibrary）
rules = [e for e in objects if e.tag == 'MachiningRule']

print(f"Total MachiningRule count: {len(rules)}")

if len(rules) > 0:
    rule = rules[0]
    print(f"\nFirst MachiningRule:")
    print(f"  ExternalId: {rule.get('ExternalId', 'N/A')}")
    print(f"  Tag: {rule.tag}")
    
    # 检查所有子元素标签
    child_tags = [child.tag for child in rule]
    print(f"  Child tags: {child_tags}")
    
    # 检查 ContentType
    content_type = rule.find('ContentType')
    print(f"  ContentType: {(content_type.text if content_type is not None else 'MISSING')}")
    
    # 检查 Machines/ProductMaterials
    print(f"  Machines: {'Present' if rule.find('Machines') is not None else 'MISSING'}")
    print(f"  ProductMaterials: {'Present' if rule.find('ProductMaterials') is not None else 'MISSING'}")
    
    # 检查 Priority 类型
    priority_elem = rule.find('Priority')
    if priority_elem is not None:
        print(f"  Priority: {priority_elem.text} (type: {type(priority_elem.text).__name__})")
