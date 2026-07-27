# 📐 一建机电实务 · 知识库

> 基于环球网校 2026 考点精讲（81 讲）整理的 Obsidian 知识库，覆盖一级建造师（机电实务）全部考点。

## 这是什么

用 [Obsidian](https://obsidian.md) 打开的知识库，包含一建机电实务全部 6 章、81 讲考点笔记。每章配有 Canvas 知识图谱，可直观浏览知识点之间的关联。

## 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/qizhengle/yijian_jidian.git

# 2. 用 Obsidian 打开
#    打开 Obsidian → Open folder as vault → 选择 yijian_jidian 目录
```

> 没有 Obsidian？直接浏览 Markdown 文件也行，只是看不到 Canvas 知识图谱。

## 内容概览

| 章节 | 讲次 | 内容 |
|------|------|------|
| ch01 材料与设备 | 5 讲 | 金属/非金属/电气材料分类，通用/专用设备性能 |
| ch02 专业技术 | 7 讲 | 工程测量、起重吊装、焊接技术与检验 |
| ch03 建筑机电 | 23 讲 | 给排水、电气、通风空调、智能化、电梯、消防 |
| ch04 工业机电 | 28 讲 | 设备安装、管道、电气、仪表、防腐绝热、锅炉发电 |
| ch05 法规与标准 | 4 讲 | 计量法、用电规定、特种设备、相关标准 |
| ch06 施工管理 | 14 讲 | 组织设计、招投标、合同、进度/质量/成本/安全管理 |

## 目录结构

```
yijian_jidian/
├── 00-目录.md                # 总导航（MOC）
├── ch01-材料与设备/           #   5 篇笔记 + Canvas 图谱
├── ch02-专业技术/             #   7 篇笔记 + Canvas 图谱
├── ch03-建筑机电/             #  23 篇笔记 + Canvas 图谱
├── ch04-工业机电/             #  28 篇笔记 + Canvas 图谱
├── ch05-法规与标准/           #   4 篇笔记 + Canvas 图谱
├── ch06-施工管理/             #  14 篇笔记 + Canvas 图谱
├── scripts/                  # 构建脚本（Python）
│   ├── build_vault.py        #   从 temp/ 生成 .md 笔记
│   └── build_canvas.py       #   生成 Canvas 知识图谱
└── temp/                     # 原始提取文本（81 个 .txt）
```

## Canvas 知识图谱

每个章节有一个 `.canvas` 文件，在 Obsidian 中打开可以看到知识点之间的可视化关联——节点是考点，连线是逻辑关系。适合复习时快速建立全局视野。

## 许可

[Apache License 2.0](LICENSE) © 2026 qizhengle
