import sys
import os
import re
import math
import unicodedata
import subprocess

"""
================================================================================
NX FBM (MKE) 自定义刀具智能生成器 (NX Tool Builder)
================================================================================

使用说明：
本脚本用于在本地环境同步和更新 NX tool_database.dat 中的自定义刀具。将本脚本
复制到任意版本的刀库目录下直接运行即可。

【核心特性：在库首自动创建集中式的自定义刀具区域】
1. 自动读取当前目录下的 `tool_database.dat`。
2. 扫描库中现存的自定义刀具并在原处将其移除。
3. 根据 `CUSTOM_TOOLS` 列表，自动推断刀具物理属性并生成标准化据体。
4. 在库首统一生成 `# >>>>>> 自定义刀具（置顶置前显示区）<<<<<<` 区块，
   其下直接包揽各项 `#CLASS` 与生成的格式和数据，确保查找便捷并规避原生库混淆。
5. 所有更新严格遵循 MKE 的 ASCII 列宽对齐（`w+1 定理`）。

运行方式：
  python nx_tool_builder.py 
或指定文件：
  python nx_tool_builder.py [输入库文件] [输出库文件]
================================================================================
"""

CUSTOM_TOOLS_INPUT = """
# 整体式圆柱立铣刀 (CLASS END_MILL_NON_INDEXABLE)
D4L22,D6L33,D8L44,D10L55,D12L55,D20L77,D21L77,D25L88,D30L88,D32L99,D35L99

# 嵌入式圆柱立铣刀 (CLASS END_MILL_INDEXABLE)
D17R08L66,D17R4L66,D21R08L77,D25R08L88,D25R5L88,D26R08L88,D30R5L88,D35R08L99,D35R5L99,D40R5L111,D63L200,D63R6L200,D63R08L200,D63R8L200

# 整体式球头立铣刀 (CLASS BALL_MILL_NON_INDEXABLE)
D4R2L22,D6R3L33,D8R4L44,D10R5L55,D12R6L55,D16R8L66_Solid,D20R10L77_Solid

# 嵌入式球头立铣刀 (CLASS BALL_MILL_INDEXABLE)
D16R8L66_Insert,D20R10L77_Insert,D25R12.5L88,D30R15L99

# 整体式倒角刀 (CLASS CHAMFER_MILL_NON_INDEXABLE)
DJD25R08

# 机用铰刀 (CLASS CHUCKING_REAMER)
JD4,JD5,JD6,JD8,JD10,JD12,JD16,JD20

# 整体式T型槽铣刀 (CLASS T_SLOT_MILL_NON_INDEXABLE)
TD63R4L111 (SDIA=25 LCOR=UCOR=4 FLEN=8)

# 螺旋麻花钻头 (CLASS TWIST_DRILL)
ZD3.3,ZD3.7,ZD4.3,ZD4.6,ZD5.2,ZD5.6,ZD6.8,ZD7.1,ZD7.5,ZD8.7,ZD9.1,ZD9.5,ZD10.5,ZD11.1,ZD11.5,ZD12.1,ZD13.1,ZD14.2,ZD15.7,ZD17.1,ZD17.7,ZD18.1,ZD19.7,ZD21.5,ZD23.5,ZD24.5

# 定心钻 (CLASS SPOT_DRILL)
ZXD10
"""

# 支持以空格、逗号(含中文逗号)、顿号或换行等分隔，自动解析 class
CUSTOM_TOOLS_WITH_CLASS = []
current_class = None
for line in CUSTOM_TOOLS_INPUT.split('\n'):
    line = line.strip()
    if not line:
        continue
    if line.startswith('#'):
        m = re.search(r'\(CLASS\s+([A-Z0-9_]+)\)', line)
        if m:
            current_class = m.group(1).strip()
        continue
    clean_line = line.split('#')[0].split('(')[0].strip()
    if clean_line:
        tools = [x.strip() for x in re.split(r'[ \n\r,，、]+', clean_line) if x.strip()]
        for t in tools:
            CUSTOM_TOOLS_WITH_CLASS.append((t, current_class))

CUSTOM_TOOLS = [t for t, c in CUSTOM_TOOLS_WITH_CLASS]

# 自定义刀具区域标记常量：写入与过滤必须共用同一常量，
# 防止标记字符串演进后新旧不一致，导致旧自定义区块无法被识别和清除。
CUSTOM_ZONE_TITLE = "# >>>>>> 自定义刀具（置顶置前显示区）<<<<<<"   # 写入用完整标题
NATIVE_ZONE_TITLE = "# >>>>>> 系统原厂刀具（后置显示区）<<<<<<"    # 写入用完整标题
CUSTOM_ZONE_MATCH = ">>>>>> 自定义刀具"     # 过滤用宽松子串（兼容历史变体标题）
NATIVE_ZONE_MATCH = ">>>>>> 系统原厂刀具"   # 过滤用宽松子串（兼容历史变体标题）
# 旧版历史标记：仅用于识别并清除旧区块，不再生成新内容
LEGACY_CUSTOM_ZONE_MARKER = "========== 自定义刀具区域 =========="

