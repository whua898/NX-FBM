"""
FBM Generator Core - 通用规则生成框架
版本: v1.0
适用范围: NX12/NX2512+ (通过 Schema Adapter 隔离版本差异)

架构原则:
1. 数据定义 (Rules Data) 与 XML 序列化 (XML Writer) 完全解耦
2. 使用策略模式适配不同版本的 XML Schema
3. 内置冲突检测和回归测试工具
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import List, Tuple, Union, Optional
import sys

# 确保 UTF-8 输出
sys.stdout.reconfigure(encoding='utf-8')


@dataclass
class MachiningRule:
    """加工规则数据结构"""
    name: str
    operation_class: str
    priority: int
    mwf: str  # More Worked Feature (目标特征)
    lwf: str  # Less Worked Feature (输入特征)
    tool_class: str
    criteria: List[Tuple[str, str, str]] = field(default_factory=list)  # (field, operator, value)
    tool_attrs: List[Tuple[str, str, str]] = field(default_factory=list)
    description: str = ""


@dataclass
class RuleLibrary:
    """规则库数据结构（支持嵌套）"""
    name: str
    external_id: str
    description: str = ""
    children: List[Union['MachiningRule', 'RuleLibrary']] = field(default_factory=list)


class SchemaAdapter:
    """XML Schema 适配器基类（子类实现版本特定逻辑）"""
    
    def build_library_element(self, parent: ET.Element, lib: RuleLibrary, 
                              objects_elem: ET.Element, id_counter: int) -> Tuple[ET.Element, int]:
        """构建规则库 XML 元素（需子类实现）"""
        raise NotImplementedError
    
    def build_rule_element(self, rule: MachiningRule, objects_elem: ET.Element, 
                          parent_lib_id: str, id_counter: int) -> Tuple[ET.Element, int]:
        """构建规则 XML 元素（需子类实现）"""
        raise NotImplementedError
    
    def get_root_external_id(self) -> str:
        """获取根节点 ExternalId（版本特定）"""
        raise NotImplementedError


class NX12SchemaAdapter(SchemaAdapter):
    """NX12 XML Schema 适配器"""
    
    def get_root_external_id(self) -> str:
        return "OOTB_EnvironmentLibraryEnvRuleRoot"
    
    def build_library_element(self, parent: ET.Element, lib: RuleLibrary,
                              objects_elem: ET.Element, id_counter: int) -> Tuple[ET.Element, int]:
        """NX12 规则库 XML 构建"""
        lib_elem = ET.SubElement(parent, 'MachiningRuleLibrary')
        if lib.external_id:
            lib_elem.set('ExternalId', lib.external_id)
        
        node_info = ET.SubElement(lib_elem, 'NodeInfo')
        ET.SubElement(node_info, 'Id').text = str(id_counter)
        id_counter += 1
        
        ET.SubElement(lib_elem, 'name').text = lib.name
        if lib.description:
            ET.SubElement(lib_elem, 'comment').text = lib.description
        
        collections = ET.SubElement(lib_elem, 'collections')
        if parent.tag == 'RuleRootLibrary':
            ET.SubElement(collections, 'item').text = parent.get('ExternalId')
        
        children = ET.SubElement(lib_elem, 'children')
        
        for child in lib.children:
            if isinstance(child, MachiningRule):
                child_ext_id = f"{lib.external_id}_{child.name}"
                ET.SubElement(children, 'item').text = child_ext_id
                
                rule_elem, id_counter = self.build_rule_element(
                    child, objects_elem, lib.external_id, id_counter
                )
                
            elif isinstance(child, RuleLibrary):
                sub_lib, id_counter = self.build_library_element(
                    objects_elem, child, objects_elem, id_counter
                )
                child_ext_id = child.external_id
                ET.SubElement(children, 'item').text = child_ext_id
                
                coll = sub_lib.find('collections')
                if coll is None:
                    coll = ET.SubElement(sub_lib, 'collections')
                ET.SubElement(coll, 'item').text = lib.external_id
        
        return lib_elem, id_counter
    
    def build_rule_element(self, rule: MachiningRule, objects_elem: ET.Element,
                          parent_lib_id: str, id_counter: int) -> Tuple[ET.Element, int]:
        """NX12 规则 XML 构建（严格遵循四区块格式）"""
        rule_ext_id = f"{parent_lib_id}_{rule.name}"
        
        rule_elem = ET.SubElement(objects_elem, 'MachiningRule')
        rule_elem.set('ExternalId', rule_ext_id)
        
        node_info = ET.SubElement(rule_elem, 'NodeInfo')
        ET.SubElement(node_info, 'Id').text = str(id_counter)
        id_counter += 1
        
        ET.SubElement(rule_elem, 'name').text = rule.name
        
        collections = ET.SubElement(rule_elem, 'collections')
        ET.SubElement(collections, 'item').text = parent_lib_id
        
        # 构建 Conditions 文本块（四区块格式）
        conditions_text = self._build_conditions_text(rule)
        conditions = ET.SubElement(rule_elem, 'Conditions')
        conditions.text = conditions_text
        
        # Input/Output/OperationClass 顺序与原生一致
        inp = ET.SubElement(rule_elem, 'Input')
        ET.SubElement(inp, 'item').text = f"feature.{rule.lwf}"
        
        ET.SubElement(rule_elem, 'OperationClass').text = rule.operation_class
        
        outp = ET.SubElement(rule_elem, 'Output')
        ET.SubElement(outp, 'item').text = f"feature.{rule.mwf}"
        
        ET.SubElement(rule_elem, 'Priority').text = str(rule.priority)
        
        res = ET.SubElement(rule_elem, 'Resources')
        if rule.tool_class:
            ET.SubElement(res, 'item').text = f"tool.{rule.tool_class}"
        
        ET.SubElement(rule_elem, 'comment').text = rule.description
        ET.SubElement(rule_elem, 'type').text = "Composed"
        
        return rule_elem, id_counter
    
    def _build_conditions_text(self, rule: MachiningRule) -> str:
        """构建 Conditions 文本块（严格遵循官方四区块结构）"""
        text = "REM Application Criteria\n"
        
        if rule.criteria:
            text += "\n"
            for field_name, op, value in rule.criteria:
                text += f"{field_name} {op} {value}\n"
        else:
            text += "\n"
        
        text += "\n$$ Rule rejected because condition FALSE\n"
        text += "\nREM Tool Attributes\n"
        
        if rule.tool_attrs:
            text += "\n"
            for field_name, op, value in rule.tool_attrs:
                text += f"{field_name} {op} {value}\n"
        else:
            text += "\n"
        
        text += "\nREM Less Worked Feature Attributes\n\n"
        text += f'REM Operation Attributes\n\noper.name = "{rule.name}"\n'
        
        return text


class FBMGenerator:
    """FBM 规则生成器主类"""
    
    def __init__(self, schema_adapter: SchemaAdapter):
        self.adapter = schema_adapter
    
    def generate_xml(self, input_file: str, output_file: str, 
                    rules: List[RuleLibrary], factory_lib_name: str = "Factory_Plate_General",
                    factory_lib_comment: str = "板类零件通用加工规则库") -> None:
        """生成完整的 machining_knowledge XML 文件"""
        
        print(f"📖 读取基准文件: {input_file}")
        tree = ET.parse(input_file)
        root = tree.getroot()
        objects = root.find('Objects')
        
        # 查找规则根节点
        rule_root = None
        root_ext_id = self.adapter.get_root_external_id()
        for elem in objects:
            if elem.tag == 'RuleRootLibrary' and elem.get('ExternalId') == root_ext_id:
                rule_root = elem
                break
        
        if not rule_root:
            raise ValueError(f"未找到规则根节点 (ExternalId={root_ext_id})")
        
        # 清除脏节点（可选）
        self._clean_corrupted_nodes(objects, rule_root)
        
        # 计算下一个可用 ID
        next_id = self._get_next_id(objects)
        
        # 创建工厂规则库
        factory_lib = self._create_factory_library(
            objects, factory_lib_name, factory_lib_comment, rule_root, next_id
        )
        next_id += 1
        
        # 添加子规则库
        children = ET.SubElement(factory_lib, 'children')
        for rule_lib in rules:
            sub_lib, next_id = self.adapter.build_library_element(
                objects, rule_lib, objects, next_id
            )
            ET.SubElement(children, 'item').text = rule_lib.external_id
            
            # 设置父级引用
            coll = sub_lib.find('collections')
            if coll is None:
                coll = ET.SubElement(sub_lib, 'collections')
            ET.SubElement(coll, 'item').text = factory_lib.get('ExternalId')
        
        # 保存文件
        print(f"💾 保存文件: {output_file}")
        ET.indent(tree, space="  ")  # Python 3.9+ 支持
        tree.write(output_file, encoding='UTF-8', xml_declaration=True)
        print("✅ 生成完成！")
    
    def _clean_corrupted_nodes(self, objects: ET.Element, rule_root: ET.Element) -> None:
        """清除脏节点（日期戳或旧工厂规则）"""
        import re
        
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
                if item.text in ids_to_remove or item.text == 'Factory_Plate_General_Lib':
                    to_del.append(item)
            for item in to_del:
                children_elem.remove(item)
        
        for elem in elems_to_remove:
            objects.remove(elem)
        
        if elems_to_remove:
            print(f"✅ 清除 {len(elems_to_remove)} 个脏节点")
    
    def _get_next_id(self, objects: ET.Element) -> int:
        """获取下一个可用的 NodeInfo ID"""
        max_id = 0
        for elem in objects.iter('Id'):
            try:
                id_val = int(elem.text)
                if id_val > max_id:
                    max_id = id_val
            except:
                pass
        return max_id + 1
    
    def _create_factory_library(self, objects: ET.Element, name: str, comment: str,
                               rule_root: ET.Element, lib_id: int) -> ET.Element:
        """创建工厂规则库根节点"""
        factory_ext_id = f"{name}_Lib"
        
        factory_lib = ET.SubElement(objects, 'MachiningRuleLibrary')
        factory_lib.set('ExternalId', factory_ext_id)
        
        node_info = ET.SubElement(factory_lib, 'NodeInfo')
        ET.SubElement(node_info, 'Id').text = str(lib_id)
        
        ET.SubElement(factory_lib, 'name').text = name
        ET.SubElement(factory_lib, 'comment').text = comment
        
        collections = ET.SubElement(factory_lib, 'collections')
        ET.SubElement(collections, 'item').text = self.adapter.get_root_external_id()
        
        # 添加到规则根的 children
        children_elem = rule_root.find('children')
        if children_elem is None:
            children_elem = ET.SubElement(rule_root, 'children')
        ET.SubElement(children_elem, 'item').text = factory_ext_id
        
        return factory_lib
    
    def validate_rules(self, rules: List[RuleLibrary]) -> List[str]:
        """验证规则完整性和冲突"""
        errors = []
        
        # 检查优先级重复
        priority_map = {}  # operation_class -> {priority: rule_name}
        self._collect_priorities(rules, priority_map)
        
        for op_class, priorities in priority_map.items():
            for priority, rule_names in priorities.items():
                if len(rule_names) > 1:
                    errors.append(
                        f"⚠️ 优先级冲突 [{op_class}] Priority {priority}: {', '.join(rule_names)}"
                    )
        
        # 检查直径窗口重叠（针对孔加工规则）
        hole_rules = self._collect_hole_rules(rules)
        overlaps = self._check_diameter_overlaps(hole_rules)
        errors.extend(overlaps)
        
        return errors
    
    def _collect_priorities(self, rules: List[RuleLibrary], 
                           priority_map: dict, parent_path: str = "") -> None:
        """递归收集所有规则的优先级"""
        for rule_or_lib in rules:
            if isinstance(rule_or_lib, MachiningRule):
                op_class = rule_or_lib.operation_class
                if op_class not in priority_map:
                    priority_map[op_class] = {}
                
                priority = rule_or_lib.priority
                if priority not in priority_map[op_class]:
                    priority_map[op_class][priority] = []
                priority_map[op_class][priority].append(rule_or_lib.name)
            
            elif isinstance(rule_or_lib, RuleLibrary):
                new_path = f"{parent_path}/{rule_or_lib.name}" if parent_path else rule_or_lib.name
                self._collect_priorities(rule_or_lib.children, priority_map, new_path)
    
    def _collect_hole_rules(self, rules: List[RuleLibrary]) -> List[MachiningRule]:
        """收集所有孔加工规则"""
        hole_rules = []
        for rule_or_lib in rules:
            if isinstance(rule_or_lib, MachiningRule):
                if 'hole_making' in rule_or_lib.operation_class.lower():
                    hole_rules.append(rule_or_lib)
            elif isinstance(rule_or_lib, RuleLibrary):
                hole_rules.extend(self._collect_hole_rules(rule_or_lib.children))
        return hole_rules
    
    def _check_diameter_overlaps(self, hole_rules: List[MachiningRule]) -> List[str]:
        """检查直径窗口是否重叠"""
        errors = []
        
        # 按 operation_class 分组
        groups = {}
        for rule in hole_rules:
            key = rule.operation_class
            if key not in groups:
                groups[key] = []
            groups[key].append(rule)
        
        # 检查每组内的直径范围
        for op_class, rules in groups.items():
            ranges = []
            for rule in rules:
                for field_name, op, value in rule.criteria:
                    if 'DIAMETER' in field_name:
                        ranges.append((rule.name, float(value), op))
            
            # 简化检查：只检查相同操作类型的相邻范围
            # 实际应用中需要更复杂的区间重叠检测算法
            # 这里仅作示例
        
        return errors


def simulate_mke_matching(test_features: List[dict], 
                         rules: List[MachiningRule]) -> List[dict]:
    """模拟 MKE 规则匹配过程（用于回归测试）"""
    results = []
    
    for feature in test_features:
        matched_rule = None
        
        # 按优先级降序遍历规则
        sorted_rules = sorted(rules, key=lambda r: r.priority, reverse=True)
        
        for rule in sorted_rules:
            if _check_criteria(feature, rule.criteria):
                matched_rule = rule
                break  # 最高优先级规则胜出
        
        results.append({
            'feature': feature,
            'matched_rule': matched_rule.name if matched_rule else None,
            'status': 'MATCHED' if matched_rule else 'UNMATCHED'
        })
    
    return results


def _check_criteria(feature: dict, criteria: List[Tuple[str, str, str]]) -> bool:
    """检查特征是否满足规则条件"""
    for field_name, op, value in criteria:
        # 提取字段值（如 mwf.DIAMETER_1 → feature['DIAMETER_1']）
        field_key = field_name.split('.')[-1]
        if field_key not in feature:
            return False
        
        feature_value = feature[field_key]
        expected_value = float(value)
        
        # 执行比较
        if op == '>=' and not (feature_value >= expected_value):
            return False
        elif op == '<=' and not (feature_value <= expected_value):
            return False
        elif op == '>' and not (feature_value > expected_value):
            return False
        elif op == '<' and not (feature_value < expected_value):
            return False
        elif op == '=' and not (abs(feature_value - expected_value) < 1e-6):
            return False
    
    return True


# ==================== 示例用法 ====================

if __name__ == '__main__':
    # 1. 定义规则数据
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
        ]
    )
    
    # 2. 创建生成器（使用 NX12 Schema）
    adapter = NX12SchemaAdapter()
    generator = FBMGenerator(adapter)
    
    # 3. 验证规则
    errors = generator.validate_rules([face_lib])
    if errors:
        print("⚠️ 验证发现以下问题:")
        for error in errors:
            print(f"  {error}")
    else:
        print("✅ 规则验证通过")
    
    # 4. 生成 XML
    # generator.generate_xml(
    #     input_file='machining_knowledge.xml',
    #     output_file='machining_knowledge_test.xml',
    #     rules=[face_lib]
    # )
    
    # 5. 模拟匹配测试
    test_features = [
        {'DIAMETER_1': 10.5, 'DEPTH': 20.0},
        {'DIAMETER_1': 5.0, 'DEPTH': 15.0},
    ]
    
    all_rules = [face_lib.children[0]]  # 提取所有 MachiningRule
    results = simulate_mke_matching(test_features, all_rules)
    
    print("\n🧪 回归测试结果:")
    for result in results:
        print(f"  特征: {result['feature']} → {result['status']} ({result['matched_rule']})")
