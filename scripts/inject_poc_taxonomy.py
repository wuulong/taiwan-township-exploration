import sqlite3
import json
import os

DB_PATH = "/Users/wuulong/github/bmad-pa/events/AIBooks/TaiwanTownshipExploration/walkgis.db"

# 新竹市 POC 資料注入 (使用前綴匹配)
POC_DATA = {
    "TOWN_10018010": { # 新竹市東區
        "taxonomy": {
            "class": "tech_core",
            "tags": ["economy:tech", "terrain:basin", "style:modern_suburb"]
        }
    },
    "TOWN_10018020": { # 新竹市北區
        "taxonomy": {
            "class": "urban_core",
            "tags": ["culture:temple_clusters", "culture:market_life", "economy:commerce"]
        }
    },
    "TOWN_10018030": { # 新竹市香山區
        "taxonomy": {
            "class": "edge_town",
            "tags": ["terrain:coastal", "economy:agri", "status:transition"]
        }
    }
}

def inject_hsinchu_metadata_v2():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for prefix, meta in POC_DATA.items():
        # 使用 LIKE 尋找匹配的 feature_id
        cursor.execute("SELECT feature_id, meta_data FROM walking_map_features WHERE feature_id LIKE ?", (f"{prefix}%",))
        rows = cursor.fetchall()
        
        for fid, m_data in rows:
            print(f"Injecting metadata for {fid}...")
            current_meta = {}
            if m_data:
                try:
                    current_meta = json.loads(m_data)
                except:
                    pass
            
            # 注入 taxonomy
            current_meta["taxonomy"] = meta["taxonomy"]
            
            cursor.execute("UPDATE walking_map_features SET meta_data = ? WHERE feature_id = ?", 
                           (json.dumps(current_meta, ensure_ascii=False), fid))

    conn.commit()
    conn.close()
    print("Hsinchu POC Metadata injection v2 complete.")

if __name__ == "__main__":
    inject_hsinchu_metadata_v2()