def get_disp_width(s):
    # 计算字符串的显示宽度。由于 NX ASCII 库要求列的物理对齐，
    # 含有中文字符的串在终端占用两列，故东亚宽字符计算为 2 宽度，其余为 1
    w = 0
    for c in str(s):
        w += 2 if unicodedata.east_asian_width(c) in 'WF' else 1
    return w

def ljust_with_disp(s, width):
    s_str = str(s)
    w = get_disp_width(s_str)
    return s_str + ' ' * max(0, width - w)

def get_jobber_length(d):
    # 根据标准直柄麻花钻标准 (类似 DIN338 / GB标准) 查找刀具总长与刃长
    # table: (最大直径限制, 总长 L1, 刃长 L2)
    table = [
        (1.06, 34, 12), (1.18, 36, 14), (1.32, 38, 16),
        (1.50, 40, 18), (1.70, 43, 20), (1.90, 46, 22),
        (2.12, 49, 24), (2.36, 53, 27), (2.65, 57, 30),
        (3.00, 61, 33), (3.35, 65, 36), (3.75, 70, 39),
        (4.25, 75, 43), (4.75, 80, 47), (5.30, 86, 52),
        (6.00, 93, 57), (6.70, 101, 63), (7.50, 109, 69),
        (8.50, 117, 75), (9.50, 125, 81), (10.60, 133, 87),
        (11.80, 142, 94), (13.20, 151, 101), (14.00, 160, 108),
        (15.00, 169, 114), (16.00, 178, 120), (17.00, 184, 125),
        (18.00, 191, 130), (19.00, 198, 135), (20.00, 205, 140),
        (21.20, 211, 145), (22.40, 218, 150), (23.60, 224, 155),
        (25.00, 230, 160), (100.0, 250, 180)
    ]
    for limit, L1, L2 in table:
        if d <= limit: return float(L1), float(L2)
    return 250.0, 180.0

def get_solid_mill_flen(dia):
    # 推断整体式硬质合金立铣刀的默认刃长，经验公式约 2~3 倍刃径 D
    if dia <= 4.0: return 12.0
    elif dia <= 6.0: return 16.0
    elif dia <= 8.0: return 20.0
    elif dia <= 10.0: return 25.0
    elif dia <= 12.0: return 30.0
    elif dia <= 16.0: return 40.0
    elif dia <= 20.0: return 50.0
    return dia * 2.0

def get_reamer_length(dia):
    # 根据 GB/T 1141 机用铰刀尺寸 (近似)
    if dia <= 2.0: return 49.0, 11.0
    elif dia <= 2.5: return 57.0, 14.0
    elif dia <= 3.0: return 61.0, 15.0
    elif dia <= 4.0: return 75.0, 19.0
    elif dia <= 5.0: return 86.0, 23.0
    elif dia <= 6.0: return 93.0, 26.0
    elif dia <= 7.0: return 109.0, 31.0
    elif dia <= 8.0: return 117.0, 33.0
    elif dia <= 9.0: return 125.0, 36.0
    elif dia <= 10.0: return 133.0, 38.0
    elif dia <= 11.0: return 142.0, 41.0
    elif dia <= 12.0: return 151.0, 44.0
    elif dia <= 14.0: return 160.0, 47.0
    elif dia <= 16.0: return 170.0, 52.0
    elif dia <= 18.0: return 182.0, 56.0
    elif dia <= 20.0: return 195.0, 60.0
    return max(195.0, dia * 10), max(60.0, dia * 3)

def get_spot_drill_length(dia):
    if dia <= 3.0: return 46.0, 12.0
    elif dia <= 4.0: return 55.0, 12.0
    elif dia <= 5.0: return 62.0, 14.0
    elif dia <= 6.0: return 66.0, 16.0
    elif dia <= 8.0: return 79.0, 21.0
    elif dia <= 10.0: return 89.0, 25.0
    elif dia <= 12.0: return 102.0, 30.0
    elif dia <= 16.0: return 115.0, 34.0
    elif dia <= 20.0: return 131.0, 40.0
    return max(131.0, dia * 5), max(40.0, dia * 2)

