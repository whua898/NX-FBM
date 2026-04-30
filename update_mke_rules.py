import xml.etree.ElementTree as ET
import os
import re

def create_machining_rules():
    rules = []
    
    # 01_Face_Milling
    face_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '01_Face_Milling',
        'external_id': 'Factory_Plate_NX2512_01_Face_Milling',
        'description': '面加工库 (NX2512)',
        'children': [
            {
                'type': 'MachiningRule', 'name': '1.1_Face_Top_Rough_D80', 'priority': '1210',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'SURFACE_PLANAR_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'FACE_MILL_INDEXABLE',
                'criteria': [('mwf.LENGTH', '>', '200.0')],
                'tool_attrs': [('tool.Diameter', '>=', '78.0'), ('tool.Diameter', '<=', '82.0')]
            },
            {
                'type': 'MachiningRule', 'name': '1.2_Face_Top_Rough_D63', 'priority': '1220',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'SURFACE_PLANAR_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'FACE_MILL_INDEXABLE',
                'criteria': [('mwf.LENGTH', '<=', '200.0')],
                'tool_attrs': [('tool.Diameter', '>=', '60.0'), ('tool.Diameter', '<=', '65.0')]
            },
            {
                'type': 'MachiningRule', 'name': '1.3_Face_Bottom_Finish_D63', 'priority': '1230',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'SURFACE_PLANAR_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'FACE_MILL_INDEXABLE',
                'criteria': [('mwf.LENGTH', '>', '150.0')],
                'tool_attrs': [('tool.Diameter', '>=', '60.0'), ('tool.Diameter', '<=', '65.0')]
            },
            {
                'type': 'MachiningRule', 'name': '1.4_Face_Bottom_Finish_D40', 'priority': '1240',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'SURFACE_PLANAR_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'FACE_MILL_INDEXABLE',
                'criteria': [('mwf.LENGTH', '<=', '150.0')],
                'tool_attrs': [('tool.Diameter', '>=', '38.0'), ('tool.Diameter', '<=', '42.0')]
            }
        ]
    }
    
    # 02_Pocket_Slot
    pocket_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '02_Pocket_Slot',
        'external_id': 'Factory_Plate_NX2512_02_Pocket_Slot',
        'description': '型腔与槽库 (NX2512)',
        'children': [
            {
                'type': 'MachiningRule', 'name': '2.1_Pocket_Rough_D20', 'priority': '2410',
                'op_class': 'mill_contour.CAVITY_MILL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.DEPTH', '>=', '15.0'), ('mwf.DEPTH', '<=', '50.0')],
                'tool_attrs': [('tool.Diameter', '>=', '18.0'), ('tool.Diameter', '<=', '22.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.2_Pocket_Rough_D12', 'priority': '2420',
                'op_class': 'mill_contour.CAVITY_MILL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.DEPTH', '>=', '5.0'), ('mwf.DEPTH', '<', '15.0')],
                'tool_attrs': [('tool.Diameter', '>=', '10.0'), ('tool.Diameter', '<=', '14.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.3_Pocket_Rough_D8', 'priority': '2430',
                'op_class': 'mill_contour.CAVITY_MILL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.DEPTH', '>=', '1.0'), ('mwf.DEPTH', '<', '5.0')],
                'tool_attrs': [('tool.Diameter', '>=', '6.0'), ('tool.Diameter', '<=', '9.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.4_Pocket_Finish_Wall_D12', 'priority': '2440',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.CORNER_RADIUS', '>=', '6.0')],
                'tool_attrs': [('tool.Diameter', '>=', '10.0'), ('tool.Diameter', '<=', '14.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.5_Pocket_Finish_Floor_D12', 'priority': '2450',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.CORNER_RADIUS', '>=', '6.0')],
                'tool_attrs': [('tool.Diameter', '>=', '10.0'), ('tool.Diameter', '<=', '14.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.6_Pocket_Finish_Wall_D8', 'priority': '2452',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.CORNER_RADIUS', '<', '6.0'), ('mwf.CORNER_RADIUS', '>=', '4.0')],
                'tool_attrs': [('tool.Diameter', '>=', '6.0'), ('tool.Diameter', '<=', '9.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.7_Pocket_Finish_Floor_D8', 'priority': '2454',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.CORNER_RADIUS', '<', '6.0'), ('mwf.CORNER_RADIUS', '>=', '4.0')],
                'tool_attrs': [('tool.Diameter', '>=', '6.0'), ('tool.Diameter', '<=', '9.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.8_Slot_Rough_D12', 'priority': '2460',
                'op_class': 'mill_planar.GROOVE_MILLING', 'mwf': 'SLOT_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.WIDTH', '>=', '14.0')],
                'tool_attrs': [('tool.Diameter', '>=', '10.0'), ('tool.Diameter', '<=', '14.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.9_Slot_Rough_D8', 'priority': '2470',
                'op_class': 'mill_planar.GROOVE_MILLING', 'mwf': 'SLOT_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.WIDTH', '<', '14.0'), ('mwf.WIDTH', '>=', '9.0')],
                'tool_attrs': [('tool.Diameter', '>=', '6.0'), ('tool.Diameter', '<=', '9.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.10_Slot_Finish_D8', 'priority': '2480',
                'op_class': 'mill_planar.GROOVE_MILLING', 'mwf': 'SLOT_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.WIDTH', '<', '14.0')],
                'tool_attrs': [('tool.Diameter', '>=', '6.0'), ('tool.Diameter', '<=', '9.0')]
            },
            {
                'type': 'MachiningRule', 'name': '2.11_Corner_Rest_Mill_D4', 'priority': '2490',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.CORNER_RADIUS', '<', '4.0')],
                'tool_attrs': [('tool.Diameter', '>=', '3.0'), ('tool.Diameter', '<=', '5.0')]
            }
        ]
    }
    
    # 03_Hole_Making (Fully Upgraded to hole_making module)
    hole_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '03_Hole_Making_NX2512',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making',
        'description': '新版孔加工库 (NX2512 hole_making)',
        'children': []
    }
    
    # 3.1 Spot
    spot_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.1_Spot',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Spot',
        'description': '定位钻',
        'children': [
            {
                'type': 'MachiningRule', 'name': '3.1_Spot_D10', 'priority': '1100',
                'op_class': 'hole_making.SPOT_DRILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'CENTER_DRILL',
                'criteria': [('mwf.DIAMETER_1', '>=', '3.0'), ('mwf.DIAMETER_1', '<=', '22.0')],
                'tool_attrs': [('tool.Diameter', '=', '10.0')]
            }
        ]
    }
    hole_lib['children'].append(spot_lib)
    
    # 3.2 Thread Bottom
    thread_bottom_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.2_Thread_Bottom',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_ThreadBottom',
        'description': '螺纹底孔',
        'children': []
    }
    thread_bottoms = [
        ("3.2_Thread_Bottom_D3p4", "2210", 3.4, 3.10, 3.50),
        ("3.2_Thread_Bottom_D4p3", "2220", 4.3, 4.10, 4.50),
        ("3.2_Thread_Bottom_D5p2", "2230", 5.2, 5.10, 5.50),
        ("3.2_Thread_Bottom_D6p9", "2240", 6.9, 6.50, 6.98),
        ("3.2_Thread_Bottom_D8p7", "2250", 8.7, 8.10, 8.98),
        ("3.2_Thread_Bottom_D10p5", "2260", 10.5, 10.10, 10.80),
        ("3.2_Thread_Bottom_D14p3", "2270", 14.3, 13.50, 14.50),
        ("3.2_Thread_Bottom_D17p8", "2280", 17.8, 17.10, 17.98),
    ]
    for name, priority, d, d_min, d_max in thread_bottoms:
        thread_bottom_lib['children'].append({
            'type': 'MachiningRule', 'name': name, 'priority': priority,
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'TWIST_DRILL',
            'criteria': [('mwf.DIAMETER_1', '>=', str(d_min)), ('mwf.DIAMETER_1', '<=', str(d_max))],
            'tool_attrs': [('tool.Diameter', '>=', str(round(d-0.05, 2))), ('tool.Diameter', '<=', str(round(d+0.05, 2)))]
        })
    hole_lib['children'].append(thread_bottom_lib)
    
    # 3.2.1 Tapping (New optimized threading ops)
    tapping_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.2.1_Tapping',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Tapping',
        'description': '攻丝加工',
        'children': []
    }
    tappings = [
        ("3.2.1_Tapping_M4", "2215", 4.0, 3.10, 3.50),
        ("3.2.1_Tapping_M5", "2225", 5.0, 4.10, 4.50),
        ("3.2.1_Tapping_M6", "2235", 6.0, 5.10, 5.50),
        ("3.2.1_Tapping_M8", "2245", 8.0, 6.50, 6.98),
        ("3.2.1_Tapping_M10", "2255", 10.0, 8.10, 8.98),
    ]
    for name, priority, tap_d, d_min, d_max in tappings:
        tapping_lib['children'].append({
            'type': 'MachiningRule', 'name': name, 'priority': priority,
            'op_class': 'hole_making.TAPPING', 'mwf': 'STEP1HOLE_THREAD', 'lwf': 'STEP1HOLE', 'tool_class': 'TAP',
            'criteria': [('mwf.DIAMETER_1', '>=', str(d_min)), ('mwf.DIAMETER_1', '<=', str(d_max))],
            'tool_attrs': [('tool.Diameter', '>=', str(round(tap_d-0.05, 2))), ('tool.Diameter', '<=', str(round(tap_d+0.05, 2)))]
        })
    hole_lib['children'].append(tapping_lib)
    
    # 3.3 Thread Through
    thread_through_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.3_Thread_Through',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_ThreadThrough',
        'description': '螺纹过孔',
        'children': []
    }
    thread_throughs = [
        ("3.3_Thread_Through_D9", "2310", 9.0, 8.98, 9.02),
        ("3.3_Thread_Through_D11", "2320", 11.0, 10.98, 11.02),
        ("3.3_Thread_Through_D13", "2330", 13.0, 12.98, 13.02),
        ("3.3_Thread_Through_D17", "2340", 17.0, 16.98, 17.02),
        ("3.3_Thread_Through_D21", "2350", 21.0, 20.98, 21.02),
    ]
    for name, priority, d, d_min, d_max in thread_throughs:
        thread_through_lib['children'].append({
            'type': 'MachiningRule', 'name': name, 'priority': priority,
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'TWIST_DRILL',
            'criteria': [('mwf.DIAMETER_1', '>=', str(d_min)), ('mwf.DIAMETER_1', '<=', str(d_max))],
            'tool_attrs': [('tool.Diameter', '>=', str(round(d-0.05, 2))), ('tool.Diameter', '<=', str(round(d+0.05, 2)))]
        })
    hole_lib['children'].append(thread_through_lib)
    
    # 3.4 Pin Hole
    pin_hole_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.4_Pin_Hole',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Pin',
        'description': '销孔',
        'children': []
    }
    
    pre_drill_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.4_Pin_Pre',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Pin_Pre',
        'description': '预钻孔',
        'children': []
    }
    pin_pres = [
        ("3.4_Pin_Pre_D4", "2110", 3.7, 3.68, 3.72),
        ("3.4_Pin_Pre_D5", "2120", 4.7, 4.68, 4.72),
        ("3.4_Pin_Pre_D6", "2130", 5.7, 5.68, 5.72),
        ("3.4_Pin_Pre_D8", "2140", 7.7, 7.68, 7.72),
        ("3.4_Pin_Pre_D10", "2150", 9.7, 9.68, 9.72),
        ("3.4_Pin_Pre_D12", "2160", 11.7, 11.68, 11.72),
        ("3.4_Pin_Pre_D16", "2170", 15.7, 15.68, 15.72),
        ("3.4_Pin_Pre_D20", "2180", 19.7, 19.68, 19.72),
    ]
    for name, priority, d, d_min, d_max in pin_pres:
        pre_drill_lib['children'].append({
            'type': 'MachiningRule', 'name': name, 'priority': priority,
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'TWIST_DRILL',
            'criteria': [('mwf.DIAMETER_1', '>=', str(d_min)), ('mwf.DIAMETER_1', '<=', str(d_max))],
            'tool_attrs': [('tool.Diameter', '>=', str(round(d-0.05, 2))), ('tool.Diameter', '<=', str(round(d+0.05, 2)))]
        })
    pin_hole_lib['children'].append(pre_drill_lib)
    
    ream_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.4_Pin_Ream',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Pin_Ream',
        'description': '铰孔',
        'children': []
    }
    pin_reams = [
        ("3.4_Pin_Ream_D4", "3110", 4.0, 3.98, 4.02),
        ("3.4_Pin_Ream_D5", "3120", 5.0, 4.98, 5.02),
        ("3.4_Pin_Ream_D6", "3130", 6.0, 5.98, 6.02),
        ("3.4_Pin_Ream_D8", "3140", 8.0, 7.98, 8.02),
        ("3.4_Pin_Ream_D10", "3150", 10.0, 9.98, 10.02),
        ("3.4_Pin_Ream_D12", "3160", 12.0, 11.98, 12.02),
        ("3.4_Pin_Ream_D16", "3170", 16.0, 15.98, 16.02),
        ("3.4_Pin_Ream_D20", "3180", 20.0, 19.98, 20.02),
    ]
    for name, priority, d, d_min, d_max in pin_reams:
        ream_lib['children'].append({
            'type': 'MachiningRule', 'name': name, 'priority': priority,
            'op_class': 'hole_making.BORING_REAMING', 'mwf': 'STEP2HOLE', 'lwf': 'STEP1HOLE', 'tool_class': 'CHUCKING_REAMER',
            'criteria': [('mwf.DIAMETER_1', '>=', str(d_min)), ('mwf.DIAMETER_1', '<=', str(d_max))],
            'tool_attrs': [('tool.Diameter', '>=', str(round(d-0.05, 2))), ('tool.Diameter', '<=', str(round(d+0.05, 2)))]
        })
    pin_hole_lib['children'].append(ream_lib)
    
    hole_lib['children'].append(pin_hole_lib)

    # 3.5 Standard Drill (General Drilling for uncategorized holes)
    std_drill_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.5_Standard_Drill',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Standard_Drill',
        'description': '标准直钻孔 (默认兜底)',
        'children': []
    }
    std_drills = [
        ("3.5_Standard_Drill_D3", "2510", 3.0),
        ("3.5_Standard_Drill_D4", "2520", 4.0),
        ("3.5_Standard_Drill_D5", "2530", 5.0),
        ("3.5_Standard_Drill_D6", "2540", 6.0),
        ("3.5_Standard_Drill_D8", "2550", 8.0),
        ("3.5_Standard_Drill_D10", "2560", 10.0),
        ("3.5_Standard_Drill_D12", "2570", 12.0),
        ("3.5_Standard_Drill_D14", "2580", 14.0),
    ]
    for name, priority, d in std_drills:
        std_drill_lib['children'].append({
            'type': 'MachiningRule', 'name': name, 'priority': priority,
            'op_class': 'hole_making.DRILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'TWIST_DRILL',
            'criteria': [('mwf.DIAMETER_1', '>=', str(round(d-0.05, 2))), ('mwf.DIAMETER_1', '<=', str(round(d+0.05, 2)))],
            'tool_attrs': [('tool.Diameter', '>=', str(round(d-0.05, 2))), ('tool.Diameter', '<=', str(round(d+0.05, 2)))]
        })
    hole_lib['children'].append(std_drill_lib)
    
    # 3.6 Large Hole
    large_hole_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.6_Large_Hole',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Large_Hole',
        'description': '大孔直铣',
        'children': [
            {
                'type': 'MachiningRule', 'name': '3.6_Large_Hole_Mill', 'priority': '3210',
                'op_class': 'hole_making.HOLE_MILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'END_MILL_NON_INDEXABLE',
                'criteria': [('mwf.DIAMETER_1', '>', '21.0'), ('mwf.DIAMETER_1', '<=', '200.0')],
                'tool_attrs': [('tool.Diameter', '>=', '10.0'), ('tool.Diameter', '<=', '20.0')]
            }
        ]
    }
    hole_lib['children'].append(large_hole_lib)
    
    # 3.7 Counter Bore
    counter_bore_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.7_Counter_Bore',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Counter_Bore',
        'description': '沉头孔加工',
        'children': []
    }
    counter_bores = [
        ("3.7_CB_M4", "2610", 8.0),
        ("3.7_CB_M5", "2620", 10.0),
        ("3.7_CB_M6", "2630", 11.0),
        ("3.7_CB_M8", "2640", 15.0),
        ("3.7_CB_M10", "2650", 18.0),
        ("3.7_CB_M12", "2660", 20.0),
    ]
    for name, priority, d_cb in counter_bores:
        counter_bore_lib['children'].append({
            'type': 'MachiningRule', 'name': name, 'priority': priority,
            'op_class': 'hole_making.HOLE_MILLING', 'mwf': 'STEP2HOLE', 'lwf': 'STEP1HOLE', 'tool_class': 'END_MILL_NON_INDEXABLE',
            'criteria': [('mwf.DIAMETER_1', '>=', str(d_cb-0.5)), ('mwf.DIAMETER_1', '<=', str(d_cb+0.5))],
            'tool_attrs': [('tool.Diameter', '>=', str(max(4.0, d_cb/2.0-1.0))), ('tool.Diameter', '<=', str(d_cb-1.0))]
        })
    hole_lib['children'].append(counter_bore_lib)

    # 3.8 Counter Sink
    counter_sink_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '3.8_Counter_Sink',
        'external_id': 'Factory_Plate_NX2512_03_Hole_Making_Counter_Sink',
        'description': '锥头孔(倒角)加工',
        'children': [
            {
                'type': 'MachiningRule', 'name': '3.8_CS_General_D12', 'priority': '2710',
                'op_class': 'hole_making.COUNTERSINKING', 'mwf': 'COUNTER_SUNK_HOLE', 'lwf': 'STEP1HOLE', 'tool_class': 'COUNTERSINK',
                'criteria': [('mwf.DIAMETER_1', '<=', '12.0')],
                'tool_attrs': [('tool.Diameter', '>=', '10.0'), ('tool.Diameter', '<=', '14.0')]
            },
            {
                'type': 'MachiningRule', 'name': '3.8_CS_General_D20', 'priority': '2720',
                'op_class': 'hole_making.COUNTERSINKING', 'mwf': 'COUNTER_SUNK_HOLE', 'lwf': 'STEP1HOLE', 'tool_class': 'COUNTERSINK',
                'criteria': [('mwf.DIAMETER_1', '>', '12.0'), ('mwf.DIAMETER_1', '<=', '20.0')],
                'tool_attrs': [('tool.Diameter', '>=', '18.0'), ('tool.Diameter', '<=', '22.0')]
            }
        ]
    }
    hole_lib['children'].append(counter_sink_lib)
    
    # 04_Chamfer
    chamfer_lib = {
        'type': 'MachiningRuleLibrary',
        'name': '04_Chamfer',
        'external_id': 'Factory_Plate_NX2512_04_Chamfer',
        'description': '倒角库 (NX2512)',
        'children': [
            {
                'type': 'MachiningRule', 'name': '4.1_Hole_Chamfer_D12', 'priority': '3310',
                'op_class': 'hole_making.HOLE_CHAMFER_MILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'CHAMFER_MILL_NON_INDEXABLE',
                'criteria': [('mwf.DIAMETER_1', '>=', '8.0'), ('mwf.DIAMETER_1', '<=', '30.0')],
                'tool_attrs': [('tool.Diameter', '>=', '10.0'), ('tool.Diameter', '<=', '14.0')]
            },
            {
                'type': 'MachiningRule', 'name': '4.2_Hole_Chamfer_D6', 'priority': '3320',
                'op_class': 'hole_making.HOLE_CHAMFER_MILLING', 'mwf': 'STEP1HOLE', 'lwf': 'BLANK', 'tool_class': 'CHAMFER_MILL_NON_INDEXABLE',
                'criteria': [('mwf.DIAMETER_1', '>=', '2.0'), ('mwf.DIAMETER_1', '<', '8.0')],
                'tool_attrs': [('tool.Diameter', '>=', '5.0'), ('tool.Diameter', '<=', '7.0')]
            },
            {
                'type': 'MachiningRule', 'name': '4.3_Pocket_Chamfer_D10', 'priority': '3330',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'POCKET_RECTANGULAR_STRAIGHT', 'lwf': 'BLANK', 'tool_class': 'CHAMFER_MILL_NON_INDEXABLE',
                'criteria': [],
                'tool_attrs': [('tool.Diameter', '>=', '9.0'), ('tool.Diameter', '<=', '11.0')]
            },
            {
                'type': 'MachiningRule', 'name': '4.4_Slot_Chamfer_D8', 'priority': '3340',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'SLOT_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'CHAMFER_MILL_NON_INDEXABLE',
                'criteria': [],
                'tool_attrs': [('tool.Diameter', '>=', '7.0'), ('tool.Diameter', '<=', '9.0')]
            },
            {
                'type': 'MachiningRule', 'name': '4.5_Outer_Chamfer_General', 'priority': '3350',
                'op_class': 'mill_planar.FLOOR_WALL', 'mwf': 'SURFACE_PLANAR_RECTANGULAR', 'lwf': 'BLANK', 'tool_class': 'CHAMFER_MILL_NON_INDEXABLE',
                'criteria': [],
                'tool_attrs': [('tool.Diameter', '>=', '8.0'), ('tool.Diameter', '<=', '25.0')]
            }
        ]
    }
    
    rules.extend([face_lib, pocket_lib, hole_lib, chamfer_lib])
    return rules

