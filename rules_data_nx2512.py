"""
NX-FBM NX2512 MKE 规则数据定义
版本: v2512.0
项目名称: NX-FBM
说明: 仅包含规则数据，不包含 XML 序列化逻辑
      使用 fbm_generator_core.py 中的 FBMGenerator 生成 XML
      基于 update_mke_rules_v2.py 重构
"""

from fbm_generator_core import MachiningRule, RuleLibrary


def create_nx2512_rules() -> list:
    """创建 NX2512 板类零件加工规则库"""
    rules = []
    
    # ==================== 01_Face_Milling ====================
    face_lib = RuleLibrary(
        name="01_Face_Milling",
        external_id="Factory_Plate_NX2512_01_Face_Milling",
        description="面加工库 (NX2512)",
        children=[
            MachiningRule(
                name="1.1_Face_Top_Rough_D80",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1210,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.LENGTH", ">", "200.0")],
                tool_attrs=[("tool.Libref", "=", "D63L200")],
                description="顶面粗加工 D80"
            ),
            MachiningRule(
                name="1.2_Face_Top_Rough_D63",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1220,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.LENGTH", "<=", "200.0")],
                tool_attrs=[("tool.Libref", "=", "D63R6L200")],
                description="顶面粗加工 D63"
            ),
            MachiningRule(
                name="1.3_Face_Bottom_Finish_D63",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1230,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.LENGTH", ">", "150.0")],
                tool_attrs=[("tool.Libref", "=", "D63R6L200")],
                description="底面精加工 D63"
            ),
            MachiningRule(
                name="1.4_Face_Bottom_Finish_D40",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1240,
                mwf="SURFACE_PLANAR_RECTANGULAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.LENGTH", "<=", "150.0")],
                tool_attrs=[("tool.Libref", "=", "D35L99")],
                description="底面精加工 D40"
            ),
            MachiningRule(
                name="1.5_Outer_Profile_Rough_D63R08",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1250,
                mwf="SURFACE_PLANAR",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.DEPTH", ">", "0.0")],
                tool_attrs=[("tool.Libref", "=", "D63R08L200")],
                description="外轮廓粗加工 D63R08"
            ),
            MachiningRule(
                name="1.6_Outer_Profile_Finish_D20",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1260,
                mwf="SURFACE_PLANAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.DEPTH", ">=", "50.0")],
                tool_attrs=[("tool.Libref", "=", "D20L77")],
                description="外轮廓精加工 D20"
            ),
            MachiningRule(
                name="1.7_Outer_Profile_Finish_D12",
                operation_class="mill_planar.FLOOR_WALL",
                priority=1265,
                mwf="SURFACE_PLANAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.DEPTH", ">", "0.0"), ("mwf.DEPTH", "<", "50.0")],
                tool_attrs=[("tool.Libref", "=", "D12L55")],
                description="外轮廓精加工 D12"
            ),
        ]
    )
    rules.append(face_lib)
    
    # ==================== 02_Pocket_Slot ====================
    pocket_lib = RuleLibrary(
        name="02_Pocket_Slot",
        external_id="Factory_Plate_NX2512_02_Pocket_Slot",
        description="型腔与槽库 (NX2512)",
        children=[
            MachiningRule(
                name="2.1_Pocket_Rough_D63R08",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2410,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "65.0")],
                tool_attrs=[("tool.Libref", "=", "D63R08L200")],
                description="型腔粗加工 D63R08"
            ),
            MachiningRule(
                name="2.2_Pocket_Rough_D35R08",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2415,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "37.0"), ("mwf.WIDTH", "<", "65.0")],
                tool_attrs=[("tool.Libref", "=", "D35R08L99")],
                description="型腔粗加工 D35R08"
            ),
            MachiningRule(
                name="2.3_Pocket_Rough_D21R08",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2420,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "22.0"), ("mwf.WIDTH", "<", "37.0")],
                tool_attrs=[("tool.Libref", "=", "D21R08L77")],
                description="型腔粗加工 D21R08"
            ),
            MachiningRule(
                name="2.4_Pocket_Rough_D17R08",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2425,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="FACE_MILL_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "18.0"), ("mwf.WIDTH", "<", "22.0")],
                tool_attrs=[("tool.Libref", "=", "D17R08L66")],
                description="型腔粗加工 D17R08"
            ),
            MachiningRule(
                name="2.5_Pocket_Rough_D12L55",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2430,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", "<", "18.0"), ("mwf.WIDTH", ">=", "12.5")],
                tool_attrs=[("tool.Libref", "=", "D12L55")],
                description="型腔粗加工 D12"
            ),
            MachiningRule(
                name="2.5_Pocket_Rough_D10L55",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2431,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", "<", "12.5"), ("mwf.WIDTH", ">=", "10.5")],
                tool_attrs=[("tool.Libref", "=", "D10L55")],
                description="型腔粗加工 D10"
            ),
            MachiningRule(
                name="2.5_Pocket_Rough_D8L44",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2432,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", "<", "10.5"), ("mwf.WIDTH", ">=", "8.5")],
                tool_attrs=[("tool.Libref", "=", "D8L44")],
                description="型腔粗加工 D8"
            ),
            MachiningRule(
                name="2.5_Pocket_Rough_D6L33",
                operation_class="mill_contour.CAVITY_MILL",
                priority=2433,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", "<", "8.5"), ("mwf.WIDTH", ">=", "0.0")],
                tool_attrs=[("tool.Libref", "=", "D6L33")],
                description="型腔粗加工 D6"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Wall_D20L77",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2440,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "10.0")],
                tool_attrs=[("tool.Libref", "=", "D20L77")],
                description="型腔壁精加工 D20"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Wall_D12L55",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2441,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "6.0"), ("mwf.BOTTOM_RADIUS", "<", "10.0")],
                tool_attrs=[("tool.Libref", "=", "D12L55")],
                description="型腔壁精加工 D12"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Wall_D10L55",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2442,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "5.0"), ("mwf.BOTTOM_RADIUS", "<", "6.0")],
                tool_attrs=[("tool.Libref", "=", "D10L55")],
                description="型腔壁精加工 D10"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Wall_D8L44",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2443,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "4.0"), ("mwf.BOTTOM_RADIUS", "<", "5.0")],
                tool_attrs=[("tool.Libref", "=", "D8L44")],
                description="型腔壁精加工 D8"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Wall_D6L33",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2444,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "0.0"), ("mwf.BOTTOM_RADIUS", "<", "4.0")],
                tool_attrs=[("tool.Libref", "=", "D6L33")],
                description="型腔壁精加工 D6"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Floor_D20L77",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2450,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "10.0")],
                tool_attrs=[("tool.Libref", "=", "D20L77")],
                description="型腔底精加工 D20"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Floor_D12L55",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2451,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "6.0"), ("mwf.BOTTOM_RADIUS", "<", "10.0")],
                tool_attrs=[("tool.Libref", "=", "D12L55")],
                description="型腔底精加工 D12"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Floor_D10L55",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2452,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "5.0"), ("mwf.BOTTOM_RADIUS", "<", "6.0")],
                tool_attrs=[("tool.Libref", "=", "D10L55")],
                description="型腔底精加工 D10"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Floor_D8L44",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2453,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "4.0"), ("mwf.BOTTOM_RADIUS", "<", "5.0")],
                tool_attrs=[("tool.Libref", "=", "D8L44")],
                description="型腔底精加工 D8"
            ),
            MachiningRule(
                name="2.6_Pocket_Finish_Floor_D6L33",
                operation_class="mill_planar.FLOOR_WALL",
                priority=2454,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.BOTTOM_RADIUS", ">=", "0.0"), ("mwf.BOTTOM_RADIUS", "<", "4.0")],
                tool_attrs=[("tool.Libref", "=", "D6L33")],
                description="型腔底精加工 D6"
            ),
            MachiningRule(
                name="2.7_Slot_Rough_D20L77",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2460,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "21.0")],
                tool_attrs=[("tool.Libref", "=", "D20L77")],
                description="槽粗加工 D20"
            ),
            MachiningRule(
                name="2.7_Slot_Rough_D12L55",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2461,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "13.0"), ("mwf.WIDTH", "<", "21.0")],
                tool_attrs=[("tool.Libref", "=", "D12L55")],
                description="槽粗加工 D12"
            ),
            MachiningRule(
                name="2.7_Slot_Rough_D10L55",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2462,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "11.0"), ("mwf.WIDTH", "<", "13.0")],
                tool_attrs=[("tool.Libref", "=", "D10L55")],
                description="槽粗加工 D10"
            ),
            MachiningRule(
                name="2.7_Slot_Rough_D8L44",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2463,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "9.0"), ("mwf.WIDTH", "<", "11.0")],
                tool_attrs=[("tool.Libref", "=", "D8L44")],
                description="槽粗加工 D8"
            ),
            MachiningRule(
                name="2.7_Slot_Rough_D6L33",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2464,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "0.0"), ("mwf.WIDTH", "<", "9.0")],
                tool_attrs=[("tool.Libref", "=", "D6L33")],
                description="槽粗加工 D6"
            ),
            MachiningRule(
                name="2.7_Slot_Finish_D20L77",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2470,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "21.0")],
                tool_attrs=[("tool.Libref", "=", "D20L77")],
                description="槽精加工 D20"
            ),
            MachiningRule(
                name="2.7_Slot_Finish_D12L55",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2471,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "13.0"), ("mwf.WIDTH", "<", "21.0")],
                tool_attrs=[("tool.Libref", "=", "D12L55")],
                description="槽精加工 D12"
            ),
            MachiningRule(
                name="2.7_Slot_Finish_D10L55",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2472,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "11.0"), ("mwf.WIDTH", "<", "13.0")],
                tool_attrs=[("tool.Libref", "=", "D10L55")],
                description="槽精加工 D10"
            ),
            MachiningRule(
                name="2.7_Slot_Finish_D8L44",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2473,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "9.0"), ("mwf.WIDTH", "<", "11.0")],
                tool_attrs=[("tool.Libref", "=", "D8L44")],
                description="槽精加工 D8"
            ),
            MachiningRule(
                name="2.7_Slot_Finish_D6L33",
                operation_class="mill_planar.GROOVE_MILLING",
                priority=2474,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="END_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">=", "0.0"), ("mwf.WIDTH", "<", "9.0")],
                tool_attrs=[("tool.Libref", "=", "D6L33")],
                description="槽精加工 D6"
            ),
        ]
    )
    rules.append(pocket_lib)
    
    # ==================== 03_Hole_Making ====================
    hole_lib = RuleLibrary(
        name="03_Hole_Making_NX2512",
        external_id="Factory_Plate_NX2512_03_Hole_Making",
        description="新版孔加工库 (NX2512 hole_making)",
        children=[]
    )
    
    # 3.1 Spot (定位钻)
    spot_lib = RuleLibrary(
        name="3.1_Spot",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Spot",
        description="定位钻",
        children=[
            MachiningRule(
                name="3.1_Spot_Chamfer_Large",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1100,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">", "8.1"), ("mwf.DIAMETER_1", "<=", "20.5")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="大孔定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Thread_M4",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1110,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "3.1"), ("mwf.DIAMETER_1", "<=", "3.5")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="M4螺纹定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Thread_M5",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1120,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "4.1"), ("mwf.DIAMETER_1", "<=", "4.5")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="M5螺纹定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Thread_M6",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1130,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "5.1"), ("mwf.DIAMETER_1", "<=", "5.5")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="M6螺纹定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Thread_M8",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1140,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "6.5"), ("mwf.DIAMETER_1", "<=", "6.98")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="M8螺纹定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Pin_D4",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1150,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "3.98"), ("mwf.DIAMETER_1", "<=", "4.02")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="D4销孔定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Pin_D5",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1160,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "4.98"), ("mwf.DIAMETER_1", "<=", "5.02")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="D5销孔定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Pin_D6",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1170,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "5.98"), ("mwf.DIAMETER_1", "<=", "6.02")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="D6销孔定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_Pin_D8",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1180,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">=", "7.98"), ("mwf.DIAMETER_1", "<=", "8.02")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="D8销孔定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_General_Small",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1190,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">", "0.0"), ("mwf.DIAMETER_1", "<=", "5.0")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="小孔通用定位钻"
            ),
            MachiningRule(
                name="3.1_Spot_Chamfer_General_Medium",
                operation_class="hole_making.SPOT_DRILLING",
                priority=1195,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CENTER_DRILL",
                criteria=[("mwf.DIAMETER_1", ">", "5.0"), ("mwf.DIAMETER_1", "<=", "8.1")],
                tool_attrs=[("tool.Libref", "=", "SD10")],
                description="中孔通用定位钻"
            ),
        ]
    )
    hole_lib.children.append(spot_lib)
    
    # 3.2 Thread Bottom (螺纹底孔)
    thread_bottom_lib = RuleLibrary(
        name="3.2_Thread_Bottom",
        external_id="Factory_Plate_NX2512_03_Hole_Making_ThreadBottom",
        description="螺纹底孔",
        children=[]
    )
    
    thread_bottoms = [
        ("3.2_Thread_Bottom_D3", "2210", 3.4, 3.10, 3.50, "ZD3.3"),
        ("3.2_Thread_Bottom_D4", "2220", 4.3, 4.10, 4.50, "ZD4.3"),
        ("3.2_Thread_Bottom_D5", "2230", 5.2, 5.10, 5.50, "ZD5.2"),
        ("3.2_Thread_Bottom_D6", "2240", 6.9, 6.50, 6.98, "ZD6.8"),
        ("3.2_Thread_Bottom_D8", "2250", 8.7, 8.10, 8.98, "ZD8.7"),
        ("3.2_Thread_Bottom_D10", "2260", 10.5, 10.10, 10.80, "ZD10.5"),
        ("3.2_Thread_Bottom_D14", "2270", 14.3, 13.50, 14.50, "ZD14.2"),
        ("3.2_Thread_Bottom_D17", "2280", 17.8, 17.10, 17.98, "ZD17.7"),
    ]
    
    for name, priority, d, d_min, d_max, libref in thread_bottoms:
        thread_bottom_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=int(priority),
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Libref", "=", libref)],
            description=f"螺纹底孔 D{d}"
        ))
    hole_lib.children.append(thread_bottom_lib)
    
    # 3.2.1 Tapping (攻丝)
    tapping_lib = RuleLibrary(
        name="3.2.1_Tapping",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Tapping",
        description="攻丝加工",
        children=[]
    )
    
    tappings = [
        ("3.2.1_Tapping_M4", "2215", 4.0, 3.10, 3.50),
        ("3.2.1_Tapping_M5", "2225", 5.0, 4.10, 4.50),
        ("3.2.1_Tapping_M6", "2235", 6.0, 5.10, 5.50),
        ("3.2.1_Tapping_M8", "2245", 8.0, 6.50, 6.98),
        ("3.2.1_Tapping_M10", "2255", 10.0, 8.10, 8.98),
    ]
    
    for name, priority, tap_d, d_min, d_max in tappings:
        tapping_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.TAPPING",
            priority=int(priority),
            mwf="STEP1HOLE_THREAD",
            lwf="STEP1HOLE",
            tool_class="TAP",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Diameter", ">=", str(round(tap_d-0.05, 2))), 
                       ("tool.Diameter", "<=", str(round(tap_d+0.05, 2)))],
            description=f"攻丝 M{tap_d}"
        ))
    hole_lib.children.append(tapping_lib)
    
    # 3.3 Thread Through (螺纹过孔)
    thread_through_lib = RuleLibrary(
        name="3.3_Thread_Through",
        external_id="Factory_Plate_NX2512_03_Hole_Making_ThreadThrough",
        description="螺纹过孔",
        children=[]
    )
    
    thread_throughs = [
        ("3.3_Thread_Through_D9", "2310", 9.0, 8.98, 9.02, "ZD9.1"),
        ("3.3_Thread_Through_D11", "2320", 11.0, 10.98, 11.02, "ZD11.1"),
        ("3.3_Thread_Through_D13", "2330", 13.0, 12.98, 13.02, "ZD13.1"),
        ("3.3_Thread_Through_D17", "2340", 17.0, 16.98, 17.02, "ZD17.1"),
        ("3.3_Thread_Through_D21", "2350", 21.0, 20.98, 21.02, "ZD21.5"),
    ]
    
    for name, priority, d, d_min, d_max, libref in thread_throughs:
        thread_through_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=int(priority),
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Libref", "=", libref)],
            description=f"螺纹过孔 D{d}"
        ))
    hole_lib.children.append(thread_through_lib)
    
    # 3.4 Pin Hole (销孔)
    pin_hole_lib = RuleLibrary(
        name="3.4_Pin_Hole",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Pin",
        description="销孔",
        children=[]
    )
    
    # 3.4.1 Pre-Drill (预钻孔) - 注意：直径窗口为成品孔径
    pre_drill_lib = RuleLibrary(
        name="3.4_Pin_Pre",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Pin_Pre",
        description="预钻孔",
        children=[]
    )
    
    pin_pres = [
        ("3.4_Pin_Pre_D4", "2110", 4.0, 3.98, 4.02, "ZD3.7"),
        ("3.4_Pin_Pre_D5", "2120", 5.0, 4.98, 5.02, "ZD4.6"),
        ("3.4_Pin_Pre_D6", "2130", 6.0, 5.98, 6.02, "ZD5.6"),
        ("3.4_Pin_Pre_D8", "2140", 8.0, 7.98, 8.02, "ZD7.5"),
        ("3.4_Pin_Pre_D10", "2150", 10.0, 9.98, 10.02, "ZD9.5"),
        ("3.4_Pin_Pre_D12", "2160", 12.0, 11.98, 12.02, "ZD11.5"),
        ("3.4_Pin_Pre_D16", "2170", 16.0, 15.98, 16.02, "ZD17.1"),
        ("3.4_Pin_Pre_D20", "2180", 20.0, 19.98, 20.02, "ZD21.5"),
    ]
    
    for name, priority, d, d_min, d_max, libref in pin_pres:
        pre_drill_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=int(priority),
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Libref", "=", libref)],
            description=f"销孔预钻 D{d}"
        ))
    pin_hole_lib.children.append(pre_drill_lib)
    
    # 3.4.2 Ream (铰孔)
    ream_lib = RuleLibrary(
        name="3.4_Pin_Ream",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Pin_Ream",
        description="铰孔",
        children=[]
    )
    
    pin_reams = [
        ("3.4_Pin_Ream_D4", "3110", 4.0, 3.98, 4.02, "JD4"),
        ("3.4_Pin_Ream_D5", "3120", 5.0, 4.98, 5.02, "JD5"),
        ("3.4_Pin_Ream_D6", "3130", 6.0, 5.98, 6.02, "JD6"),
        ("3.4_Pin_Ream_D8", "3140", 8.0, 7.98, 8.02, "JD8"),
        ("3.4_Pin_Ream_D10", "3150", 10.0, 9.98, 10.02, "JD10"),
        ("3.4_Pin_Ream_D12", "3160", 12.0, 11.98, 12.02, "JD12"),
        ("3.4_Pin_Ream_D16", "3170", 16.0, 15.98, 16.02, "JD16"),
    ]
    
    for name, priority, d, d_min, d_max, libref in pin_reams:
        ream_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.BORING_REAMING",
            priority=int(priority),
            mwf="STEP2HOLE",
            lwf="STEP1HOLE",
            tool_class="CHUCKING_REAMER",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)), ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Libref", "=", libref)],
            description=f"销孔铰孔 D{d}"
        ))
    pin_hole_lib.children.append(ream_lib)
    hole_lib.children.append(pin_hole_lib)
    
    # 3.5 Standard Drill (标准直钻孔)
    std_drill_lib = RuleLibrary(
        name="3.5_Standard_Drill",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Standard_Drill",
        description="标准直钻孔 (默认兜底)",
        children=[]
    )
    
    std_drills = [
        ("3.5_Standard_Drill_D3", "2510", 3.0, "ZD3.3"),
        ("3.5_Standard_Drill_D4", "2520", 4.0, "ZD4.3"),
        ("3.5_Standard_Drill_D5", "2530", 5.0, "ZD5.2"),
        ("3.5_Standard_Drill_D6", "2540", 6.0, "ZD5.6"),
        ("3.5_Standard_Drill_D8", "2550", 8.0, "ZD7.5"),
        ("3.5_Standard_Drill_D10", "2560", 10.0, "ZD9.5"),
        ("3.5_Standard_Drill_D12", "2570", 12.0, "ZD12.1"),
        ("3.5_Standard_Drill_D14", "2580", 14.0, "ZD14.2"),
    ]
    
    for name, priority, d, libref in std_drills:
        std_drill_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.DRILLING",
            priority=int(priority),
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(round(d-0.05, 2))), ("mwf.DIAMETER_1", "<=", str(round(d+0.05, 2)))],
            tool_attrs=[("tool.Libref", "=", libref)],
            description=f"标准钻孔 D{d}"
        ))
    hole_lib.children.append(std_drill_lib)
    
    # 3.6 Large Hole (大孔)
    large_hole_lib = RuleLibrary(
        name="3.6_Large_Hole",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Large_Hole",
        description="大孔直铣",
        children=[
            MachiningRule(
                name="3.6_Large_Hole_Mill",
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
    
    # 3.7 Counter Bore (沉头孔)
    counter_bore_lib = RuleLibrary(
        name="3.7_Counter_Bore",
        external_id="Factory_Plate_NX2512_03_Hole_Making_Counter_Bore",
        description="沉头孔加工",
        children=[]
    )
    
    counter_bores = [
        ("3.7_CB_M4", "2610", 8.0, "D8L44"),
        ("3.7_CB_M5", "2620", 10.0, "D10L55"),
        ("3.7_CB_M6", "2630", 11.0, "D10L55"),
        ("3.7_CB_M8", "2640", 15.0, "D12L55"),
        ("3.7_CB_M10", "2650", 18.0, "D12L55"),
        ("3.7_CB_M12", "2660", 20.0, "D20L77"),
    ]
    
    for name, priority, d_cb, libref in counter_bores:
        counter_bore_lib.children.append(MachiningRule(
            name=name,
            operation_class="hole_making.HOLE_MILLING",
            priority=int(priority),
            mwf="STEP2HOLE",
            lwf="STEP1HOLE",
            tool_class="END_MILL_NON_INDEXABLE",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_cb-0.5)), ("mwf.DIAMETER_1", "<=", str(d_cb+0.5))],
            tool_attrs=[("tool.Libref", "=", libref)],
            description=f"沉头孔 M{int(d_cb)}"
        ))
    hole_lib.children.append(counter_bore_lib)
    
    rules.append(hole_lib)
    
    # ==================== 04_Chamfer ====================
    chamfer_lib = RuleLibrary(
        name="04_Chamfer",
        external_id="Factory_Plate_NX2512_04_Chamfer",
        description="倒角库 (NX2512)",
        children=[
            MachiningRule(
                name="4.1_Hole_Chamfer_Large",
                operation_class="hole_making.HOLE_CHAMFER_MILLING",
                priority=3310,
                mwf="STEP1HOLE",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                criteria=[("mwf.DIAMETER_1", ">", "20.5"), ("mwf.DIAMETER_1", "<=", "200.0")],
                tool_attrs=[("tool.Libref", "=", "DD25")],
                description="大孔倒角"
            ),
            MachiningRule(
                name="4.2_Counter_Bore_Chamfer",
                operation_class="hole_making.HOLE_CHAMFER_MILLING",
                priority=3315,
                mwf="STEP2HOLE",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                criteria=[("mwf.DIAMETER_1", ">", "0.0")],
                tool_attrs=[("tool.Libref", "=", "DD25")],
                description="沉头孔倒角"
            ),
            MachiningRule(
                name="4.3_Pocket_Chamfer_C1",
                operation_class="mill_planar.FLOOR_WALL",
                priority=3330,
                mwf="POCKET_RECTANGULAR_STRAIGHT",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">", "0.0")],
                tool_attrs=[("tool.Libref", "=", "DD25")],
                oper_attrs=[
                    ("oper.Corner_Control_Fillet_Flag", "=", "1"),
                    ("oper.Corner_Control_Fillet_Delta_Radius", "=", "3.0")
                ],
                description="型腔倒角 C1"
            ),
            MachiningRule(
                name="4.4_Slot_Chamfer_C1",
                operation_class="mill_planar.FLOOR_WALL",
                priority=3340,
                mwf="SLOT_RECTANGULAR",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                criteria=[("mwf.WIDTH", ">", "0.0")],
                tool_attrs=[("tool.Libref", "=", "DD25")],
                oper_attrs=[
                    ("oper.Corner_Control_Fillet_Flag", "=", "1"),
                    ("oper.Corner_Control_Fillet_Delta_Radius", "=", "3.0")
                ],
                description="槽倒角 C1"
            ),
            MachiningRule(
                name="4.5_Outer_Chamfer_C3",
                operation_class="mill_planar.FLOOR_WALL",
                priority=3350,
                mwf="SURFACE_PLANAR",
                lwf="BLANK",
                tool_class="CHAMFER_MILL_NON_INDEXABLE",
                criteria=[("mwf.LENGTH", ">", "0.0")],
                tool_attrs=[("tool.Libref", "=", "DD25")],
                oper_attrs=[
                    ("oper.Corner_Control_Fillet_Flag", "=", "1"),
                    ("oper.Corner_Control_Fillet_Delta_Radius", "=", "3.0")
                ],
                description="外轮廓倒角 C3"
            ),
        ]
    )
    rules.append(chamfer_lib)
    
    return rules


if __name__ == '__main__':
    # 测试数据定义
    rules = create_nx2512_rules()
    print(f"✅ 成功创建 {len(rules)} 个主规则库")
    
    for lib in rules:
        print(f"  - {lib.name}: {len(lib.children)} 个子项")