def get_best_fmb_holder(l_val, dia=63.0):
    # 大直径面铣飞刀 FMB 刀柄自适应匹配逻辑：
    # NX FBM 处理大型面铣刀时，如刀盘实体有效高度 HEI 被锁定为 50，超出需求的悬伸 L_val
    # 必须由 FMB 夹持器补充。BT50 标准的 FMB 刀柄其标称长度从法兰接触面起算，
    # 扣除法兰厚度及连接头等导致内部 STEP1 有效步进长度衰减，通常衰减约为 38.2mm。
    # 故有效夹持延长量 = 标称长度 - 38.2。
    standard_lengths = [45, 60, 75, 105, 120, 150, 200, 250, 300, 350, 400, 450, 500]
    best_hld = standard_lengths[-1]
    # 必须确保 50(面铣刀盘基础高度) + 刀柄有效步进1 >= 总需求长 L_val
    for nominal_l in standard_lengths:
        eff_len = nominal_l - 38.2
        if 50 + eff_len >= l_val:
            best_hld = nominal_l
            break
            
    # 根据刀盘直径推倒对应的 FMB 接口尺寸
    if dia <= 63.0:
        fmb_type = "FMB22"
    elif dia <= 80.0:
        fmb_type = "FMB27"
    elif dia <= 100.0:
        fmb_type = "FMB32"
    elif dia <= 125.0:
        fmb_type = "FMB40"
    else:
        fmb_type = "FMB60"
        
    return f"BT50{fmb_type}-{best_hld}"

