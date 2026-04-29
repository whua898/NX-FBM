# FBM Generator Core - 通用框架

**版本**: v1.0  
**适用范围**: NX12/NX2512+  
**状态**: 生产就绪

---

## 项目结构

```
NX12MKE/
├── fbm_generator_core.py      # 核心框架（数据与序列化分离）
├── rules_data_nx12.py         # NX12 规则数据定义
├── generate_mke_nx12.py       # NX12 生成器入口
├── modify_mke_v12.py          # 旧版脚本（保留用于参考）
│
├── docs/
│   └── guides/
│       └── FBM_Development_Guide.md  # 通用开发规范
│
├── machining_knowledge.xml    # 基准知识库（只读）
└── machining_knowledge_v12.xml # 生成的 NX12 规则库
```

---

## 架构设计

### 核心理念：数据与序列化分离

**传统方式**（modify_mke_v12.py）：
```python
# ❌ 数据定义和 XML 构建混在一起
def create_rules():
    rules = []
    # ... 构建数据结构
    
def build_xml(rules):
    # ... 直接操作 XML ElementTree
```

**新架构**（fbm_generator_core.py）：
```python
# ✅ 数据定义独立
@dataclass
class MachiningRule:
    name: str
    operation_class: str
    # ...

# ✅ XML 构建通过适配器隔离
class SchemaAdapter:
    def build_rule_element(self, rule):
        # 版本特定的 XML 构建逻辑

# ✅ 生成器协调两者
class FBMGenerator:
    def __init__(self, adapter: SchemaAdapter):
        self.adapter = adapter
```

### 优势

1. **可维护性**：修改规则数据不需要触碰 XML 构建逻辑
2. **可扩展性**：新增 NX2512 支持只需创建 `NX2512SchemaAdapter`
3. **可测试性**：规则数据可以独立单元测试
4. **复用性**：`fbm_generator_core.py` 可在多个项目中共享

---

## 快速开始

### 1. 生成 NX12 规则库

```bash
python generate_mke_nx12.py
```

输出：
- `machining_knowledge_v12.xml`

### 2. 自定义规则

编辑 `rules_data_nx12.py`，添加新规则：

```python
from fbm_generator_core import MachiningRule, RuleLibrary

my_rule = MachiningRule(
    name="My_Custom_Rule",
    operation_class="mill_planar.FLOOR_WALL",
    priority=1500,
    mwf="SURFACE_PLANAR_RECTANGULAR",
    lwf="BLANK",
    tool_class="FACE_MILL_INDEXABLE",
    criteria=[("mwf.DEPTH", ">=", "5.0")],
    tool_attrs=[("tool.Diameter", ">=", "20.0")]
)
```

### 3. 验证规则冲突

```python
from fbm_generator_core import FBMGenerator, NX12SchemaAdapter
from rules_data_nx12 import create_nx12_rules

rules = create_nx12_rules()
adapter = NX12SchemaAdapter()
generator = FBMGenerator(adapter)

errors = generator.validate_rules(rules)
for error in errors:
    print(error)
```

### 4. 回归测试

```python
from fbm_generator_core import simulate_mke_matching

test_features = [
    {'DIAMETER_1': 10.5, 'DEPTH': 20.0},
    {'DIAMETER_1': 5.0, 'DEPTH': 15.0},
]

all_rules = extract_all_rules(rules)  # 需要自己实现
results = simulate_mke_matching(test_features, all_rules)

for result in results:
    print(f"{result['feature']} → {result['matched_rule']}")
```

---

## 适配新版本（NX2512 示例）

### 步骤 1：创建 Schema 适配器

```python
# fbm_generator_nx2512.py
from fbm_generator_core import SchemaAdapter, NX12SchemaAdapter

class NX2512SchemaAdapter(NX12SchemaAdapter):
    """NX2512 XML Schema 适配器"""
    
    def get_root_external_id(self) -> str:
        return "OOTB_EnvironmentLibraryEnvRuleRoot_NX2512"  # 假设变化
    
    def build_rule_element(self, rule, objects_elem, parent_lib_id, id_counter):
        # 调用父类方法
        rule_elem, id_counter = super().build_rule_element(
            rule, objects_elem, parent_lib_id, id_counter
        )
        
        # 添加 NX2512 特有的标签
        ET.SubElement(rule_elem, 'MultiAxisSupport').text = "true"
        
        return rule_elem, id_counter
```

### 步骤 2：创建规则数据

```python
# rules_data_nx2512.py
from fbm_generator_core import MachiningRule, RuleLibrary

def create_nx2512_rules():
    # 可能包含多轴加工规则
    multi_axis_rule = MachiningRule(
        name="5_Axis_Blisk_Rough",
        operation_class="mill_multiaxis.VARIABLE_CONTOUR",
        # ...
    )
    return [multi_axis_rule]
```

### 步骤 3：创建生成器入口

```python
# generate_mke_nx2512.py
from fbm_generator_core import FBMGenerator
from fbm_generator_nx2512 import NX2512SchemaAdapter
from rules_data_nx2512 import create_nx2512_rules

adapter = NX2512SchemaAdapter()
generator = FBMGenerator(adapter)
rules = create_nx2512_rules()

generator.generate_xml(
    input_file='machining_knowledge_nx2512.xml',
    output_file='machining_knowledge_v2512.xml',
    rules=rules
)
```

---

## 常见问题

### Q1: 为什么保留 modify_mke_v12.py？

**A**: 作为历史参考，展示 V12 成功经验。新项目应使用新架构。

### Q2: 如何调试 Conditions 格式错误？

**A**: 打印 Conditions 文本进行人工检查：

```python
rule = MachiningRule(...)
adapter = NX12SchemaAdapter()
conditions_text = adapter._build_conditions_text(rule)
print(repr(conditions_text))
```

预期输出应包含：
```
"REM Application Criteria\n\nmwf.DIAMETER_1 >= 3.0\n\n$$ Rule rejected..."
```

### Q3: 规则被静默拒绝怎么办？

**A**: 按以下顺序排查：
1. 检查 Conditions 四区块格式（特别是空行和 `$$` 标记）
2. 检查 Application Criteria 是否混入赋值语句
3. 检查刀具库是否有匹配的刀具规格
4. 检查优先级是否被更高优先级规则覆盖

### Q4: 如何迁移现有规则到新架构？

**A**: 
1. 从 `modify_mke_v12.py` 复制规则数据到 `rules_data_nx12.py`
2. 使用 `MachiningRule` 和 `RuleLibrary` 重构数据结构
3. 运行 `generate_mke_nx12.py` 生成 XML
4. 在 NX MKE 中验证结果

---

## 参考资料

- [FBM 开发通用规范](docs/guides/FBM_Development_Guide.md)
- [NX12MKE 详细手册](NX12MKE.md)
- [AGENTS.md](AGENTS.md) - AI 行为准则

---

**维护者**: AI CAM Engineering Team  
**最后更新**: 2026-04-29
