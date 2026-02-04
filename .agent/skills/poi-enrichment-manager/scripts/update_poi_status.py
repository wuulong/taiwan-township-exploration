import sqlite3
import json
import sys
import os

# 設定路徑
BASE_PATH = "/Users/wuulong/github/bmad-pa"
DB_PATH = f"{BASE_PATH}/events/notes/wuulong-notes-blog/static/walkgis_prj/walkgis.db"

def update_status(feature_id, status):
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # 1. 取得目前 meta_data
        cursor.execute("SELECT meta_data FROM walking_map_features WHERE feature_id = ?", (feature_id,))
        row = cursor.fetchone()
        
        if not row:
            print(f"Error: POI {feature_id} not found in database.")
            return

        meta_data = json.loads(row[0]) if row[0] else {}
        
        # 2. 更新狀態
        meta_data['enrichment_status'] = status
        
        # 3. 寫回
        new_meta_json = json.dumps(meta_data, ensure_ascii=False)
        cursor.execute("UPDATE walking_map_features SET meta_data = ? WHERE feature_id = ?", (new_meta_json, feature_id))
        
        conn.commit()
        print(f"Successfully updated {feature_id} status to {status}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python update_poi_status.py <feature_id> <status>")
        print("Status levels: DEFAULT, AI_ENRICHED, DEEP_RESEARCHED, VERIFIED")
    else:
        update_status(sys.argv[1], sys.argv[2])
