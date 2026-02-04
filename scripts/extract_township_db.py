import sqlite3
import os

SOURCE_DB = "/Users/wuulong/github/bmad-pa/events/notes/wuulong-notes-blog/static/walkgis_prj/walkgis.db"
TARGET_DB = "/Users/wuulong/github/bmad-pa/events/AIBooks/TaiwanTownshipExploration/walkgis.db"

def extract_township_data():
    if not os.path.exists(SOURCE_DB):
        print("Source DB not found.")
        return

    # 連接來源與目標
    s_conn = sqlite3.connect(SOURCE_DB)
    t_conn = sqlite3.connect(TARGET_DB)
    
    s_cursor = s_conn.cursor()
    t_cursor = t_conn.cursor()

    # 1. 搬移地圖定義
    print("Extracting map definition...")
    s_cursor.execute("SELECT * FROM walking_maps WHERE map_id = 'taiwan_admin_enrichment'")
    map_row = s_cursor.fetchone()
    if map_row:
        # 取得欄位名稱以確保匹配
        col_names = [description[0] for description in s_cursor.description]
        placeholders = ', '.join(['?'] * len(map_row))
        t_cursor.execute(f"INSERT OR REPLACE INTO walking_maps ({', '.join(col_names)}) VALUES ({placeholders})", map_row)

    # 2. 搬移行政區 POI (COUNTY_ 與 TOWN_ 開頭)
    print("Extracting administrative POIs...")
    s_cursor.execute("SELECT * FROM walking_map_features WHERE feature_id LIKE 'COUNTY_%' OR feature_id LIKE 'TOWN_%'")
    features = s_cursor.fetchall()
    
    col_names = [description[0] for description in s_cursor.description]
    placeholders = ', '.join(['?'] * len(col_names))
    
    count = 0
    for row in features:
        t_cursor.execute(f"INSERT OR REPLACE INTO walking_map_features ({', '.join(col_names)}) VALUES ({placeholders})", row)
        count += 1
    
    print(f"Total features extracted: {count}")

    t_conn.commit()
    s_conn.close()
    t_conn.close()
    print("Extraction complete.")

if __name__ == "__main__":
    extract_township_data()
