#!/usr/bin/env python3
"""
Phase 3: 为每个章节生成 Canvas 知识图谱文件
Phase 4: 生成 00-目录.md MOC 索引 + .obsidian 基础配置
"""
import json, os, re
from pathlib import Path

VAULT = Path(__file__).parent.parent
CHAPTERS = [
    ("ch01-材料与设备", "机电工程常用材料及设备", [
        ("1.1", "金属材料", 1, 3),   # 第1-3讲
        ("1.2", "设备", 4, 5),       # 第4-5讲
    ]),
    ("ch02-专业技术", "机电工程专业技术", [
        ("2.1", "工程测量", 6, 6),
        ("2.2", "起重技术", 7, 9),
        ("2.3", "焊接技术", 10, 12),
    ]),
    ("ch03-建筑机电", "建筑机电工程施工技术", [
        ("3.1", "给排水供暖", 13, 15),
        ("3.2", "建筑电气", 16, 21),
        ("3.3", "通风与空调", 22, 26),
        ("3.4", "智能化系统", 27, 29),
        ("3.5", "电梯", 30, 32),
        ("3.6", "消防", 33, 35),
    ]),
    ("ch04-工业机电", "工业机电工程安装技术", [
        ("4.1", "机械设备安装", 36, 40),
        ("4.2", "工业管道", 41, 44),
        ("4.3", "电气装置", 45, 49),
        ("4.4", "自动化仪表", 50, 51),
        ("4.5", "防腐蚀", 52, 52),
        ("4.6", "绝热", 53, 53),
        ("4.7", "设备安装", 54, 57),
        ("4.8", "发电设备", 58, 61),
        ("4.9", "冶炼设备", 62, 63),
    ]),
    ("ch05-法规与标准", "机电工程相关法规与标准", [
        ("5.1", "计量", 64, 64),
        ("5.2", "建设用电", 65, 65),
        ("5.3", "特种设备", 66, 66),
        ("6", "相关标准", 67, 67),
    ]),
    ("ch06-施工管理", "机电工程项目施工管理", [
        ("7.1-7.2", "企业资质与机构", 68, 68),
        ("7.3", "施工组织设计", 69, 70),
        ("8.1-8.2", "招投标与合同", 71, 72),
        ("9", "施工进度管理", 73, 73),
        ("10", "施工质量管理", 74, 74),
        ("11", "施工成本管理", 75, 75),
        ("12", "施工安全管理", 76, 76),
        ("13", "绿色建造", 77, 77),
        ("14", "资源管理", 78, 79),
        ("15", "试运行与竣工", 80, 80),
        ("16", "运维与保修", 81, 81),
    ]),
]

COLORS = {
    'center': '#2563eb',     # 蓝色 - 章节中心
    'lecture': '#16a34a',    # 绿色 - 讲次节点
    'subsection': '#7c3aed', # 紫色 - 小节节点
    'edge_dep': '#16a34a',   # 绿色 - 依赖关系
    'edge_ref': '#ea580c',   # 橙色 - 横向关联
}

def find_md_files(ch_dir: Path, lec_range: range) -> list:
    """Find .md files in chapter directory matching lecture numbers."""
    files = []
    for md in sorted(ch_dir.glob('*.md')):
        m = re.match(r'第(\d+)讲', md.name)
        if m:
            num = int(m.group(1))
            if num in lec_range:
                files.append(md)
    return files

def generate_canvas(ch_id: str, ch_title: str, subsections: list) -> dict:
    """Generate Canvas JSON for a chapter."""
    ch_dir = VAULT / ch_id
    nodes = []
    edges = []
    edge_idx = 0

    # Center node: chapter title
    center_id = f"center-{ch_id}"
    nodes.append({
        "id": center_id,
        "type": "text",
        "text": f"# {ch_title}\n\n[[00-目录|← 返回目录]]",
        "x": 300, "y": 0,
        "width": 280, "height": 100,
        "color": COLORS['center']
    })

    # Process each subsection
    prev_section_end_y = 150
    for sec_idx, (sec_id, sec_title, lec_start, lec_end) in enumerate(subsections):
        lec_range = range(lec_start, lec_end + 1)
        md_files = find_md_files(ch_dir, lec_range)

        # Subsection label node
        sec_node_id = f"sec-{ch_id}-{sec_id}"
        sec_y = prev_section_end_y
        nodes.append({
            "id": sec_node_id,
            "type": "text",
            "text": f"## {sec_id} {sec_title}",
            "x": 100, "y": sec_y,
            "width": 180, "height": 50,
            "color": COLORS['subsection']
        })

        # Edge: center → subsection
        edge_idx += 1
        edges.append({
            "id": f"e{edge_idx:04d}",
            "fromNode": center_id,
            "fromSide": "bottom",
            "toNode": sec_node_id,
            "toSide": "top",
            "color": COLORS['edge_dep'],
            "label": f"第{lec_start}-{lec_end}讲"
        })

        # Lecture nodes (horizontal layout)
        node_y = sec_y + 80
        for file_idx, md_file in enumerate(md_files):
            lec_name = md_file.stem.replace('.md', '')
            # Shorten display name
            display_name = lec_name[:18] + '...' if len(lec_name) > 20 else lec_name
            node_x = 100 + file_idx * 260

            lec_node_id = f"lec-{ch_id}-{md_file.stem[:30]}"
            nodes.append({
                "id": lec_node_id,
                "type": "text",
                "text": f"# [[{lec_name}|{display_name}]]",
                "x": node_x, "y": node_y,
                "width": 240, "height": 80,
                "color": COLORS['lecture']
            })

            # Edge: subsection → lecture
            edge_idx += 1
            edges.append({
                "id": f"e{edge_idx:04d}",
                "fromNode": sec_node_id,
                "fromSide": "bottom",
                "toNode": lec_node_id,
                "toSide": "top",
                "color": COLORS['edge_dep'],
                "label": ""
            })

            # Edge: lecture → lecture (sequential)
            if file_idx > 0:
                prev_lec_node_id = f"lec-{ch_id}-{md_files[file_idx-1].stem[:30]}"
                edge_idx += 1
                edges.append({
                    "id": f"e{edge_idx:04d}",
                    "fromNode": prev_lec_node_id,
                    "fromSide": "right",
                    "toNode": lec_node_id,
                    "toSide": "left",
                    "color": COLORS['edge_ref'],
                    "label": "→"
                })

        prev_section_end_y = node_y + 120

    return {"nodes": nodes, "edges": edges}