def auto_infer_tool(name, explicit_class=None):
    # 核心转换引擎：
    # 接收如 "D16R8L66_Solid"、"DJD25R08" 等自定义刀名，通过正则解析切削刃径(dia)、
    # R 角、加工长(l_val)等标识，并推导出在 NX MKE 系统内该刀具的各个属性（包括
    # CLASS，类型码，切削面深度参数等），最终返回完整的 {属性键值字典} 及其 {MKE 类别}。
    tool = {
        'LIBRF': name, 'T': '02', 'ST': '1', 'UGT': '01', 'UGST': '1',
        'DESCR': f'自定义刀具 {name}', 'MATREF': 'TMC0_00007', 'MATDES': 'Coated(Ti,Al)N',
        'TLNUM': '0', 'ADJREG': '1', 'CUTCOMREG': '0', 'HLD': '', 'HLDDES': '',
        'DIA': '10.00000', 'FN': '4', 'HEI': '50.00000', 'ZOFF': '0.00000', 'DROT': '3',
        'FLEN': '25.00000', 'TAPA': '0.00000', 'TIPA': '0.00000', 'COR1': '0.00000',
        'CTH': '0', 'HOFF': '0.00000', 'ZMOUNT': '0.00000', 'RIGID': '1.0',
        'TSDIA': '', 'TSLEN': '', 'TSTLEN': '', 'RAMPANGLE': '15.00000',
        'HELICALDIA': '90.00000%T', 'MINRAMPLEN': '70.00000%T', 'MAXCUTWIDTH': '50.00000%T',
        'HLDREF': 'BT50ER16-100', 'TPREF': '', 'HA': '', 'RD': '', 'RL': '', 'SHAREF': ''
    }

    dia = 10.0
    r_val = 0.0
    hei_val = 50.0
    flen_val = 25.0

    m_mill = re.match(r'^(T?D)(\d+(?:\.\d+)?)(?:R(\d+(?:\.\d+)?))?(?:L(\d+(?:\.\d+)?))?(?:_(Solid|Insert))?$', name, re.IGNORECASE)
    m_drill = re.match(r'^(ZD|SD|ZXD|DXZ|DD|DJD|JD)(\d+(?:\.\d+)?)(?:R(\d+(?:\.\d+)?))?$', name, re.IGNORECASE)

    tool_class = explicit_class if explicit_class else "GENERIC"

    if m_mill:
        prefix, dia_str, r_str, l_str, material_type = m_mill.groups()
        if material_type: material_type = material_type.lower()
        prefix = prefix.upper()
        
        dia = float(dia_str)
        if r_str:
            if r_str.startswith('0') and '.' not in r_str and len(r_str) > 1:
                r_val = float("0." + r_str[1:])
            else:
                r_val = float(r_str)
                
        is_insert = False
        
        # 优先级：1. 刀具名自带的 _Solid / _Insert, 2. 显示声明的 Class, 3. 直径与 R角自动推导
        if material_type == 'insert':
            is_insert = True
        elif material_type == 'solid':
            is_insert = False
        elif explicit_class:
            if "NON_INDEXABLE" in explicit_class:
                is_insert = False
            elif "INDEXABLE" in explicit_class:
                is_insert = True
        else:
            if dia >= 16.0 and r_str is not None:
                # D16及以上带R角的，默认视为装刀片刀具
                is_insert = True
            elif dia >= 50.0:
                is_insert = True
        
        if r_val > 0:
            if abs(r_val - dia/2) < 0.01:
                if is_insert:
                    tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '02', '3', '01', '4'
                    tool['DESCR'] = f'嵌入式球头铣刀 {name}'
                    tool['FN'] = '2'
                    if not explicit_class: tool_class = "BALL_MILL_INDEXABLE"
                else:
                    tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '02', '3', '01', '4'
                    tool['DESCR'] = f'整体球头立铣刀 {name}'
                    tool['FN'] = '2' if dia <= 6.0 else '4'
                    if not explicit_class: tool_class = "BALL_MILL_NON_INDEXABLE"
            else:
                if is_insert:
                    tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '02', '02', '01', '01'
                    tool['DESCR'] = f'嵌入式牛鼻刀 {name}'
                    tool['FN'] = '2' if dia <= 16.0 else ('3' if dia <= 25.0 else '4')
                    if not explicit_class: tool_class = "END_MILL_INDEXABLE"
                else:
                    tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '02', '01', '01', '01'
                    tool['DESCR'] = f'整体牛鼻圆角铣刀 {name}'
                    tool['FN'] = '2' if dia <= 3.0 else ('3' if dia <= 6.0 else '4')
                    if not explicit_class: tool_class = "END_MILL_NON_INDEXABLE"
        else:
            if is_insert:
                tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '02', '02', '01', '01'
                tool['DESCR'] = f'嵌入式立铣刀 {name}'
                tool['FN'] = '2' if dia <= 16.0 else ('3' if dia <= 25.0 else '4')
                if not explicit_class: tool_class = "END_MILL_INDEXABLE"
            else:
                tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '02', '01', '01', '01'
                tool['DESCR'] = f'整体立铣刀 {name}'
                tool['FN'] = '2' if dia <= 3.0 else ('3' if dia <= 6.0 else '4')
                if not explicit_class: tool_class = "END_MILL_NON_INDEXABLE"
            
        if prefix == 'TD':
            tool['T'] = '02'
            tool['ST'] = '21'
            tool['UGT'] = '08'
            tool['UGST'] = '00'
            tool['DESCR'] = f'T型铣刀 {name}'
            tool['FN'] = '4' if dia <= 12.0 else ('6' if dia <= 25.0 else '8')
            if not explicit_class: tool_class = "T_SLOT_MILL_NON_INDEXABLE"
            is_insert = False
            
            # 填入括号中的其他标准参数 (T型槽铣刀特供)
            tool['LCOR'] = f"{r_val:.5f}" if r_val > 0 else "0.00000"
            tool['UCOR'] = f"{r_val:.5f}" if r_val > 0 else "0.00000"
            if abs(dia - 63.0) < 0.01:
                tool['SDIA'] = '25.00000'
                tool['TSDIA'] = '25.00000'
            else:
                sdia_val = max(10.0, float(int(dia * 0.4)))
                tool['SDIA'] = f"{sdia_val:.5f}"
                tool['TSDIA'] = f"{sdia_val:.5f}"
            # DEBUG 输出改为环境变量守卫，避免污染正式运行输出（NX_TOOL_BUILDER_DEBUG=1 开启）
            if os.environ.get("NX_TOOL_BUILDER_DEBUG"):
                print(f"DEBUG: T-Slot Cutter {name} assigned SDIA={tool['SDIA']}, LCOR={tool.get('LCOR', None)}")

        if l_str:
            l_val = float(l_str)
            hei_val = l_val
            if prefix != 'TD' and dia >= 50.0:
                hei_val = 50.0
                if r_val > 0.0:
                    if abs(r_val - 0.4) < 0.01 or abs(r_val - 0.8) < 0.01:
                        flen_val = 11.0
                    else:
                        flen_val = min(11.0, r_val)
                else:
                    flen_val = 11.0
                tool['HLDREF'] = get_best_fmb_holder(l_val, dia)
                tool['DESCR'] = f'面铣飞刀盘 {name}'
                tool['FN'] = '4' if dia <= 63.0 else ('5' if dia <= 80.0 else ('6' if dia <= 100.0 else '8'))
                tool_class = "END_MILL_INDEXABLE"
                tool['ST'] = '02'
                tool['UGT'] = '01'
                tool['UGST'] = '01'
            elif is_insert:
                if tool_class == "BALL_MILL_INDEXABLE":
                    flen_val = dia / 2.0
                elif r_val > 0.0:
                    if abs(r_val - 0.4) < 0.01 or abs(r_val - 0.8) < 0.01:
                        flen_val = 11.0
                    else:
                        flen_val = r_val
                else:
                    flen_val = 11.0
            elif prefix == 'TD':
                if abs(dia - 63.0) < 0.01:
                    flen_val = 8.0
                else:
                    flen_val = min(10.0, float(r_val * 2 if r_val > 0 else 5.0))
            else:
                flen_val = min(get_solid_mill_flen(dia), hei_val)
        else:
            hei_val = dia * 5.0
            if is_insert:
                if tool_class == "BALL_MILL_INDEXABLE":
                    flen_val = dia / 2.0
                elif r_val > 0.0:
                    if abs(r_val - 0.4) < 0.01 or abs(r_val - 0.8) < 0.01:
                        flen_val = 11.0
                    else:
                        flen_val = r_val
                else:
                    flen_val = 11.0
            elif prefix == 'TD':
                if abs(dia - 63.0) < 0.01:
                    flen_val = 8.0
                else:
                    flen_val = min(10.0, float(r_val * 2 if r_val > 0 else 5.0))
            else:
                flen_val = min(get_solid_mill_flen(dia), hei_val)
                
            if prefix != 'TD' and dia >= 50.0:
                l_val_proxy = dia * 5.0
                hei_val = 50.0
                tool['HLDREF'] = get_best_fmb_holder(l_val_proxy, dia)
                tool['DESCR'] = f'面铣飞刀盘 {name}'
                tool['FN'] = '4' if dia <= 63.0 else ('5' if dia <= 80.0 else ('6' if dia <= 100.0 else '8'))
                tool_class = "END_MILL_INDEXABLE"
                tool['ST'] = '02'
                tool['UGT'] = '01'
                tool['UGST'] = '01'
                if r_val > 0.0:
                    if abs(r_val - 0.4) < 0.01 or abs(r_val - 0.8) < 0.01:
                        flen_val = 11.0
                    else:
                        flen_val = min(11.0, r_val)
                else:
                    flen_val = 11.0

    elif m_drill:
        prefix, dia_str, r_str = m_drill.groups()
        prefix = prefix.upper()
        dia = float(dia_str)
        if r_str:
            if r_str.startswith('0') and '.' not in r_str and len(r_str) > 1:
                r_val = float("0." + r_str[1:])
            else:
                r_val = float(r_str)
        if prefix == 'JD':
            tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '03', '41', '02', '06'
            tool['DESCR'] = f'铰刀 {name}'
            tool['FN'] = '4' if dia <= 3.0 else ('6' if dia <= 12.5 else '8')
            tool_class = "CHUCKING_REAMER"
            L1, L2 = get_reamer_length(dia)
            # 悬伸折算：扣除约 30mm 夹持安全段（经验值，非标准推导）
            hei_val = max(L1 - 30.0, 10.0)
            flen_val = min(L2, hei_val)
            tool['TIPLEN'] = '1.00000' if dia <= 6.0 else ('1.50000' if dia <= 10.0 else '2.00000')
            tool['SDIA'] = f"{dia:.5f}"
            tool['TSDIA'] = f"{dia:.5f}"
        elif prefix in ['ZD', 'SD']:
            tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '03', '01', '02', '00'
            tool['DESCR'] = f'麻花钻 {name}'
            tool['FN'] = '2'
            tool_class = "TWIST_DRILL"
            L1, L2 = get_jobber_length(dia)
            # 悬伸折算：扣除约 30mm 夹持安全段（经验值，非标准推导）
            hei_val = max(L1 - 30.0, 10.0)
            flen_val = min(L2, hei_val)
            tool['PNTA'] = '118.00000'
            tool['PNTL'] = f"{(dia/2.0) / 1.664279:.5f}"
            tool['SDIA'] = f"{dia:.5f}"
            tool['TSDIA'] = f"{dia:.5f}"
        elif prefix in ['ZXD', 'DXZ', 'DD']:
            tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '03', '21', '02', '04'
            tool['DESCR'] = f'定心钻 {name}'
            tool['FN'] = '2'
            tool_class = "SPOT_DRILL"
            L1, L2 = get_spot_drill_length(dia)
            # 悬伸折算：扣除约 30mm 夹持安全段（经验值，非标准推导）
            hei_val = max(L1 - 30.0, 10.0)
            flen_val = min(L2, hei_val)
            tool['PNTA'] = '90.00000'
            tool['PNTL'] = f"{dia/2.0:.5f}"
            tool['SDIA'] = f"{dia:.5f}"
            tool['TSDIA'] = f"{dia:.5f}"
        elif prefix == 'DJD':
            tool['T'], tool['ST'], tool['UGT'], tool['UGST'] = '02', '5', '01', '5'
            tool['DESCR'] = f'倒角刀 {name}'
            tool_class = "CHAMFER_MILL_NON_INDEXABLE"
            tool['FN'] = '1'  # 单刃单刀粒
            L1, L2 = get_spot_drill_length(dia)
            hei_val = max(L1 - 30.0, 10.0)
            
            # 根据用户提示与图示几何关系推论：
            # 由于 NX 里自动上下两个地方都要倒圆0.8，导致：
            # 1. 底部 R 角相当于把对刀原点（最低点）往上推了 R*(sqrt(2)-1)
            # 所以 CHAMFERLEN = D/2 - R*(sqrt(2)-1)
            bottom_loss = r_val * (math.sqrt(2.0) - 1.0) if r_val > 0 else 0.0
            chamfer_len = (dia / 2.0) - bottom_loss
            # 为防止浮点数精度进位导致超出相切圆弧极限而使得NX验证抛出异常
            # 必须使用向下截断四位小数（只舍不入）进行安全避让
            # 【重构红线】以下截断不可改为 round/四舍五入，否则 NX 相切圆弧验证会抛异常
            chamfer_len = math.floor(chamfer_len * 10000) / 10000.0
            
            # 2. FLEN 是实际刀刃长度。在 CHAMFERLEN 的基础上，
            # 还要减去顶端 135° 夹角倒圆带来的有效切削刃（沿着 Z 向）的衰减量。
            # 这是从顶端虚尖角向下到切点沿 Z 轴的下沉量：R*(1 - sqrt(2)/2)
            top_loss_z = r_val * (1.0 - math.sqrt(2.0) / 2.0) if r_val > 0 else 0.0
            flen_val = chamfer_len - top_loss_z
            # 同样对 FLEN 取四位小数的向下截断
            flen_val = math.floor(flen_val * 10000) / 10000.0
            
            tool['TAPA'] = '45.00000'
            tool['CHAMFERLEN'] = f"{chamfer_len:.5f}"

    if not tool['HLDREF'].startswith('BT50FMB'):
        if dia <= 10.0: tool['HLDREF'] = 'BT50ER16-100'
        elif dia <= 13.0: tool['HLDREF'] = 'BT50ER20-100'
        elif dia <= 16.0: tool['HLDREF'] = 'BT50ER25-100'
        elif dia <= 20.0: tool['HLDREF'] = 'BT50ER32-100'
        elif dia <= 26.0: tool['HLDREF'] = 'BT50ER40-100'
        else: tool['HLDREF'] = 'BT50ASC32-105'

    tool['DIA'] = f"{dia:.5f}"
    tool['COR1'] = f"{r_val:.5f}"
    tool['HEI'] = f"{hei_val:.5f}"
    tool['FLEN'] = f"{flen_val:.5f}"

    return tool, tool_class