def erase_corrupted_nodes(objects, rule_root):
    elems_to_remove = []
    ids_to_remove = set()
    
    for elem in objects:
        ext_id = elem.get('ExternalId', '')
        if re.search(r'\d{2}-\d{2}-2026', ext_id) or 'Factory_Plate' in ext_id:
            elems_to_remove.append(elem)
            ids_to_remove.add(ext_id)
            
    children_elem = rule_root.find('children')
    if children_elem is not None:
        to_del = []
        for item in children_elem.findall('item'):
            if item.text in ids_to_remove or item.text == 'Factory_Plate_NX2512_General_Lib':
                to_del.append(item)
        for item in to_del:
            children_elem.remove(item)
            
    for elem in elems_to_remove:
        objects.remove(elem)
        
    print(f"Removed {len(elems_to_remove)} dirty/corrupt nodes.")

def build_library_element(parent, lib_data, objects_elem, id_counter):
    lib = ET.SubElement(parent, 'MachiningRuleLibrary')
    if 'external_id' in lib_data:
        lib.set('ExternalId', lib_data['external_id'])
    
    node_info = ET.SubElement(lib, 'NodeInfo')
    ET.SubElement(node_info, 'Id').text = str(id_counter)
    id_counter += 1
    
    ET.SubElement(lib, 'name').text = lib_data['name']
    if 'description' in lib_data:
        ET.SubElement(lib, 'comment').text = lib_data['description']
    
    collections = ET.SubElement(lib, 'collections')
    if parent.tag == 'RuleRootLibrary':
        ET.SubElement(collections, 'item').text = parent.get('ExternalId')
    
    children = ET.SubElement(lib, 'children')
    
    for child_data in lib_data.get('children', []):
        if child_data['type'] == 'MachiningRule':
            child_ext_id = f"{lib_data['external_id']}_{child_data['name']}"
            ET.SubElement(children, 'item').text = child_ext_id
            
            rule_elem = ET.SubElement(objects_elem, 'MachiningRule')
            rule_elem.set('ExternalId', child_ext_id)
            
            node_info_r = ET.SubElement(rule_elem, 'NodeInfo')
            ET.SubElement(node_info_r, 'Id').text = str(id_counter)
            id_counter += 1

            ET.SubElement(rule_elem, 'name').text = child_data['name']

            collections_r = ET.SubElement(rule_elem, 'collections')
            ET.SubElement(collections_r, 'item').text = lib_data['external_id']
            
            conditions = ET.SubElement(rule_elem, 'Conditions')
            criteria_text = "REM Application Criteria\n\n"
            for field, op, value in child_data['criteria']:
                criteria_text += f"{field} {op} {value}\n"
            criteria_text += "\n$$ Rule rejected because condition FALSE\n\n"
            
            criteria_text += "REM Tool Attributes\n\n"
            for field, op, value in child_data.get('tool_attrs', []):
                criteria_text += f"{field} {op} {value}\n"
            
            criteria_text += "\nREM Less Worked Feature Attributes\n\n"
            
            criteria_text += f'REM Operation Attributes\n\noper.name = "{child_data["name"]}"\n'
            conditions.text = criteria_text
            
            inp = ET.SubElement(rule_elem, 'Input')
            ET.SubElement(inp, 'item').text = f"feature.{child_data['lwf']}"
            
            ET.SubElement(rule_elem, 'OperationClass').text = child_data['op_class']
            
            outp = ET.SubElement(rule_elem, 'Output')
            ET.SubElement(outp, 'item').text = f"feature.{child_data['mwf']}"
            
            ET.SubElement(rule_elem, 'Priority').text = child_data['priority']
            
            res = ET.SubElement(rule_elem, 'Resources')
            if child_data['tool_class']:
                ET.SubElement(res, 'item').text = f"tool.{child_data['tool_class']}"
            
            ET.SubElement(rule_elem, 'comment').text = child_data.get('description', '')
            ET.SubElement(rule_elem, 'type').text = "Composed"
            
        elif child_data['type'] == 'MachiningRuleLibrary':
            sub_lib, id_counter = build_library_element(objects_elem, child_data, objects_elem, id_counter)
            child_ext_id = child_data['external_id']
            ET.SubElement(children, 'item').text = child_ext_id
            
            coll = sub_lib.find('collections')
            if coll is None:
                coll = ET.SubElement(sub_lib, 'collections')
            ET.SubElement(coll, 'item').text = lib_data['external_id']
    
    return lib, id_counter

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    input_file = 'machining_knowledge.xml'
    output_file = 'machining_knowledge.xml'
    
    print(f"📖 读取基准文件: {input_file}")
    tree = ET.parse(input_file)
    root = tree.getroot()
    objects = root.find('Objects')
    
    rule_root = None
    for elem in objects:
        if elem.tag == 'RuleRootLibrary' and elem.get('ExternalId') == 'OOTB_EnvironmentLibraryEnvRuleRoot':
            rule_root = elem
            break
            
    erase_corrupted_nodes(objects, rule_root)
    
    max_id = 0
    for elem in objects.iter('Id'):
        try:
            id_val = int(elem.text)
            if id_val > max_id:
                max_id = id_val
        except:
            pass
    next_id = max_id + 1
    
    rules = create_machining_rules()
    
    factory_lib = ET.SubElement(objects, 'MachiningRuleLibrary')
    factory_lib.set('ExternalId', 'Factory_Plate_NX2512_General_Lib')
    
    node_info = ET.SubElement(factory_lib, 'NodeInfo')
    ET.SubElement(node_info, 'Id').text = str(next_id)
    next_id += 1
    
    ET.SubElement(factory_lib, 'name').text = 'Factory_Plate_NX2512_General'
    ET.SubElement(factory_lib, 'comment').text = '板类零件 NX2512 自动化升级加工规则库'
    
    collections = ET.SubElement(factory_lib, 'collections')
    ET.SubElement(collections, 'item').text = 'OOTB_EnvironmentLibraryEnvRuleRoot'
    
    children_elem = rule_root.find('children')
    if children_elem is None:
        children_elem = ET.SubElement(rule_root, 'children')
    ET.SubElement(children_elem, 'item').text = 'Factory_Plate_NX2512_General_Lib'
    
    children = ET.SubElement(factory_lib, 'children')
    for rule_lib in rules:
        sub_lib, next_id = build_library_element(objects, rule_lib, objects, next_id)
        ET.SubElement(children, 'item').text = rule_lib['external_id']
        coll = sub_lib.find('collections')
        if coll is None:
            coll = ET.SubElement(sub_lib, 'collections')
        ET.SubElement(coll, 'item').text = 'Factory_Plate_NX2512_General_Lib'
        
    print(f"💾 保存修改后的 XML")
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)

if __name__ == '__main__':
    main()
