"""
NX12 MKE 规则数据定义
版本: v12.0
说明: 仅包含规则数据，不包含 XML 序列化逻辑
      使用 fbm_generator_core.py 中的 FBMGenerator 生成 XML
"""

from fbm_generator_core import MachiningRule, RuleLibrary


def create_nx12_rules() -> list:
    """创建 NX12 板类零件加工规则库"""
    rules = []
    
    # ==================== 01_Face_Milling ====================
    face_lib = RuleLibrary(
        name="01_Face_Milling",
        external_id="Factory_Plate_01_Face_Milling",
        description="面加工库",
        children=[
            MachiningRule(
                name="1.1_Face_Top_Rough",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1210,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "40.0"), ("tool.Diameter", "<=", "80.0")],
                description="顶面粗加工"
            ),
            MachiningRule(
                name="1.2_Face_Top_Finish",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1220,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "32.0"), ("tool.Diameter", "<=", "63.0")],
                description="顶面精加工"
            ),
            MachiningRule(
                name="1.3_Face_Bottom_Finish",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1230,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "32.0"), ("tool.Diameter", "<=", "63.0")],
                description="底面精加工"
            ),
            MachiningRule(
                name="1.4_Face_ThinWall_LightCut",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1240,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "16.0"), ("tool.Diameter", "<=", "40.0")],
                description="薄壁轻切削"
            ),
        ]
    )
    rules.append(face_lib)
    
    # ==================== 02_Pocket_Slot ====================
    pocket_lib = RuleLibrary(
        name="02_Pocket_Slot",
        external_id="Factory_Plate_02_Pocket_Slot",
        description="型腔与槽库",
        children=[
            MachiningRule(
                name="2.1_Pocket_Rough_General",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2410,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.DEPTH", ">=", "1.0"), ("mwf.DEPTH", "<=", "40.0")],
                tool_attrs=[("tool.Diameter", ">=", "8.0"), ("tool.Diameter", "<=", "20.0")],
                description="型腔粗加工"
            ),
            MachiningRule(
                name="2.2_Pocket_Finish_Wall",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2420,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.DEPTH", ">=", "1.0"), ("mwf.DEPTH", "<=", "40.0")],
                tool_attrs=[("tool.Diameter", ">=", "6.0"), ("tool.Diameter", "<=", "16.0")],
                description="型腔壁精加工"
            ),
            MachiningRule(
                name="2.3_Pocket_Finish_Floor",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2430,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.DEPTH", ">=", "1.0"), ("mwf.DEPTH", "<=", "40.0")],
                tool_attrs=[("tool.Diameter", ">=", "6.0"), ("tool.Diameter", "<=", "20.0")],
                description="型腔底精加工"
            ),
            MachiningRule(
                name="2.4_Slot_Open_Rough",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2440,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "5.0"), ("tool.Diameter", "<=", "16.0")],
                description="开口槽粗加工"
            ),
            MachiningRule(
                name="2.5_Slot_Closed_Finish",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2450,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "3.0"), ("tool.Diameter", "<=", "10.0")],
                description="闭口槽精加工"
            ),
            MachiningRule(
                name="2.6_Corner_Rest_Mill",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2460,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.DEPTH", "<=", "30.0")],
                tool_attrs=[("tool.Diameter", ">=", "2.0"), ("tool.Diameter", "<=", "8.0")],
                description="清角加工"
            ),
        ]
    )
    rules.append(pocket_lib)
    
    # ==================== 03_Hole_Making ====================
    hole_lib = RuleLibrary(
        name="03_Hole_Making",
        external_id="Factory_Plate_03_Hole_Making",
        description="孔加工库",
        children=[]
    )
    
    # 3.1 Spot (定位钻)
    spot_lib = RuleLibrary(
        name="3.1_Spot",
        external_id="Factory_Plate_03_Hole_Making_Spot",
        description="定位钻",
        children=[
            MachiningRule(
                name="3.1_Spot_D10",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1100,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "3.0"), ("mwf.DIAMETER_1", "<=", "22.0")],
                tool_attrs=[("tool.Diameter", "=", "10.0")],
                description="定位钻 D10"
            ),
        ]
    )
    hole_lib.children.append(spot_lib)
    
    # 3.2 Thread Bottom (螺纹底孔)
    thread_bottom_lib = RuleLibrary(
        name="3.2_Thread_Bottom",
        external_id="Factory_Plate_03_Hole_Making_ThreadBottom",
        description="螺纹底孔",
        children=[]
    )
    
    thread_bottoms = [
        ("3.2_Thread_Bottom_D3p4", 2210, 3.4, 3.10, 3.50),
        ("3.2_Thread_Bottom_D4p3", 2220, 4.3, 4.10, 4.50),
        ("3.2_Thread_Bottom_D5p2", 2230, 5.2, 5.10, 5.50),
        ("3.2_Thread_Bottom_D6p9", 2240, 6.9, 6.50, 6.98),
        ("3.2_Thread_Bottom_D8p7", 2250, 8.7, 8.10, 8.98),
        ("3.2_Thread_Bottom_D10p5", 2260, 10.5, 10.10, 10.80),
        ("3.2_Thread_Bottom_D14p3", 2270, 14.3, 13.50, 14.50),
        ("3.2_Thread_Bottom_D17p8", 2280, 17.8, 17.10, 17.98),
    ]
    
    for name, priority, d, d_min, d_max in thread_bottoms:
        thread_bottom_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=priority,
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Diameter", ">=", str(round(d-0.05, 2))), 
                       ("tool.Diameter", "<=", str(round(d+0.05, 2)))],
            description=f"螺纹底孔 D{d}"
        ))
    
    hole_lib.children.append(thread_bottom_lib)
    
    # 3.3 Thread Through (螺纹过孔)
    thread_through_lib = RuleLibrary(
        name="3.3_Thread_Through",
        external_id="Factory_Plate_03_Hole_Making_ThreadThrough",
        description="螺纹过孔",
        children=[]
    )
    
    thread_throughs = [
        ("3.3_Thread_Through_D9", 2310, 9.0, 8.98, 9.02),
        ("3.3_Thread_Through_D11", 2320, 11.0, 10.98, 11.02),
        ("3.3_Thread_Through_D13", 2330, 13.0, 12.98, 13.02),
        ("3.3_Thread_Through_D17", 2340, 17.0, 16.98, 17.02),
        ("3.3_Thread_Through_D21", 2350, 21.0, 20.98, 21.02),
    ]
    
    for name, priority, d, d_min, d_max in thread_throughs:
        thread_through_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=priority,
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Diameter", ">=", str(round(d-0.05, 2))), 
                       ("tool.Diameter", "<=", str(round(d+0.05, 2)))],
            description=f"螺纹过孔 D{d}"
        ))
    
    hole_lib.children.append(thread_through_lib)
    
    # 3.4 Pin Hole (销孔)
    pin_hole_lib = RuleLibrary(
        name="3.4_Pin_Hole",
        external_id="Factory_Plate_03_Hole_Making_Pin",
        description="销孔",
        children=[]
    )
    
    # 3.4.1 Pre-Drill (预钻孔)
    pre_drill_lib = RuleLibrary(
        name="3.4_Pin_Pre",
        external_id="Factory_Plate_03_Hole_Making_Pin_Pre",
        description="预钻孔",
        children=[]
    )
    
    pin_pres = [
        ("3.4_Pin_Pre_D4", 2110, 3.7, 3.68, 3.72),
        ("3.4_Pin_Pre_D5", 2120, 4.7, 4.68, 4.72),
        ("3.4_Pin_Pre_D6", 2130, 5.7, 5.68, 5.72),
        ("3.4_Pin_Pre_D8", 2140, 7.7, 7.68, 7.72),
        ("3.4_Pin_Pre_D10", 2150, 9.7, 9.68, 9.72),
        ("3.4_Pin_Pre_D12", 2160, 11.7, 11.68, 11.72),
        ("3.4_Pin_Pre_D16", 2170, 15.7, 15.68, 15.72),
        ("3.4_Pin_Pre_D20", 2180, 19.7, 19.68, 19.72),
    ]
    
    for name, priority, d, d_min, d_max in pin_pres:
        pre_drill_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=priority,
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Diameter", ">=", str(round(d-0.05, 2))), 
                       ("tool.Diameter", "<=", str(round(d+0.05, 2)))],
            description=f"销孔预钻 D{d}"
        ))
    
    pin_hole_lib.children.append(pre_drill_lib)
    
    # 3.4.2 Ream (铰孔)
    ream_lib = RuleLibrary(
        name="3.4_Pin_Ream",
        external_id="Factory_Plate_03_Hole_Making_Pin_Ream",
        description="铰孔",
        children=[]
    )
    
    pin_reams = [
        ("3.4_Pin_Ream_D4", 3110, 4.0, 3.98, 4.02),
        ("3.4_Pin_Ream_D5", 3120, 5.0, 4.98, 5.02),
        ("3.4_Pin_Ream_D6", 3130, 6.0, 5.98, 6.02),
        ("3.4_Pin_Ream_D8", 3140, 8.0, 7.98, 8.02),
        ("3.4_Pin_Ream_D10", 3150, 10.0, 9.98, 10.02),
        ("3.4_Pin_Ream_D12", 3160, 12.0, 11.98, 12.02),
        ("3.4_Pin_Ream_D16", 3170, 16.0, 15.98, 16.02),
        ("3.4_Pin_Ream_D20", 3180, 20.0, 19.98, 20.02),
    ]
    
    for name, priority, d, d_min, d_max in pin_reams:
        ream_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=priority,
            mwf="STEP2HOLE",
            lwf="STEP1HOLE",
            tool_class="CHUCKING_REAMER",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Diameter", ">=", str(round(d-0.05, 2))), 
                       ("tool.Diameter", "<=", str(round(d+0.05, 2)))],
            description=f"销孔铰孔 D{d}"
        ))
    
    pin_hole_lib.children.append(ream_lib)
    hole_lib.children.append(pin_hole_lib)
    
    # 3.5 Large Hole (大孔)
    large_hole_lib = RuleLibrary(
        name="3.5_Large_Hole",
        external_id="Factory_Plate_03_Hole_Making_Large_Hole",
        description="大孔",
        children=[
            MachiningRule(
                name="3.5_Large_Hole_Mill",
                operation_class="hole_making.HOLE_MILLING",
                priority=3210,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.DIAMETER_1", ">", "21.0"), ("mwf.DIAMETER_1", "<=", "200.0")],
                tool_attrs=[("tool.Diameter", ">=", "10.0"), ("tool.Diameter", "<=", "20.0")],
                description="大孔铣削"
            ),
        ]
    )
    hole_lib.children.append(large_hole_lib)
    
    rules.append(hole_lib)
    
    # ==================== 04_Chamfer ====================
    chamfer_lib = RuleLibrary(
        name="04_Chamfer",
        external_id="Factory_Plate_04_Chamfer",
        description="倒角库",
        children=[
            MachiningRule(
                name="4.1_Hole_Chamfer_C0p5",
                operation_class="hole_making.HOLE_CHAMFER_MILLING",
                priority=3310,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                criteria=[("mwf.DIAMETER_1", ">=", "3.0"), ("mwf.DIAMETER_1", "<=", "20.0")],
                tool_attrs=[("tool.Diameter", ">=", "5.0"), ("tool.Diameter", "<=", "16.0")],
                description="孔口倒角 C0.5"
            ),
            MachiningRule(
                name="4.2_Hole_Chamfer_C1p0",
                operation_class="hole_making.HOLE_CHAMFER_MILLING",
                priority=3320,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                criteria=[("mwf.DIAMETER_1", ">=", "6.0"), ("mwf.DIAMETER_1", "<=", "30.0")],
                tool_attrs=[("tool.Diameter", ">=", "8.0"), ("tool.Diameter", "<=", "20.0")],
                description="孔口倒角 C1.0"
            ),
            MachiningRule(
                name="4.3_Outer_Chamfer_General",
                operation_class="mill_planar.FLOOR_WALL",
                priority=3330,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "8.0"), ("tool.Diameter", "<=", "25.0")],
                description="外轮廓倒角"
            ),
            MachiningRule(
                name="4.4_Deburr_Light_Pass",
                operation_class="mill_planar.FLOOR_WALL",
                priority=3340,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                tool_attrs=[("tool.Diameter", ">=", "6.0"), ("tool.Diameter", "<=", "20.0")],
                description="去毛刺轻切削"
            ),
        ]
    )
    rules.append(chamfer_lib)
    
    return rules


if __name__ == '__main__':
    # 测试数据定义
    rules = create_nx12_rules()
    print(f"✅ 成功创建 {len(rules)} 个主规则库")
    
    for lib in rules:
        print(f"  - {lib.name}: {len(lib.children)} 个子项")