def dict_to_data_row(row_dict, col_names, col_widths):
    parts = [ljust_with_disp("DATA", col_widths[0])]
    for idx, cname in enumerate(col_names):
        val = row_dict.get(cname, "")
        if cname not in row_dict:
            # Handle unknown columns cleanly
            pass
        w = col_widths[idx+1]
        inner_w = w - 1
        if inner_w > 0:
            val_str = " " + ljust_with_disp(val, inner_w)
            parts.append(val_str)
        else:
            parts.append("")
    return "|".join(parts) + "|\n"

def extract_header(lines):
    # 从原始库文件行中提取文件头部注释区（Header）。
    # 头部定义：从文件第一行起，到第一个数据区块边界之前的所有行——
    # 边界包括：#CLASS 记录、自定义刀具区域标记、系统原厂区域标记及旧版历史标记。
    # 写入新库时复用该头部（含 ASCII 库名称、创建日期、单位、格式说明等），不使用硬编码。
    end_idx = len(lines)
    for idx, line in enumerate(lines):
        if (line.startswith("#CLASS ")
                or CUSTOM_ZONE_MATCH in line
                or NATIVE_ZONE_MATCH in line
                or LEGACY_CUSTOM_ZONE_MARKER in line):
            end_idx = idx
            break
    header = list(lines[:end_idx])
    # 剔除尾部混入的区域装饰线（# ====）：它属于上次生成时自定义区标题的装饰，
    # 并非原库头部内容。若不剔除，每次运行都会向头部累积一行装饰线，破坏幂等性。
    # 原库头部自身的 #==== / # ---- 等注释线不含 "# <空格>=" 前缀，不受影响。
    while header and header[-1].startswith("# ===="):
        header.pop()
    return header, lines[end_idx:]

