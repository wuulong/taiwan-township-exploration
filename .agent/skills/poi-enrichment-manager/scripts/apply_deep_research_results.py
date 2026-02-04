import os
import re
import json
import sqlite3

# 設定路徑
BASE_PATH = "/Users/wuulong/github/bmad-pa"
PROJECT_ROOT = f"{BASE_PATH}/events/notes/wuulong-notes-blog/static/walkgis_prj"
DB_PATH = f"{PROJECT_ROOT}/walkgis.db"
FEATURES_DIR = f"{PROJECT_ROOT}/features"
RESEARCH_FILE = f"{PROJECT_ROOT}/data/deep_research/taiwan_admin_enrichment/新竹市地誌研究報告.md"

def update_poi_status(feature_id, status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT meta_data FROM walking_map_features WHERE feature_id = ?", (feature_id,))
    row = cursor.fetchone()
    if row:
        meta = json.loads(row[0]) if row[0] else {}
        meta['enrichment_status'] = status
        cursor.execute("UPDATE walking_map_features SET meta_data = ? WHERE feature_id = ?", 
                       (json.dumps(meta, ensure_ascii=False), feature_id))
        conn.commit()
    conn.close()

def extract_section(content, section_name):
    """提取特定區塊內容"""
    # 尋找 ### **{section_name}[:：] 到下一個同級標題 ### 或更高等級標題 ## 之前的內容
    pattern = rf"(###\s+\*\*({section_name})[:：].*?)(?=\n###\s|\n##\s|$)"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(0).strip()
    return ""

def process_deep_research():
    if not os.path.exists(RESEARCH_FILE):
        print(f"Error: Research file not found at {RESEARCH_FILE}")
        return

    with open(RESEARCH_FILE, 'r', encoding='utf-8') as f:
        research_content = f.read()

    # 1. 處理新竹市 (COUNTY)
    county_id = "COUNTY_10018_新竹市"
    county_path = os.path.join(FEATURES_DIR, f"{county_id}.md")
    if os.path.exists(county_path):
        with open(county_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 移除之前的研究指令區塊 (如果存在)
        new_lines = []
        skip = False
        for line in lines:
            if "## 🚀 深度研究指令" in line:
                skip = True
            if not skip:
                new_lines.append(line)
        
        # 注入完整的研究摘要
        summary_section = "\n## 📚 深度地誌研究 (Deep Research Summary)\n\n"
        summary_section += "本內容由 Gemini Advanced Deep Research 產出，涵蓋了新竹市從竹塹拓墾到科技矽島的完整脈絡。\n\n"
        summary_section += "### 核心主題\n"
        summary_section += "- **歷史演進**: 探討城池從莿竹、土城到石磚城的質變。\n"
        summary_section += "- **自然地理**: 九降風如何形塑米粉與玻璃產業。\n"
        summary_section += "- **社會結構**: 眷村文化與科學園區的雙重空間變奏。\n\n"
        summary_section += f"詳細研究報告請參閱: `data/deep_research/taiwan_admin_enrichment/新竹市地誌研究報告.md`\n"
        
        with open(county_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            f.write(summary_section)
        
        update_poi_status(county_id, "DEEP_RESEARCHED")
        print(f"Updated {county_id} to DEEP_RESEARCHED")

    # 2. 處理行政區 (TOWNS)
    towns = {
        "東區": "TOWN_10018010_新竹市東區",
        "北區": "TOWN_10018020_新竹市北區",
        "香山區": "TOWN_10018030_新竹市香山區"
    }

    for name, fid in towns.items():
        town_path = os.path.join(FEATURES_DIR, f"{fid}.md")
        if os.path.exists(town_path):
            section_content = extract_section(research_content, name)
            if section_content:
                with open(town_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                skip = False
                for line in lines:
                    if "## 🚀 深度研究指令" in line:
                        skip = True
                    if not skip:
                        new_lines.append(line)
                
                deep_section = f"\n## 🏛️ 深度人文地誌 (Deep Gazetteer)\n\n{section_content}\n\n"
                deep_section += f"*全文請參閱研究報告: `data/deep_research/taiwan_admin_enrichment/新竹市地誌研究報告.md`*\n"
                
                with open(town_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                    f.write(deep_section)
                
                update_poi_status(fid, "DEEP_RESEARCHED")
                print(f"Updated {fid} ({name}) to DEEP_RESEARCHED")

if __name__ == "__main__":
    process_deep_research()
