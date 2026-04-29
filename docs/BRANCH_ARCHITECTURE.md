# GitHub 分支架构说明

**版本**: v1.0  
**最后更新**: 2026-04-29  
**适用范围**: NX12MKE 项目

---

## 分支架构图

```
main (核心主干)
│   ├── 通用工艺手册（docs/guides/FBM_Development_Guide.md）
│   ├── 核心自动化框架（fbm_generator_core.py）
│   └── 业务流程规范（FBM 开发 SOP）
│
├─ release/NX12MKE
│   ├── modify_mke_v12.py（旧版脚本，保留参考）
│   ├── machining_knowledge_v12.xml（生成的规则库）
│   └── NX12 特定的工艺窗口和 XML Schema
│
└─ release/NX2512FBM
    ├── fbm_generator_core.py（从 master 合并）
    ├── rules_data_nx2512.py（待开发：NX2512 规则数据）
    └── 适配 NX2512 新特性（多轴支持、新特征识别引擎等）
```

---

## 分支策略详解

### 1. main 分支（核心主干）

**用途**：存储跨版本通用的核心资产

**包含内容**：
- ✅ `fbm_generator_core.py` - 通用生成框架（数据与序列化分离）
- ✅ `docs/guides/FBM_Development_Guide.md` - 通用工艺知识
- ✅ `docs/guides/README_FBM_Core.md` - 核心框架使用说明
- ✅ `.gitignore` - 排除版本特定输出文件
- ❌ **不包含**：版本特定的规则数据、生成的 XML 文件

**提交规范**：
```bash
# 仅提交通用框架改进
git checkout main
git add fbm_generator_core.py docs/guides/
git commit -m "feat: 新增冲突检测工具"
```

### 2. release/NX12MKE 分支

**用途**：锁定 NX12 的 XML Schema 和工艺窗口

**包含内容**：
- ✅ `modify_mke_v12.py` - 旧版脚本（历史参考）
- ✅ `machining_knowledge_v12.xml` - 已验证的规则库
- ✅ `rules_data_nx12.py` - NX12 规则数据定义（可选，如果使用新框架）
- ❌ **不包含**：master 的新框架文件（除非手动合并）

**状态**：生产就绪，不再主动开发新功能

**维护策略**：
- 仅接受 Bug 修复
- 不接受新功能（新功能应在 NX2512FBM 分支开发）

### 3. release/NX2512FBM 分支

**用途**：适配 NX2512 的新特性

**包含内容**：
- ✅ `fbm_generator_core.py` - 从 master 合并的核心框架
- ⏳ `rules_data_nx2512.py` - 待开发：NX2512 规则数据
- ⏳ `generate_mke_nx2512.py` - 待开发：NX2512 生成器入口
- ⏳ `fbm_generator_nx2512.py` - 待开发：NX2512 Schema 适配器

**开发计划**：
1. 创建 `NX2512SchemaAdapter`（继承自 `SchemaAdapter`）
2. 定义 NX2512 特有的规则数据（如多轴加工规则）
3. 测试并验证生成的 XML 在 NX2512 中的兼容性

---

## 工作流程示例

### 场景 1：修复通用框架 Bug

```bash
# 1. 在 main 分支修复
git checkout main
git checkout -b fix/conflict-detection
# 修改 fbm_generator_core.py
git add fbm_generator_core.py
git commit -m "fix: 修复优先级冲突检测逻辑"

# 2. 合并到 main
git checkout main
git merge fix/conflict-detection

# 3. 同步到各版本分支
git checkout release/NX2512FBM
git merge main

git checkout release/NX12MKE
git merge main  # 可选，如果 NX12 也需要此修复
```

### 场景 2：新增 NX2512 多轴加工规则

```bash
# 1. 在 NX2512FBM 分支开发
git checkout release/NX2512FBM
git checkout -b feature/multi-axis-rules

# 2. 创建 NX2512 规则数据
# 编辑 rules_data_nx2512.py

# 3. 创建 Schema 适配器
# 编辑 fbm_generator_nx2512.py

# 4. 测试并验证
python generate_mke_nx2512.py

# 5. 合并回 NX2512FBM
git checkout release/NX2512FBM
git merge feature/multi-axis-rules
```

### 场景 3：为板类零件创建专用规则

```bash
# 1. 创建特性分支
git checkout release/NX2512FBM
git checkout -b feature/Plate_General

# 2. 开发板类规则
# 编辑 rules_data_nx2512.py，添加板类特定规则

# 3. 测试并验证
python generate_mke_nx2512.py

# 4. 合并回 NX2512FBM
git checkout release/NX2512FBM
git merge feature/Plate_General
```