def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("🚀 开始执行 NX FBM 自动刀库构建与注入器 (nx_tool_builder) ...")
    
    input_file = sys.argv[1] if len(sys.argv) > 1 else "tool_database.dat"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "tool_database.dat"
    
    if not os.path.exists(input_file):
        print(f"❌ 找不到刀库文件: {input_file}，请确保脚本在包含该文件的目录下运行。")
        return

    try:
        # 统一以 UTF-8 编码读取，保证含中文头部的库文件正确解析
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except PermissionError:
        print(f"❌ 无权限读取 {input_file}：文件被其他程序占用或为只读，请关闭 NX/编辑器等占用程序后重试。")
        return
    except UnicodeDecodeError as e:
        print(f"❌ {input_file} 不是有效的 UTF-8 文本文件: {e}")
        return
    except OSError as e:
        print(f"❌ 无法读取 {input_file}: {e}")
        return

    # 提取原库文件头（ASCII 库名称、创建日期、单位、格式说明等），
    # 写入新库时直接复用该头部，不使用硬编码内容
    header_lines, body_lines = extract_header(lines)
    if not header_lines:
        print("⚠️ 警告: 未能从原库提取到文件头（Header），新库将不含头部说明区。")

    # First, collect target classes and formatting
    class_formats = {}
    
    i = 0
    current_class = ""
    while i < len(body_lines):
        line = body_lines[i]
        if line.startswith("#CLASS "):
            current_class = line.strip().split()[1]
        elif line.startswith("FORMAT") and current_class:
            words = line.strip().split()
            col_names = words[1:] if len(words) > 1 else []
            class_formats[current_class] = {"format_line": line, "col_names": col_names}
        elif line.startswith("#----") and current_class in class_formats and "col_widths" not in class_formats[current_class]:
            if '+' in line:
                parts = line.rstrip('\n').split('+')
                class_formats[current_class]["col_widths"] = [len(p) for p in parts]
            else:
                # Default fallback widths if not explicitly formatted with +
                names = class_formats[current_class]["col_names"]
                class_formats[current_class]["col_widths"] = [6] + [16] * len(names)
            class_formats[current_class]["separator_line"] = line
        i += 1

    # Extract all existing tools
    tools_by_class = {}
    for name, explicit_class in CUSTOM_TOOLS_WITH_CLASS:
        t_dict, t_class = auto_infer_tool(name, explicit_class)
        if t_class not in tools_by_class:
            tools_by_class[t_class] = []
        tools_by_class[t_class].append((name, t_dict))

    # Now filter original lines, remove old custom tool zone, and remove custom tools
    filtered_lines = []
    existing_custom_dicts = {}
    
    in_custom_zone = False
    
    i = 0
    while i < len(body_lines):
        line = body_lines[i]

        # Check boundaries
        if CUSTOM_ZONE_MATCH in line or LEGACY_CUSTOM_ZONE_MARKER in line:
            in_custom_zone = True
            if len(filtered_lines) > 0 and filtered_lines[-1].startswith("# ===="):
                filtered_lines.pop()
            if i + 1 < len(body_lines) and body_lines[i+1].startswith("# ===="):
                i += 1
            i += 1
            if i < len(body_lines) and body_lines[i].strip() == "":
                i += 1
            continue

        if NATIVE_ZONE_MATCH in line:
            in_custom_zone = False
            if len(filtered_lines) > 0 and filtered_lines[-1].startswith("# ===="):
                filtered_lines.pop()
            if i + 1 < len(body_lines) and body_lines[i+1].startswith("# ===="):
                i += 1
            i += 1
            if i < len(body_lines) and body_lines[i].strip() == "":
                i += 1
            continue

        if line.startswith("#CLASS "):
            current_class = line.strip().split()[1]
        
        if line.startswith("FORMAT"):
            words = line.strip().split()
            current_col_names = words[1:] if len(words) > 1 else []
        
        is_custom_data_line = False
        if line.startswith("DATA   |"):
            d_parts = line.rstrip('\n').split('|')[1:]
            row_dict = {}
            for idx, cname in enumerate(current_col_names):
                if idx < len(d_parts):
                    row_dict[cname] = d_parts[idx].strip()
            
            librf = row_dict.get("LIBRF", "")
            if librf in CUSTOM_TOOLS:
                existing_custom_dicts[librf] = row_dict
                is_custom_data_line = True
                
        if in_custom_zone or is_custom_data_line:
            i += 1
            continue
            
        filtered_lines.append(line)
        i += 1

    # 原生库区块 = 过滤后从第一个 #CLASS 起的剩余内容（已剔除旧自定义区）
    native_insert_idx = 0
    for idx, line in enumerate(filtered_lines):
        if line.startswith("#CLASS "):
            native_insert_idx = idx
            break
    native_lines = filtered_lines[native_insert_idx:]

    # 使用从原库提取的文件头作为新库头部（含 ASCII 库名、创建日期、单位、格式说明等）
    # 不再通过 insert_idx 间接推导，逻辑更清晰且避免误判
    custom_zone_lines = []
    custom_zone_lines.append("# ==================================================\n")
    custom_zone_lines.append(CUSTOM_ZONE_TITLE + "\n")
    custom_zone_lines.append("# ==================================================\n\n")
    
    for t_class, customs in tools_by_class.items():
        if not customs: continue
        
        fmt_info = class_formats.get(t_class)
        if not fmt_info:
            fallback_class = t_class.replace("INDEXABLE", "NON_INDEXABLE")
            if fallback_class in class_formats:
                fmt_info = class_formats[fallback_class]
            elif t_class.replace("NON_INDEXABLE", "INDEXABLE") in class_formats:
                fmt_info = class_formats[t_class.replace("NON_INDEXABLE", "INDEXABLE")]
            else:
                for k in class_formats.keys():
                    if "MILL" in k and "MILL" in t_class:
                        fmt_info = class_formats[k]
                        break
            if not fmt_info:
                print(f"⚠️ 警告: 找不到 {t_class} 及其降级类型的 FORMAT 信息，跳过。")
                continue
            
        custom_zone_lines.append(f"#CLASS {t_class}\n")
        custom_zone_lines.append(fmt_info["format_line"])
        custom_zone_lines.append(fmt_info["separator_line"])
        
        class_rows = []
        for c_name, c_dict_inferred in customs:
            if c_name in existing_custom_dicts:
                row_dict = existing_custom_dicts[c_name]
                # Force override all inferred properties to ensure physics and classification are correct
                for key in c_dict_inferred:
                    row_dict[key] = c_dict_inferred[key]
            else:
                row_dict = c_dict_inferred
                
            # 强刷物理防线
            try:
                flen = float(row_dict.get("FLEN", "0") or "0")
                hei = float(row_dict.get("HEI", "0") or "0")
                if flen > hei and hei > 0:
                    row_dict["FLEN"] = f"{hei:.5f}"
            except ValueError:
                pass
                
            dia = 0.0
            try:
                dia = float(row_dict.get("DIA", "0") or "0")
            except ValueError:
                pass
                
            class_rows.append((dia, row_dict))
            
        class_rows.sort(key=lambda x: x[0], reverse=True)
        
        for dia, row_dict in class_rows:
            custom_zone_lines.append(dict_to_data_row(row_dict, fmt_info["col_names"], fmt_info["col_widths"]))
        
        custom_zone_lines.append("#END_DATA\n\n")

    custom_zone_lines.append("# ==================================================\n")
    custom_zone_lines.append(NATIVE_ZONE_TITLE + "\n")
    custom_zone_lines.append("# ==================================================\n\n")

    out_lines = header_lines + custom_zone_lines + native_lines

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(out_lines)
        print(f"✅ 生成 {output_file} 成功！")
        print(f"✅ 提取或注入了 {len(CUSTOM_TOOLS)} 把自定义刀具，集中建档于顶部：# >>>>>> 自定义刀具（置顶置前显示区）<<<<<<")
    except PermissionError:
        print(f"❌ 无权限写入 {output_file}：文件可能正在被 NX 或其他程序打开，请关闭后重试。")
        return
    except OSError as e:
        print(f"❌ 写入文件失败 {output_file}: {e}")
        return
    
    # 自动对齐处理
    print("🚀 开始自动对齐格式...")
    try:
        align_dat_file(output_file)
        print(f"✨ 格式对齐完成！已保存回 {output_file}")
    except Exception as e:
        print(f"⚠️ 格式对齐执行失败: {str(e)}")

