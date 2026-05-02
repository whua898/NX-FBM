import sys
import xml.etree.ElementTree as ET
import re

def parse_tools(dat_file):
    with open(dat_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    tools = []
    current_class = ""
    for line in lines:
        if line.startswith("#CLASS "):
            current_class = line.strip().split()[1]
        elif line.startswith("DATA   |"):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) > 15:
                libref = parts[1]
                # Filter out standard tools that don't look like our custom ones
                # We know our custom ones start with D, ZD, JD, DJD, ZXD
                if libref.startswith('D') or libref.startswith('ZD') or libref.startswith('JD') or libref.startswith('Z') or '_Insert' in libref:
                    dia = float(parts[14])
                    tools.append({
                        'libref': libref,
                        'tool_class': current_class,
                        'dia': dia
                    })
    return tools

def create_machining_rules(tools):
    rules = []
    
    # Organize tools
    
    end_mills = sorted([t for t in tools if t['tool_class'] in ['END_MILL_NON_INDEXABLE', 'END_MILL_INDEXABLE']], key=lambda x: x['dia'], reverse=True)
    ball_mills = sorted([t for t in tools if t['tool_class'] in ['BALL_MILL_NON_INDEXABLE', 'BALL_MILL_INDEXABLE']], key=lambda x: x['dia'], reverse=True)

    face_mills = sorted([t for t in tools if t['tool_class'] in ['FACE_MILL_INDEXABLE', 'FACE_MILL_NON_INDEXABLE']], key=lambda x: x['dia'], reverse=True)
    drills = sorted([t for t in tools if t['tool_class'] == 'TWIST_DRILL'], key=lambda x: x['dia'])
    reamers = sorted([t for t in tools if t['tool_class'] == 'CHUCKING_REAMER'], key=lambda x: x['dia'])
    chamfers = sorted([t for t in tools if t['tool_class'] in ['CHAMFER_MILL_NON_INDEXABLE', 'CHAMFER_MILL_INDEXABLE']], key=lambda x: x['dia'])
    spot_drills = sorted([t for t in tools if t['tool_class'] == 'SPOT_DRILL'], key=lambda x: x['dia'])
    
    # 01 Face Milling
    face_children = []
    priority = 1210
    for t in face_mills:
        dia = t['dia']
        libref = t['libref']
        face_children.append({
            'type': 'MachiningRule', 'name': f'1.1_Face_Top_Rough_{libref}', 'priority': str(priority),
            'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'SURFACE_PLANAR_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.LENGTH', '>', '0.0')],
            'tool_attrs': [('tool.Libref', '=', libref)]
        })
        priority += 1
        
    face_lib = {
        'type': 'MachiningRuleLibrary', 'name': '01_Face_Milling_Dynamic', 'external_id': 'Factory_NX2512_01_Face_Milling_Dynamic',
        'description': '动态面加工库', 'children': face_children
    }
    
    # 02 Pocket Slot
    pocket_children = []
    priority = 2410
    for t in end_mills:
        dia = t['dia']
        libref = t['libref']
        # Pocket rough
        pocket_children.append({
            'type': 'MachiningRule', 'name': f'2.1_Pocket_Rough_{libref}', 'priority': str(priority),
            'op_class': 'mill_contour.CAVITY_MILL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.WIDTH', '>=', str(round(dia + 1.0, 2)))],
            'tool_attrs': [('tool.Libref', '=', libref)]
        })
        # Slot rough
        pocket_children.append({
            'type': 'MachiningRule', 'name': f'2.7_Slot_Rough_{libref}', 'priority': str(priority + 100),
            'op_class': 'mill_planar.GROOVE_MILLING', 'mwf': 'SLOT_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.WIDTH', '>=', str(round(dia, 2)))],
            'tool_attrs': [('tool.Libref', '=', libref)]
        })
        priority += 1
        
    pocket_lib = {
        'type': 'MachiningRuleLibrary', 'name': '02_Pocket_Slot_Dynamic', 'external_id': 'Factory_NX2512_02_Pocket_Slot_Dynamic',
        'description': '动态型腔与槽加工库', 'children': pocket_children
    }
    
    # 03_Hole_Making
    hole_children = []
    
    # Spot Drills
    spot_children = []
    priority = 1110
    for t in spot_drills:
        libref = t['libref']
        spot_children.append({
            'type': 'MachiningRule', 'name': f'3.1_Spot_Drill_{libref}', 'priority': str(priority),
            'op_class': 'hole_making.SPOT_DRILLING', 'mwf': 'POCKET_ROUND_TAPERED', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', '2.0')],
            'tool_attrs': [('tool.Libref', '=', libref)]
        })
        priority += 1
    hole_children.append({
        'type': 'MachiningRuleLibrary', 'name': '3.1_Spot_Dynamic', 'external_id': 'Factory_NX2512_03_Hole_Spot_Dynamic',
        'children': spot_children
    })
    
    # Standard Drills
    std_drill_children = []
    priority = 2510
    for t in drills:
        dia = t['dia']
        libref = t['libref']
        
        # Through holes (STEP1HOLE)
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Thru_{libref}_From_Solid', 'priority': str(priority),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Thru_{libref}_After_Spot', 'priority': str(priority + 1),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE', 'lwf': 'POCKET_ROUND_TAPERED', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        
        # Blind holes (STEP1POCKET)
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Blind_{libref}_From_Solid', 'priority': str(priority + 2),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1POCKET', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Blind_{libref}_After_Spot', 'priority': str(priority + 3),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1POCKET', 'lwf': 'POCKET_ROUND_TAPERED', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        
        # Threaded holes (Thru and Blind)
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Thru_Thread_{libref}_From_Solid', 'priority': str(priority + 4),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE_THREAD', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Blind_Thread_{libref}_From_Solid', 'priority': str(priority + 5),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1POCKET_THREAD', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Thru_Thread_{libref}_After_Spot', 'priority': str(priority + 6),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE_THREAD', 'lwf': 'POCKET_ROUND_TAPERED', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        std_drill_children.append({
            'type': 'MachiningRule', 'name': f'3.5_Standard_Drill_Blind_Thread_{libref}_After_Spot', 'priority': str(priority + 7),
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1POCKET_THREAD', 'lwf': 'POCKET_ROUND_TAPERED', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', f'"{libref}"')]
        })
        priority += 8
        
    hole_children.append({
        'type': 'MachiningRuleLibrary', 'name': '3.5_Standard_Drill_Dynamic', 'external_id': 'Factory_NX2512_03_Hole_Std_Dynamic',
        'children': std_drill_children
    })
    
    # Reamers
    ream_children = []
    priority = 3110
    for t in reamers:
        dia = t['dia']
        libref = t['libref']
        ream_children.append({
            'type': 'MachiningRule', 'name': f'3.4_Pin_Ream_{libref}', 'priority': str(priority),
            'op_class': 'hole_making.BORING_REAMING', 'mwf': 'STEP2HOLE', 'lwf': 'STEP1HOLE', 'tool_class': t['tool_class'],
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(dia - 0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(dia + 0.05, 2)))],
            'tool_attrs': [('tool.Libref', '=', libref)]
        })
        priority += 1
    hole_children.append({
        'type': 'MachiningRuleLibrary', 'name': '3.4_Pin_Ream_Dynamic', 'external_id': 'Factory_NX2512_03_Hole_Ream_Dynamic',
        'children': ream_children
    })
    
    hole_lib = {
        'type': 'MachiningRuleLibrary', 'name': '03_Hole_Making_Dynamic', 'external_id': 'Factory_NX2512_03_Hole_Dynamic',
        'description': '动态孔加工库', 'children': hole_children
    }
    
    # 04_Chamfer
    chamfer_children = []
    priority = 3310
    hole_types = ['STEP1HOLE', 'STEP1POCKET', 'STEP1HOLE_THREAD', 'STEP1POCKET_THREAD']
    for t in chamfers:
        dia = t['dia']
        libref = t['libref']
        
        for h_type in hole_types:
            op_cls = 'hole_making.HOLE_CHAMFER_MILLING' if 'MILL' in t['tool_class'] else 'hole_making.COUNTERSINKING'
            chamfer_children.append({
                'type': 'MachiningRule', 'name': f'4.1_Hole_Chamfer_{h_type}_{libref}', 'priority': str(priority),
                'op_class': op_cls, 'mwf': h_type, 'lwf': h_type, 'tool_class': t['tool_class'],
                'criteria': [
                    ('mwf.DIAMETER_1', '>', '0.0'),
                    ('mwf.DEPTH_TOP_CHAMFER', '>', 'constant.Small_Value')
                ],
                'tool_attrs': [
                    ('tool.Libref', '=', f'"{libref}"'),
                    ('tool.Diameter', '>', 'mwf.DIAMETER_1 + 2*mwf.DEPTH_TOP_CHAMFER*TAN(mwf.ANGLE_TOP_CHAMFER)'),
                    ('tool.TipDiameter', '<=', 'mwf.DIAMETER_1')
                ],
                'lwf_attrs': [
                    ('lwf.DEPTH_TOP_CHAMFER', '=', '0'),
                    ('lwf.ANGLE_TOP_CHAMFER', '=', '0'),
                    ('lwf.RADIUS_TOP_CHAMFER', '=', '0'),
                    ('lwf.CHAMFER', '=', '"No_top"')
                ],
                'oper_attrs': [
                    ('oper.Geometry_Roles', '=', 'mwf.FACES_TOP_CHAMFER')
                ]
            })
            priority += 1
        
    chamfer_lib = {
        'type': 'MachiningRuleLibrary', 'name': '04_Chamfer_Dynamic', 'external_id': 'Factory_NX2512_04_Chamfer_Dynamic',
        'description': '动态倒角库', 'children': chamfer_children
    }
    
    
    # 05_3D_Profile
    profile_children = []
    priority = 4110
    for t in ball_mills:
        dia = t['dia']
        libref = t['libref']
        profile_children.append({
            'type': 'MachiningRule', 'name': f'5.1_Profile_3D_{libref}', 'priority': str(priority),
            'op_class': 'mill_contour.ZLEVEL_PROFILE', 'mwf': 'SURFACE_CONTOURED', 'lwf': 'BLANK', 'tool_class': t['tool_class'],
            'criteria': [('mwf.SMALLEST_CONCAVE_RADIUS', '>=', str(round(dia / 2, 2)))],
            'tool_attrs': [('tool.Libref', '=', libref)]
        })
        priority += 1
        
    profile_lib = {
        'type': 'MachiningRuleLibrary', 'name': '05_3D_Profile_Dynamic', 'external_id': 'Factory_NX2512_05_3D_Profile_Dynamic',
        'description': '动态曲面加工库 (球刀)', 'children': profile_children
    }
    
    rules.extend([face_lib, pocket_lib, hole_lib, chamfer_lib, profile_lib])
    return rules


