# FBM 开发通用规范 (Feature-Based Machining)

**版本**: v1.0 | **适用范围**: NX12/NX2512+ | **状态**: 跨版本真理来源

---

## 目录

- [1. MKE 规则语言核心原理](#1-mke-规则语言核心原理)
- [2. 规则库架构设计原则](#2-规则库架构设计原则)
- [3. 命名与优先级规范](#3-命名与优先级规范)
- [4. XML Schema 结构标准](#4-xml-schema-结构标准)
- [5. 自动化生成器设计规范](#5-自动化生成器设计规范)
- [6. 质量控制与测试策略](#6-质量控制与测试策略)
- [7. 常见陷阱与避坑指南](#7-常见陷阱与避坑指南)

---

## 1. MKE 规则语言核心原理

### 1.1 声明式条件过滤器

> **核心定义**：MKE 规则语言不是脚本语言，而是"声明式条件过滤器 + 有限的工序属性赋值"。

**关键约束**：
- ❌ **禁止**：`If/Then/Else/End If` 等脚本语句、任何赋值语句（含 `Rule_Validity = FALSE`）
- ✅ **允许**：形如 `mwf.DIAMETER_1 >= 3.0` 的条件表达式（布尔逻辑）

### 1.2 Conditions 四区块格式（强制标准）

```text
REM Application Criteria
<只允许布尔条件，每行一个条件；多行自动 AND>

$$ Rule rejected because condition FALSE

REM Tool Attributes
<以筛选条件为主；可对部分 tool.* 属性赋值>

REM Less Worked Feature Attributes
<可空>

REM Operation Attributes
<允许 oper.* 赋值>
```

**⚠️ 铁律**：
1. 每个 REM 标题前后必须有明确空行
2. `$$ Rule rejected because condition FALSE` 必须保留，作为区块分隔符
3. Application Criteria **严禁**混入赋值语句（会导致规则无声拒绝）
4. Operation Attributes 是**唯一**允许 `oper.*` 赋值的地方

### 1.3 规则匹配流程

```
特征识别 → 遍历规则库（按优先级降序）
    ↓
检查 Application Criteria（布尔条件）
    ↓ 条件为 FALSE
规则被拒绝（静默跳过）
    ↓ 条件为 TRUE
检查 Tool Attributes（刀具筛选）
    ↓ 无匹配刀具
规则被拒绝
    ↓ 有匹配刀具
应用 Operation Attributes（工序属性赋值）
    ↓
生成 NC 工序
```

---

## 2. 规则库架构设计原则

### 2.1 层级结构设计

**推荐结构**（板类零件示例）：
```
Factory_Plate_General (父库)
├─ 01_Face_Milling (面加工库)
├─ 02_Pocket_Slot (口袋与槽库)
├─ 03_Hole_Making (孔加工库)
│   ├─ 3.1_Spot (定位钻)
│   ├─ 3.2_Thread_Bottom (螺纹底孔)
│   ├─ 3.3_Thread_Through (螺纹过孔)
│   ├─ 3.4_Pin_Hole (销孔)
│   │   ├─ Pre-Drill (预钻)
│   │   └─ Ream (铰孔)
│   └─ 3.5_Large_Hole (大孔)
└─ 04_Chamfer (倒角库)
```

**设计原则**：
- **模块化**：每个工艺类型独立成库，便于维护和扩展
- **层次化**：子库嵌套在父库中，形成清晰的树状结构
- **可扩展**：新增工艺类型时只需添加新子库，不影响现有规则

### 2.2 互斥性设计

**直径窗口互斥示例**（螺纹底孔 vs 过孔）：
- 螺纹底孔 D8.7：`[8.10, 8.98]`
- 螺纹过孔 D9.0：`[8.98, 9.02]`

**关键技巧**：
- 边界值精确到小数点后两位
- 相邻窗口使用相同边界值实现无缝衔接
- 避免重叠导致"双命中"冲突

### 2.3 工序链路设计

利用 `lwf.MACHINING_RULE` 确保工序顺序：
- 铰孔（Ream）的 LWF = `STEP1HOLE`（预钻孔输出）
- 预钻孔的 LWF = `BLANK`（毛坯输入）

**效果**：系统自动识别依赖关系，按正确顺序生成工序链。

---

## 3. 命名与优先级规范

### 3.1 统一命名模板

**格式**：`模块_工艺_特征_窗口_刀具_R版本`

**示例**：
- `HM_Drill_ThreadBottom_D8p10-8p98_T8p7_R01`
- `FM_Face_Top_A400-200k_D63_R01`
- `HM_Ream_Pin_D9p98-10p02_T10_R01`

**简写规则**（用于规则树显示）：
- `1.1_Face_Top_Rough`
- `3.2_Thread_Bottom_D8p7`
- `3.4_Pin_Pre_D10`

### 3.2 优先级分带策略

| 模块 | 优先级范围 | 说明 |
|------|-----------|------|
| Face | 1200~1299 | 面加工 |
| Pocket_Slot | 2400~2499 | 型腔与槽 |
| Hole_Making - Spot | 1100 | 定位钻（最高优先级） |
| Hole_Making - Thread Bottom | 2200~2299 | 螺纹底孔 |
| Hole_Making - Thread Through | 2300~2399 | 螺纹过孔 |
| Hole_Making - Pin Pre | 2100~2199 | 销孔预钻 |
| Hole_Making - Pin Ream | 3100~3199 | 销孔铰孔 |
| Hole_Making - Large Hole | 3200~3299 | 大孔铣削 |
| Chamfer | 3300~3399 | 倒角 |
| Fallback_ManualCheck | 100 | 最低优先级兜底规则 |

**设计原则**：
- **数值越大越先尝试**：高优先级规则优先匹配
- **预留间隔**：每个分带预留 100 个优先级空间，便于插入新规则
- **兜底策略**：最低优先级规则捕获未匹配特征，触发人工检查

---

## 4. XML Schema 结构标准

### 4.1 核心元素定义

```xml
<MachiningRuleLibrary ExternalId="Factory_Plate_General_Lib">
  <NodeInfo>
    <Id>1001</Id>
  </NodeInfo>
  <name>Factory_Plate_General</name>
  <comment>板类零件通用加工规则库</comment>
  <collections>
    <item>OOTB_EnvironmentLibraryEnvRuleRoot</item>
  </collections>
  <children>
    <item>Factory_Plate_01_Face_Milling</item>
    <item>Factory_Plate_02_Pocket_Slot</item>
    <!-- ... -->
  </children>
</MachiningRuleLibrary>

<MachiningRule ExternalId="Factory_Plate_01_Face_Milling_1.1_Face_Top_Rough">
  <NodeInfo>
    <Id>1002</Id>
  </NodeInfo>
  <name>1.1_Face_Top_Rough</name>
  <collections>
    <item>Factory_Plate_01_Face_Milling</item>
  </collections>
  <Conditions>
    REM Application Criteria
    mwf.DEPTH &gt;= 1.0
    
    $$ Rule rejected because condition FALSE
    
    REM Tool Attributes
    tool.Diameter &gt;= 40.0
    tool.Diameter &lt;= 80.0
    
    REM Less Worked Feature Attributes
    
    REM Operation Attributes
    oper.name = "1.1_Face_Top_Rough"
  </Conditions>
  <Input>
    <item>feature.BLANK</item>
  </Input>
  <OperationClass>mill_planar.FLOOR_WALL</OperationClass>
  <Output>
    <item>feature.SURFACE_PLANAR_RECTANGULAR</item>
  </Output>
  <Priority>1210</Priority>
  <Resources>
    <item>tool.FACE_MILL_INDEXABLE</item>
  </Resources>
  <comment>顶面粗加工</comment>
  <type>Composed</type>
</MachiningRule>
```

### 4.2 关键标签说明

| 标签 | 用途 | 必填 | 说明 |
|------|------|------|------|
| `ExternalId` | 全局唯一标识符 | ✅ | 格式：`{ParentLib}_{RuleName}` |
| `NodeInfo/Id` | 内部节点 ID | ✅ | 递增整数，不能重复 |
| `Conditions` | 规则条件文本块 | ✅ | 严格遵循四区块格式 |
| `Input` | LWF 特征列表 | ✅ | 通常为 `feature.BLANK` 或上游输出 |
| `OperationClass` | 工序类型 | ✅ | 决定刀具类别和参数模板 |
| `Output` | MWF 特征列表 | ✅ | 当前工序生成的特征 |
| `Priority` | 优先级数值 | ✅ | 数值越大越先尝试 |
| `Resources` | 刀具/刀柄资源 | ✅ | 格式：`tool.{ToolClass}` |

### 4.3 ⚠️ V12 成功经验（永久遵守）

**核心铁律**：
1. **不要生成 DecorationObjects/History 标签**（Gemini V12 验证成功）
2. **Conditions 四区块格式不可改**（官方文档第 47-52 页）
3. **Application Criteria 只能写布尔条件**（严禁赋值语句）
4. **Input/Output 顺序与原生一致**（Input → OperationClass → Output）
5. **直接构建 XML，不依赖克隆**（避免旧 ExternalId 引用残留）

**7 次失败教训总结**：
| 版本 | 问题 | 后果 | 解决方案 |
|------|------|------|----------|
| V5/V6 | 缺失 DecorationObjects/History | "is not valid class" | V7 克隆保留标签 |
| V7 初版 | DecorationObjects 含旧 OOTB ExternalId | 规则详情空白 | 清空 DecorationObjects 内容 |
| V7 修复版 | 保留空标签但 NX 仍报错 | 解析错位 | **V12：完全不生成这两个标签** |
| 所有版本 | Conditions 格式不规范 | 规则无声拒绝 | **严格按官方四区块格式** |
| 所有版本 | Application Criteria 混入赋值 | 规则被拒绝 | **赋值移至 Operation Attributes** |

---

## 5. 自动化生成器设计规范

### 5.1 数据与序列化分离架构

**核心原则**：将规则数据定义（Rules Data）与 XML 序列化（XML Writer）解耦。

**推荐架构**：
```python
# fbm_generator_core.py (通用框架)

class MachiningRule:
    """规则数据结构"""
    name: str
    operation_class: str
    priority: int
    mwf: str
    lwf: str
    tool_class: str
    criteria: List[Tuple[str, str, str]]  # (field, operator, value)
    tool_attrs: List[Tuple[str, str, str]]

class RuleLibrary:
    """规则库数据结构"""
    name: str
    external_id: str
    description: str
    children: List[Union[MachiningRule, 'RuleLibrary']]

class FBMGenerator:
    """通用生成器（适配不同版本 XML Schema）"""
    
    def __init__(self, schema_version: str):
        self.schema_version = schema_version
    
    def build_xml(self, rules: List[RuleLibrary]) -> ET.ElementTree:
        """根据规则数据构建 XML 树"""
        # 版本特定的 XML 构建逻辑
        pass
    
    def validate_rules(self, rules: List[RuleLibrary]) -> List[str]:
        """验证规则冲突和完整性"""
        # 检查优先级重复、直径窗口重叠等
        pass
```

### 5.2 批量生成器模式

针对重复性高的规则（如螺纹底孔、销孔），使用循环逻辑自动生成：

```python
def generate_thread_bottom_rules():
    """批量生成螺纹底孔规则"""
    thread_bottoms = [
        ("D3p4", 2210, 3.4, 3.10, 3.50),
        ("D4p3", 2220, 4.3, 4.10, 4.50),
        # ...
    ]
    
    rules = []
    for name_suffix, priority, d, d_min, d_max in thread_bottoms:
        rules.append(MachiningRule(
            name=f"3.2_Thread_Bottom_{name_suffix}",
            priority=priority,
            operation_class="hole_making.DRILLING",
            mwf="STEP1HOLE",
            lwf="BLANK",
            tool_class="TWIST_DRILL",
            criteria=[("mwf.DIAMETER_1", ">=", str(d_min)),
                      ("mwf.DIAMETER_1", "<=", str(d_max))],
            tool_attrs=[("tool.Diameter", ">=", str(round(d-0.05, 2))),
                        ("tool.Diameter", "<=", str(round(d+0.05, 2)))]
        ))
    return rules
```

### 5.3 冲突检测机制

在写入前执行以下检查：
1. **优先级重复检测**：同一 `OperationClass` 下不能有相同优先级
2. **直径窗口重叠检测**：相邻规则的直径范围不能重叠
3. **LWF 依赖链检测**：确保工序链路完整（如铰孔必须有预钻孔前置）

---

## 6. 质量控制与测试策略

### 6.1 回归测试脚本

**功能**：模拟 MKE 匹配过程，验证规则覆盖率和冲突情况。

```python
def simulate_mke_matching(test_features: List[Dict], rules: List[MachiningRule]):
    """模拟 MKE 规则匹配"""
    results = []
    for feature in test_features:
        matched_rules = []
        for rule in sorted(rules, key=lambda r: r.priority, reverse=True):
            if check_criteria(feature, rule.criteria):
                if check_tool_availability(rule.tool_attrs):
                    matched_rules.append(rule)
                    break  # 最高优先级规则胜出
        
        results.append({
            'feature': feature,
            'matched_rule': matched_rules[0] if matched_rules else None,
            'status': 'MATCHED' if matched_rules else 'UNMATCHED'
        })
    
    return results
```

### 6.2 发布门槛

**Go 条件**：
- ✅ 最小回归全通过
- ✅ 关键特征零漏加工
- ✅ 规则命名可追溯
- ✅ 无"双命中"冲突

**No-Go 条件**：
- ❌ 存在双命中未解
- ❌ 关键工序缺失
- ❌ 无刀具匹配未闭环
- ❌ 直径窗口重叠

### 6.3 测试用例设计

**典型测试特征**：
| 特征类型 | 测试参数 | 预期规则 |
|---------|---------|---------|
| 螺纹底孔 M10 | Diameter=10.5mm, Depth=20mm | 3.2_Thread_Bottom_D10p5 |
| 销孔 Ø10 | Diameter=10.0mm, Depth=15mm | 3.4_Pin_Pre_D10 → 3.4_Pin_Ream_D10 |
| 矩形型腔 | Width=50mm, Depth=10mm | 2.1_Pocket_Rough_General → 2.2_Pocket_Finish_Wall |
| 大孔 Ø25 | Diameter=25.0mm, Depth=30mm | 3.5_Large_Hole_Mill |

---

## 7. 常见陷阱与避坑指南

### 7.1 编码问题

**PowerShell UTF-8 BOM 陷阱**：
- ❌ 错误：使用默认编码保存 `.ps1` 脚本
- ✅ 正确：使用 UTF-8 BOM 编码（Notepad++ → Encoding → UTF-8-BOM）

**Python 文件读写**：
```python
# ✅ 正确做法
with open('file.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# ❌ 错误做法（可能导致中文乱码）
with open('file.xml', 'r') as f:
    content = f.read()
```

### 7.2 XML 解析陷阱

**Namespace 处理**：
```python
# ✅ 正确：注册 namespace
ET.register_namespace('', 'http://www.siemens.com/nx/mke')
tree = ET.parse('machining_knowledge.xml')

# ❌ 错误：忽略 namespace 导致查找失败
root = tree.getroot()
rules = root.findall('MachiningRule')  # 返回空列表
```

**特殊字符转义**：
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`

### 7.3 规则无声拒绝排查

**症状**：规则在 MKE 编辑器中显示正常，但实际加工时未被触发。

**排查步骤**：
1. 检查 `Conditions` 文本是否符合四区块格式（特别是空行和 `$$` 标记）
2. 检查 Application Criteria 是否混入赋值语句
3. 检查刀具库是否有匹配的刀具规格
4. 检查优先级是否被更高优先级规则覆盖

**调试技巧**：
```python
# 打印 Conditions 文本块进行人工检查
print(repr(rule.conditions_text))
# 预期输出应包含：
# "REM Application Criteria\n\nmwf.DIAMETER_1 >= 3.0\n\n$$ Rule rejected..."
```

### 7.4 版本兼容性

**NX12 vs NX2512 差异**：
- XML Schema 可能有细微变化（如新增标签、属性顺序调整）
- 建议：在 `fbm_generator_core.py` 中使用策略模式隔离版本差异

```python
class NX12SchemaAdapter(SchemaAdapter):
    def build_rule_element(self, rule: MachiningRule) -> ET.Element:
        # NX12 特定的 XML 构建逻辑
        pass

class NX2512SchemaAdapter(SchemaAdapter):
    def build_rule_element(self, rule: MachiningRule) -> ET.Element:
        # NX2512 特定的 XML 构建逻辑（可能支持多轴参数）
        pass
```

---

## 附录：快速参考

### A. Conditions 模板

```text
REM Application Criteria
mwf.DIAMETER_1 >= 3.0
mwf.DIAMETER_1 <= 22.0

$$ Rule rejected because condition FALSE

REM Tool Attributes
tool.Diameter >= 10.0
tool.Diameter <= 16.0

REM Less Worked Feature Attributes

REM Operation Attributes
oper.name = "Rule_Name"
```

### B. 常用 OperationClass

| 工艺类型 | OperationClass | 对应刀具类型 |
|---------|---------------|-------------|
| 面铣 | `mill_planar.FLOOR_WALL` | FACE_MILL_INDEXABLE |
| 型腔粗加工 | `mill_contour.CAVITY_MILL` | END_MILL_NON_INDEXABLE |
| 钻孔 | `hole_making.DRILLING` | TWIST_DRILL |
| 铰孔 | `hole_making.DRILLING` | CHUCKING_REAMER |
| 孔口倒角 | `hole_making.HOLE_CHAMFER_MILLING` | CHAMFER_MILL_NON_INDEXABLE |
| 槽加工 | `mill_planar.GROOVE_MILLING` | END_MILL_NON_INDEXABLE |

### C. 常用 MWF/LWF 特征

| 特征名称 | 说明 | 典型应用场景 |
|---------|------|------------|
| `BLANK` | 毛坯 | 第一道工序的 LWF |
| `STEP1HOLE` | 单步孔 | 钻孔输出 / 铰孔输入 |
| `STEP2HOLE` | 两步孔 | 铰孔输出 |
| `SURFACE_PLANAR_RECTANGULAR` | 矩形平面 | 面加工 MWF |
| `POCKET_RECTANGULAR_STRAIGHT` | 矩形型腔 | 型腔加工 MWF |
| `SLOT_RECTANGULAR` | 矩形槽 | 槽加工 MWF |

---

**文档维护者**: AI CAM Engineering Team  
**最后更新**: 2026-04-29  
**反馈渠道**: GitHub Issues