def main():
    # ─── Generate Canvas files ───
    for ch_id, ch_title, subsections in CHAPTERS:
        canvas_data = generate_canvas(ch_id, ch_title, subsections)
        canvas_path = VAULT / ch_id / f"{ch_id}.canvas"
        with open(canvas_path, 'w', encoding='utf-8') as f:
            json.dump(canvas_data, f, ensure_ascii=False, indent=2)
        print(f"✅ {ch_id}.canvas — {len(canvas_data['nodes'])} 节点, {len(canvas_data['edges'])} 边")

    # ─── Generate MOC index ───
    moc_lines = [
        "---",
        "title: 一建机电知识库",
        "tags:",
        "  - MOC",
        "  - 一建机电",
        "created: 2026-07-13",
        "---",
        "",
        "# 一建机电实务 · 知识库",
        "",
        "> [!important] 总览",
        "> 基于环球网校 2026 考点精讲（81讲）整理的 Obsidian 知识库。",
        "> 共 6 章、81 讲，覆盖一建机电实务全部考点。",
        "",
        "---",
        "",
        "## 📊 章节速览",
        "",
        "| 章节 | 讲次 | Canvas |",
        "|------|------|--------|",
    ]

    for ch_id, ch_title, subsections in CHAPTERS:
        ch_dir = VAULT / ch_id
        md_count = len(list(ch_dir.glob('*.md')))
        canvas_file = f"{ch_id}.canvas"
        moc_lines.append(f"| [[{ch_id}/{ch_id}.canvas|{ch_title}]] | {md_count} 讲 | [[{ch_id}/{canvas_file}|📊 图谱]] |")

    moc_lines.append("")
    moc_lines.append("---")
    moc_lines.append("")
    moc_lines.append("## 📖 各章目录")
    moc_lines.append("")

    for ch_id, ch_title, subsections in CHAPTERS:
        ch_dir = VAULT / ch_id
        moc_lines.append(f"### [[{ch_id}/{ch_id}.canvas|{ch_title}]]")
        moc_lines.append("")

        for sec_id, sec_title, lec_start, lec_end in subsections:
            lec_range = range(lec_start, lec_end + 1)
            md_files = sorted(
                [f for f in ch_dir.glob('*.md') if re.match(r'第(\d+)讲', f.name) and int(re.match(r'第(\d+)讲', f.name).group(1)) in lec_range],
                key=lambda f: int(re.match(r'第(\d+)讲', f.name).group(1))
            )
            moc_lines.append(f"**{sec_id} {sec_title}**")
            for md_file in md_files:
                lec_name = md_file.stem
                m = re.match(r'第(\d+)讲', lec_name)
                lec_num = m.group(0) if m else ""
                moc_lines.append(f"- [[{ch_id}/{lec_name}|{lec_num} {md_file.stem[len(lec_num):].lstrip('-')}]]")
            moc_lines.append("")

        moc_lines.append(f"> 打开 Canvas: [[{ch_id}/{ch_id}.canvas|📊 {ch_title} 知识图谱]]")
        moc_lines.append("")

    moc_path = VAULT / "00-目录.md"
    with open(moc_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(moc_lines))
    print(f"\n✅ 00-目录.md 已生成")

    # ─── Generate .obsidian config ───
    obsidian_dir = VAULT / ".obsidian"
    os.makedirs(obsidian_dir, exist_ok=True)

    # app.json
    app_config = {
        "newFileLocation": "folder",
        "newFileFolderPath": "00-收件箱",
        "attachmentFolderPath": "assets",
        "showLineNumber": False,
        "defaultViewMode": "preview",
        "livePreview": True,
    }
    with open(obsidian_dir / "app.json", 'w', encoding='utf-8') as f:
        json.dump(app_config, f, ensure_ascii=False, indent=2)

    # graph.json
    graph_config = {
        "collapse-filter": False,
        "search": "",
        "showTags": True,
        "showAttachments": False,
        "hideUnresolved": False,
        "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [],
        "collapse-display": False,
        "showArrow": False,
        "textFadeMultiplier": 0,
        "nodeSizeMultiplier": 1,
        "lineSizeMultiplier": 1,
        "collapse-forces": False,
        "centerStrength": 0.518713248970312,
        "repelStrength": 10,
        "linkStrength": 1,
        "linkDistance": 250,
        "scale": 1,
    }
    with open(obsidian_dir / "graph.json", 'w', encoding='utf-8') as f:
        json.dump(graph_config, f, ensure_ascii=False, indent=2)

    print("✅ .obsidian/ 配置已生成")
    print(f"\n🎉 Phase 3+4 完成! Vault 就绪: {VAULT}")

if __name__ == '__main__':
    main()
