#!/usr/bin/env python3
"""
Phase 1: 批量提取 2026一建机电考点精讲 PDF → 原始文本文件
输出到 yijian-vault/temp/ 目录，供 Phase 2 AI 精炼
"""
import os, re, json, sys
from pathlib import Path
from PyPDF2 import PdfReader

# Paths
PROJ_ROOT = Path(__file__).parent.parent.parent  # proj_agent/
PDF_DIR = PROJ_ROOT / "2026-yijian-jidian"
VAULT_ROOT = Path(__file__).parent.parent  # yijian-vault/
TEMP_DIR = VAULT_ROOT / "temp"

# Chapter mapping
CHAPTER_MAP = [
    ("ch01-材料与设备", "机电工程常用材料及设备",        range(1, 6)),    # 第1-5讲
    ("ch02-专业技术",   "机电工程专业技术",              range(6, 13)),   # 第6-12讲
    ("ch03-建筑机电",   "建筑机电工程施工技术",           range(13, 36)),  # 第13-35讲
    ("ch04-工业机电",   "工业机电工程安装技术",           range(36, 64)),  # 第36-63讲
    ("ch05-法规与标准", "机电工程相关法规与标准",         range(64, 68)),  # 第64-67讲
    ("ch06-施工管理",   "机电工程项目施工管理",           range(68, 82)),  # 第68-81讲
]

def clean_text(text: str) -> str:
    """Remove boilerplate headers/footers, normalize whitespace."""
    text = re.sub(r'学员专用\s*请勿外泄', '', text)
    text = re.sub(r'第\s*\d+\s*页\s*共\s*\d+\s*页', '', text)
    text = re.sub(r'扫码关注更多内容', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = [l.strip() for l in text.split('\n')]
    return '\n'.join(l for l in lines if l)

def extract_lecture_number(filename: str) -> int:
    m = re.search(r'第(\d+)讲', filename)
    return int(m.group(1)) if m else 0

def extract_title(filename: str) -> str:
    name = re.sub(r'^2026一建机电考点精讲-第\d+讲-', '', filename)
    name = name.replace('.pdf', '')
    return name

def extract_section_id(filename: str) -> str:
    """Extract section number like 1.1, 2.3, 3.1 from filename"""
    m = re.search(r'-(\d+\.\d+)', filename)
    return m.group(1) if m else ""

def assign_chapter(lecture_num: int) -> tuple:
    for ch_id, ch_title, r in CHAPTER_MAP:
        if lecture_num in r:
            return ch_id, ch_title
    return 'ch99-未分类', '未分类'

def parse_pdf(filepath: Path) -> dict:
    """Parse a single PDF and return structured content."""
    try:
        reader = PdfReader(str(filepath))
        full_text = '\n'.join(page.extract_text() or '' for page in reader.pages)
        full_text = clean_text(full_text)

        lecture_num = extract_lecture_number(filepath.name)
        title = extract_title(filepath.name)
        section_id = extract_section_id(filepath.name)
        ch_id, ch_title = assign_chapter(lecture_num)

        return {
            'lecture': lecture_num,
            'title': title,
            'section_id': section_id,
            'chapter_id': ch_id,
            'chapter_title': ch_title,
            'raw_text': full_text,
            'total_chars': len(full_text),
            'source_filename': filepath.name,
        }
    except Exception as e:
        print(f'  ⚠️ 解析失败: {filepath.name} — {e}', file=sys.stderr)
        return None

def main():
    # Filter: only process yijian jidian PDFs, skip the economics textbook
    all_pdfs = sorted(PDF_DIR.glob('*.pdf'), key=lambda p: extract_lecture_number(p.name))
    pdf_files = [p for p in all_pdfs if '一建机电考点精讲' in p.name]
    skipped = [p for p in all_pdfs if '一建机电考点精讲' not in p.name]

    print(f'📂 找到 {len(pdf_files)} 个考点精讲 PDF')
    if skipped:
        print(f'⏭️ 跳过 {len(skipped)} 个非考点文件: {[p.name for p in skipped]}')
    print()

    os.makedirs(TEMP_DIR, exist_ok=True)

    # Build manifest
    manifest = {'chapters': {}, 'lectures': []}

    for pdf_file in pdf_files:
        lec = extract_lecture_number(pdf_file.name)
        if lec == 0:
            print(f'  ⚠️ 无法识别讲次: {pdf_file.name}')
            continue

        print(f'  [{lec:02d}] 提取: {pdf_file.name[:60]}...')
        parsed = parse_pdf(pdf_file)

        if parsed and parsed['raw_text']:
            # Write raw text to temp file
            safe_name = f'L{lec:02d}-{parsed["section_id"]}-{parsed["title"][:40]}.txt'
            safe_name = re.sub(r'[\\/:*?"<>|]', '_', safe_name)
            out_path = TEMP_DIR / safe_name
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(parsed['raw_text'])

            # Track in manifest
            ch_id = parsed['chapter_id']
            if ch_id not in manifest['chapters']:
                manifest['chapters'][ch_id] = {
                    'title': parsed['chapter_title'],
                    'lectures': [],
                }
            manifest['chapters'][ch_id]['lectures'].append({
                'num': lec,
                'section': parsed['section_id'],
                'title': parsed['title'],
                'file': safe_name,
                'source': parsed['source_filename'],
                'chars': parsed['total_chars'],
            })
            manifest['lectures'].append(lec)
            print(f'       → {safe_name} ({parsed["total_chars"]:,} 字符)')
        else:
            print(f'       ⚠️ 无文本内容，跳过')

    # Write manifest
    manifest_path = TEMP_DIR / 'manifest.json'
    # Sort chapters
    manifest['chapters'] = dict(sorted(manifest['chapters'].items()))
    manifest['lectures'].sort()
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Summary
    total_chars = sum(
        l['chars'] for ch in manifest['chapters'].values() for l in ch['lectures']
    )
    print(f'\n🎉 Phase 1 完成!')
    print(f'   {len(pdf_files)} PDF → {len(manifest["lectures"])} 个文本文件')
    print(f'   总计 {total_chars:,} 字符')
    print(f'   输出目录: {TEMP_DIR}')
    print(f'   Manifest: {manifest_path}')

if __name__ == '__main__':
    main()
