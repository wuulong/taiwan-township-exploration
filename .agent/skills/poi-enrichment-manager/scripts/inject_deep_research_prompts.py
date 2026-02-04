import os

# 路徑設定
BASE_PATH = "/Users/wuulong/github/bmad-pa"
PROJECT_ROOT = f"{BASE_PATH}/events/notes/wuulong-notes-blog/static/walkgis_prj"
FEATURES_DIR = f"{PROJECT_ROOT}/features"
SKILL_TEMPLATES_DIR = f"{BASE_PATH}/.agent/skills/poi-enrichment-manager/templates"

def inject_hsinchu_prompts():
    prompt_file = os.path.join(SKILL_TEMPLATES_DIR, "hsinchu_deep_research_prompt.md")
    if not os.path.exists(prompt_file):
        print(f"Error: Prompt template not found at {prompt_file}")
        return

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_content = f.read()

    # 1. 更新縣市級檔案 (注入完整 Prompt)
    county_id = "COUNTY_10018_新竹市"
    county_path = os.path.join(FEATURES_DIR, f"{county_id}.md")
    
    if os.path.exists(county_path):
        with open(county_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if "## 🚀 深度研究指令" not in content:
            section = f"\n\n## 🚀 深度研究指令 (Next Step: Deep Research)\n\n當前狀態為 `AI_ENRICHED`。欲提升至 `DEEP_RESEARCHED` 等級，請將以下指令貼至 Gemini Advanced (Deep Research 模式) 執行，完成後將結果回填至本檔案並更新狀態。\n\n```markdown\n{prompt_content}\n```\n"
            with open(county_path, "a", encoding="utf-8") as f:
                f.write(section)
            print(f"Injected full prompt into {county_id}")
        else:
            print(f"Prompt already exists in {county_id}")

    # 2. 更新鄉鎮級檔案 (注入引導連結)
    towns = [
        "TOWN_10018010_新竹市東區",
        "TOWN_10018020_新竹市北區",
        "TOWN_10018030_新竹市香山區"
    ]
    
    for town_id in towns:
        town_path = os.path.join(FEATURES_DIR, f"{town_id}.md")
        if os.path.exists(town_path):
            with open(town_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if "## 🚀 深度研究指令" not in content:
                section = f"\n\n## 🚀 深度研究指令 (Next Step: Deep Research)\n\n當前狀態為 `AI_ENRICHED`。本行政區屬於新竹市母體研究的一部分，請至 [新竹市](?map=taiwan_admin_enrichment&feature={county_id}) 獲取完整的深度研究指令 Prompt，並於研究完成後將該區結果回填至此。\n"
                with open(town_path, "a", encoding="utf-8") as f:
                    f.write(section)
                print(f"Injected reference into {town_id}")
            else:
                print(f"Reference already exists in {town_id}")

if __name__ == "__main__":
    inject_hsinchu_prompts()