---

## 合并策略

### main → release/NX2512FBM

**频率**：每周或当 main 有重要更新时

**方式**：快进合并或三方合并

```bash
git checkout release/NX2512FBM
git merge main --no-edit
```

**注意**：
- 可能遇到 `.idea/workspace.xml` 冲突，使用 `git checkout --ours` 解决
- 不要将版本特定文件（如 `machining_knowledge_v12.xml`）合并到 main

### release/NX2512FBM → main

**频率**：仅当 NX2512FBM 开发了通用框架改进时

**方式**： cherry-pick 特定提交

```bash
# 假设 NX2512FBM 提交了通用框架改进
git checkout main
git cherry-pick <commit-hash-from-NX2512FBM>
```

**注意**：
- 避免将版本特定代码合并到 main
- 优先提取通用逻辑到 `fbm_generator_core.py`

---

## 标签与发布

### 创建 Release 标签

当某个版本的规则库验证通过后，创建 Git 标签：

```bash
# NX12 规则库发布
git checkout release/NX12MKE
git tag -a v12.0.0 -m "Release NX12 MKE rule base v12.0.0"
git push origin v12.0.0

# NX2512 规则库发布（未来）
git checkout release/NX2512FBM
git tag -a v2512.0.0 -m "Release NX2512 FBM rule base v2512.0.0"
git push origin v2512.0.0
```

### GitHub Release

在 GitHub Web 界面创建 Release，挂载：
- 生成的 XML 文件（`machining_knowledge_v12.xml`）
- 工艺单（HTML/PDF）
- 变更日志（CHANGELOG.md）

---

## 常见问题

### Q1: 为什么不在 main 分支直接开发？

**A**: 
- main 分支应保持纯净，仅包含跨版本通用代码
- 版本特定开发应在各自分支进行，避免污染主干
- 便于回溯和维护不同版本的规则库

### Q2: 如何处理分支间的代码复用？

**A**:
- 通用逻辑应放在 `fbm_generator_core.py`（main 分支）
- 版本特定逻辑通过 `SchemaAdapter` 隔离
- 使用继承和策略模式实现代码复用

### Q3: release/NX12MKE 需要合并 main 的更新吗？

**A**:
- 如果 main 的更新是 Bug 修复且影响 NX12，应该合并
- 如果是新功能（如 NX2512 多轴支持），不需要合并
- 合并前评估影响范围，避免引入不兼容改动

### Q4: 如何管理多个零件类型的规则？

**A**:
- 方案 1：在同一版本分支内创建子模块（如 `rules_data_plate.py`, `rules_data_shaft.py`）
- 方案 2：为每个零件类型创建特性分支（如 `feature/Plate_General`, `feature/Shaft_Rules`）
- 推荐：方案 2，便于独立开发和测试

---

## 最佳实践

### 1. 提交信息规范

```
<type>: <subject>

<body>

<footer>
```

**Type 类型**：
- `feat`: 新功能
- `fix`: Bug 修复
- `refactor`: 重构（不改变功能）
- `docs`: 文档更新
- `test`: 测试相关
- `chore`: 构建工具、依赖更新

**示例**：
```
feat: 新增 NX2512 五轴叶片加工规则

- 创建 NX2512SchemaAdapter
- 添加 VARIABLE_CONTOUR 工序支持
- 更新 rules_data_nx2512.py

Closes #123
```

### 2. 分支命名规范

- 特性分支：`feature/<描述>`（如 `feature/multi-axis-rules`）
- 修复分支：`fix/<描述>`（如 `fix/priority-conflict`）
- 发布分支：`release/<版本>`（如 `release/NX2512FBM`）

### 3. 代码审查

- 所有合并到 main 的 PR 必须经过 Code Review
- 重点检查：是否符合数据与序列化分离原则
- 验证：是否引入了版本特定耦合

### 4. 持续集成

未来可配置 GitHub Actions：
- 自动运行回归测试
- 验证生成的 XML 格式
- 检查规则冲突

---

## 参考资料

- [FBM 开发通用规范](docs/guides/FBM_Development_Guide.md)
- [核心框架使用说明](docs/guides/README_FBM_Core.md)
- [AGENTS.md](AGENTS.md) - AI 行为准则

---

**维护者**: AI CAM Engineering Team  
**最后更新**: 2026-04-29