def build_library_element(parent, lib_data, id_counter):
    lib = ET.SubElement(parent, 'MachiningRuleLibrary')
    if 'external_id' in lib_data:
        lib.set('ExternalId', lib_data['external_id'])
    
    node_info = ET.SubElement(lib, 'NodeInfo')
    ET.SubElement(node_info, 'Id').text = str(id_counter)
    id_counter += 1
    
    ET.SubElement(lib, 'ContentType').text = 'InferenceRule'
    ET.SubElement(lib, 'History')
    ET.SubElement(lib, 'Machines')
    ET.SubElement(lib, 'ProductMaterials')
    
    ET.SubElement(lib, 'name').text = lib_data['name']
    if 'description' in lib_data:
        ET.SubElement(lib, 'comment').text = lib_data['description']
    
    collections = ET.SubElement(lib, 'collections')
    if parent.tag == 'RuleRootLibrary':
        ET.SubElement(collections, 'item').text = parent.get('ExternalId')
    elif parent.tag == 'DummyRoot':
        ET.SubElement(collections, 'item').text = '1748121186'  # MillDrill
        
    children = ET.SubElement(lib, 'children')
    
    for child_data in lib_data.get('children', []):
        if child_data['type'] == 'MachiningRule':
            child_ext_id = f"{lib_data['external_id']}_{child_data['name']}"
            ET.SubElement(children, 'item').text = child_ext_id
            
            rule_elem = ET.SubElement(parent, 'MachiningRule')
            rule_elem.set('ExternalId', child_ext_id)
            
            node_info_r = ET.SubElement(rule_elem, 'NodeInfo')
            ET.SubElement(node_info_r, 'Id').text = str(id_counter)
            id_counter += 1

            ET.SubElement(rule_elem, 'name').text = child_data['name']

            collections_r = ET.SubElement(rule_elem, 'collections')
            ET.SubElement(collections_r, 'item').text = lib_data['external_id']
            
            # 添加工序必需的元数据标签
            ET.SubElement(rule_elem, 'Machines')
            ET.SubElement(rule_elem, 'ProductMaterials')
            ET.SubElement(rule_elem, 'History')
            ET.SubElement(rule_elem, 'DecorationObjects')
            
            conditions = ET.SubElement(rule_elem, 'Conditions')
            app_criteria = ["REM Application Criteria", ""]
            for field, op, value in child_data.get('criteria', []):
                app_criteria.append(f"{field} {op} {value}")
            app_criteria.append("")
            app_criteria.append("$$ Rule rejected because condition FALSE")
            app_criteria.append("")
            
            tool_attrs = ["REM Tool Attributes", ""]
            for field, op, value in child_data.get('tool_attrs', []):
                if field == 'tool.Libref' and not value.startswith('"'):
                    value = f'"{value}"'
                tool_attrs.append(f"{field} {op} {value}")
            tool_attrs.append("")
            
            lwf_attrs = ["REM Less Worked Feature Attributes", ""]
            for field, op, value in child_data.get('lwf_attrs', []):
                lwf_attrs.append(f"{field} {op} {value}")
            lwf_attrs.append("")
            
            oper_attrs = ["REM Operation Attributes", ""]
            oper_attrs.append(f'oper.name = "{child_data["name"]}"')
            
            if child_data.get('op_class', '') == 'mill_contour.CAVITY_MILL':
                oper_attrs.append('oper.Smart_Tool_Axis_Vector[1] = -mwf.X_ORIENTATION_D')
                oper_attrs.append('oper.Smart_Tool_Axis_Vector[2] = -mwf.Y_ORIENTATION_D')
                oper_attrs.append('oper.Smart_Tool_Axis_Vector[3] = -mwf.Z_ORIENTATION_D')
                
            if child_data.get('op_class', '').startswith('hole_making.'):
                if child_data.get('op_class', '') not in ['hole_making.HOLE_CHAMFER_MILLING', 'hole_making.COUNTERSINKING']:
                    oper_attrs.append('oper.Geometry_Roles = mwf.FACES_CYLINDER_1')

            for field, op, value in child_data.get('oper_attrs', []):
                oper_attrs.append(f"{field} {op} {value}")
                
            oper_attrs.append("")

            criteria_text = "\n".join(app_criteria + tool_attrs + lwf_attrs + oper_attrs)
            conditions.text = criteria_text
            
            inp = ET.SubElement(rule_elem, 'Input')
            ET.SubElement(inp, 'item').text = f"feature.{child_data['lwf']}"
            
            ET.SubElement(rule_elem, 'Machines')
            ET.SubElement(rule_elem, 'OperationClass').text = child_data['op_class']
            
            outp = ET.SubElement(rule_elem, 'Output')
            ET.SubElement(outp, 'item').text = f"feature.{child_data['mwf']}"
            
            ET.SubElement(rule_elem, 'ProductMaterials')
            ET.SubElement(rule_elem, 'Priority').text = child_data['priority']
            
            res = ET.SubElement(rule_elem, 'Resources')
            if child_data.get('tool_class'):
                ET.SubElement(res, 'item').text = f"tool.{child_data['tool_class']}"
            
            ET.SubElement(rule_elem, 'comment').text = child_data.get('description', '')
            ET.SubElement(rule_elem, 'type').text = "Composed"
            
        elif child_data['type'] == 'MachiningRuleLibrary':
            sub_lib, id_counter = build_library_element(parent, child_data, id_counter)
            child_ext_id = child_data['external_id']
            ET.SubElement(children, 'item').text = child_ext_id
            
            coll = sub_lib.find('collections')
            if coll is None:
                coll = ET.SubElement(sub_lib, 'collections')
            ET.SubElement(coll, 'item').text = lib_data['external_id']
            
    return lib, id_counter

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    input_file = 'machining_knowledge.xml'
    output_file = 'machining_knowledge_v3.xml'
    dat_file = 'tool_database_v24.dat'
    
    print(f"📖 读取刀具数据库: {dat_file}")
    tools = parse_tools(dat_file)
    print(f"找到 {len(tools)} 把符合我们命名的高潜自定义刀具")
    
    print(f"📖 读取基准文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()

    # 清除历史碎片
    target_children_close_old = "<item>Factory_Dynamic_Rules_Lib</item></children></RuleRootLibrary>"
    if target_children_close_old in xml_content:
        xml_content = xml_content.replace(target_children_close_old, "</children></RuleRootLibrary>")

    anchor_prefix = "<name>MillDrill</name><collections><item>OOTB_EnvironmentLibraryEnvRuleRoot</item></collections><children>"
    if f"{anchor_prefix}<item>Factory_Dynamic_Rules_Lib</item>" in xml_content:
        xml_content = xml_content.replace(f"{anchor_prefix}<item>Factory_Dynamic_Rules_Lib</item>", anchor_prefix)
    
    # 也清除 v12 的残留
    if f"{anchor_prefix}<item>Factory_Plate_NX2512_General_Lib</item>" in xml_content:
        xml_content = xml_content.replace(f"{anchor_prefix}<item>Factory_Plate_NX2512_General_Lib</item>", anchor_prefix)

    id_matches = re.findall(r'<Id>(\d+)</Id>', xml_content)
    max_id = max([int(x) for x in id_matches]) if id_matches else 2000000000
    next_id = max_id + 1

    root_dummy = ET.Element('DummyRoot')
    
    factory_lib = ET.SubElement(root_dummy, 'MachiningRuleLibrary')
    factory_lib.set('ExternalId', 'Factory_Dynamic_Rules_Lib')
    
    node_info = ET.SubElement(factory_lib, 'NodeInfo')
    ET.SubElement(node_info, 'Id').text = str(next_id)
    next_id += 1
    
    ET.SubElement(factory_lib, 'ContentType').text = 'InferenceRule'
    ET.SubElement(factory_lib, 'History')
    ET.SubElement(factory_lib, 'Machines')
    ET.SubElement(factory_lib, 'ProductMaterials')
    ET.SubElement(factory_lib, 'name').text = 'Factory_Dynamic_Rules_All'
    ET.SubElement(factory_lib, 'comment').text = '100% 映射自定义本地刀库的绝对规则！'
    
    collections = ET.SubElement(factory_lib, 'collections')
    ET.SubElement(collections, 'item').text = '1748121186'
    
    children = ET.SubElement(factory_lib, 'children')
    
    rules = create_machining_rules(tools)
    for rule_lib in rules:
        sub_lib, next_id = build_library_element(root_dummy, rule_lib, next_id)
        ET.SubElement(children, 'item').text = rule_lib['external_id']
        coll = sub_lib.find('collections')
        if coll is None:
            coll = ET.SubElement(sub_lib, 'collections')
        ET.SubElement(coll, 'item').text = 'Factory_Dynamic_Rules_Lib'

    injected_str = ""
    for child in root_dummy:
        injected_str += ET.tostring(child, encoding='unicode')

    print(f"🔧 注入自定义规则到官方核心库 MillDrill...")
    if anchor_prefix in xml_content:
        xml_content = xml_content.replace(anchor_prefix, f"{anchor_prefix}<item>Factory_Dynamic_Rules_Lib</item>")
    if "</Objects>" in xml_content:
        xml_content = xml_content.replace("</Objects>", injected_str + "</Objects>")
    else:
        last_rule_idx = xml_content.rfind('</MachiningRule>')
        if last_rule_idx != -1:
            xml_content = xml_content[:last_rule_idx + 16] + "\n" + injected_str + "\n</Objects>\n</Data>"
        else:
            xml_content = xml_content + "\n" + injected_str + "\n</Objects>\n</Data>"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(xml_content)
        
    print(f"✅ 成功生成 {output_file}，注入了所有专属自定义刀具的规则！")

if __name__ == '__main__':
    main()
