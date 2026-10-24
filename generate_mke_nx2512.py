"""
NX-FBM NX2512 MKE 规则生成器主入口
版本: v2512.0
项目名称: NX-FBM
用法: python generate_mke_nx2512.py
"""

import sys
from fbm_generator_core import FBMGenerator, NX12SchemaAdapter
from rules_data_nx2512 import create_nx2512_rules


def main():
    """主函数"""
    print("=" * 60)
    print("NX-FBM NX2512 MKE 规则生成器 v2512.0")
    print("=" * 60)
    
    # 1. 加载规则数据
    print("\n📋 加载 NX2512 规则数据...")
    rules = create_nx2512_rules()
    print(f"✅ 加载完成，共 {len(rules)} 个主规则库")
    
    # 统计规则数量
    total_rules = 0
    for lib in rules:
        total_rules += count_rules(lib)
    print(f"📊 总规则数: {total_rules} 条")
    
    # 2. 验证规则
    print("\n🔍 验证规则完整性和冲突...")
    adapter = NX12SchemaAdapter()
    generator = FBMGenerator(adapter)
    
    errors = generator.validate_rules(rules)
    if errors:
        print("⚠️ 发现以下问题:")
        for error in errors:
            print(f"  {error}")
        print("\n⚠️ 建议修复后再继续生成 XML")
        return
    else:
        print("✅ 规则验证通过")
    
    # 3. 生成 XML
    input_file = 'machining_knowledge.xml'
    output_file = 'machining_knowledge_v2.xml'
    
    print(f"\n🏭 开始生成 XML 文件...")
    print(f"   输入: {input_file}")
    print(f"   输出: {output_file}")
    
    try:
        generator.generate_xml(
            input_file=input_file,
            output_file=output_file,
            rules=rules,
            factory_lib_name="Factory_Plate_NX2512_General",
            factory_lib_comment="板类零件 NX2512 自动化升级加工规则库"
        )
        print("\n✅ 生成成功！")
        print(f"📁 输出文件: {output_file}")
        
    except FileNotFoundError:
        print(f"\n❌ 错误: 找不到输入文件 '{input_file}'")
        print("   请确保 machining_knowledge.xml 存在于当前目录")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def count_rules(lib_or_rule) -> int:
    """递归统计规则数量"""
    from fbm_generator_core import MachiningRule, RuleLibrary
    
    if isinstance(lib_or_rule, MachiningRule):
        return 1
    elif isinstance(lib_or_rule, RuleLibrary):
        count = 0
        for child in lib_or_rule.children:
            count += count_rules(child)
        return count
    return 0


if __name__ == '__main__':
    main()