def align_dat_file(filepath):
    # 复用模块级显示宽度工具（get_disp_width / ljust_with_disp），
    # 避免在函数内部重复实现同样的东亚宽度计算逻辑
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except PermissionError:
        raise OSError(f"无权限读取 {filepath}：文件可能被其他程序占用") from None
    except OSError as e:
        raise OSError(f"无法读取对齐目标文件 {filepath}") from e
        
    out_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('FORMAT '):
            format_line = line
            out_lines.append(format_line)
            format_cols = format_line.strip().split()[1:] 
            
            i += 1
            if i >= len(lines): break
            sep_line = lines[i]
            out_lines.append(sep_line)
            
            i += 1
            data_start_idx = i
            data_lines = []
            while i < len(lines) and lines[i].startswith('DATA '):
                data_lines.append(lines[i])
                i += 1
            
            col_widths = [len(c) for c in format_cols]
            
            parsed_data = []
            for d in data_lines:
                parts = d.split('|')
                vals = [p.strip() for p in parts[1:]]
                vals = vals[:len(format_cols)]
                while len(vals) < len(format_cols):
                    vals.append("")
                parsed_data.append(vals)
                for c_idx, val in enumerate(vals):
                    dl = get_disp_width(val)
                    if dl > col_widths[c_idx]:
                        col_widths[c_idx] = dl
            
            col_widths = [w + 1 for w in col_widths]
            
            fmt_str = "FORMAT   "
            for c_idx, col_name in enumerate(format_cols):
                fmt_str += ljust_with_disp(col_name, col_widths[c_idx]) + " "
            out_lines[-2] = fmt_str.rstrip() + "\n"
            
            sep_str = "#--------"
            for c_idx in range(len(format_cols)):
                sep_str += "+" + "-" * (col_widths[c_idx])
            out_lines[-1] = sep_str + "\n"
            
            end_pipe = ""
            for vals in parsed_data:
                d_str = "DATA   "
                for c_idx, val in enumerate(vals):
                    d_str += "| " + ljust_with_disp(val, col_widths[c_idx] - 1)
                out_lines.append(d_str.rstrip() + "\n")
        else:
            out_lines.append(line)
            i += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(out_lines)

if __name__ == "__main__":
    main()
