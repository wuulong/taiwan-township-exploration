import sqlite3
import os
import json

SOURCE_DB = "/Users/wuulong/github/bmad-pa/events/notes/wuulong-notes-blog/static/walkgis_prj/walkgis.db"
TARGET_DB = "/Users/wuulong/github/bmad-pa/events/AIBooks/TaiwanTownshipExploration/walkgis.db"

def fix_mojibake(text):
    if text is None:
        return None
    try:
        # 嘗試處理 UTF-8 被 Latin-1 解析的情況
        # 如果本來就是好的 UTF-8，這步 encode('latin-1') 可能會失敗或產生錯亂
        # 所以我們先偵測是否包含非 ASCII 且看起來像 mojibake 的字元
        # 這裡簡單判斷：如果 encode('latin-1') 成功且 decode('utf-8') 也成功且內容改變了，就採納
        b = text.encode('latin-1')
        decoded = b.decode('utf-8')
        if decoded != text:
            return decoded
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return text

def extract_township_data():
    if not os.path.exists(SOURCE_DB):
        print("Source DB not found.")
        return

    # 連接來源與目標
    s_conn = sqlite3.connect(SOURCE_DB)
    t_conn = sqlite3.connect(TARGET_DB)
    
    s_cursor = s_conn.cursor()
    t_cursor = t_conn.cursor()

    # 清理目標資料庫相關資料表
    print("Cleaning target tables...")
    t_cursor.execute("DELETE FROM walking_map_features")
    t_cursor.execute("DELETE FROM walking_map_relations")
    t_cursor.execute("DELETE FROM walking_maps WHERE map_id = 'taiwan_admin_enrichment'")
    t_cursor.execute("CREATE TABLE IF NOT EXISTS walking_layers (layer_id INTEGER PRIMARY KEY, map_id TEXT, name TEXT, description TEXT)")
    t_cursor.execute("DELETE FROM walking_layers WHERE map_id = 'taiwan_admin_enrichment'")
    
    # 也清理 relations 中殘留的 example 資料 (如果有的話)
    t_cursor.execute("DELETE FROM walking_map_relations")

    # 1. 搬移地圖定義
    print("Extracting map definition...")
    s_cursor.execute("SELECT * FROM walking_maps WHERE map_id = 'taiwan_admin_enrichment'")
    map_row = s_cursor.fetchone()
    if map_row:
        col_names = [description[0] for description in s_cursor.description]
        placeholders = ', '.join(['?'] * len(map_row))
        t_cursor.execute(f"INSERT OR REPLACE INTO walking_maps ({', '.join(col_names)}) VALUES ({placeholders})", map_row)

    # 2. 搬移圖層定義
    print("Checking for layer definitions...")
    s_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='walking_layers'")
    if s_cursor.fetchone():
        print("Extracting layer definitions...")
        s_cursor.execute("SELECT * FROM walking_layers WHERE map_id = 'taiwan_admin_enrichment'")
        layers = s_cursor.fetchall()
        for row in layers:
            t_cursor.execute("INSERT OR REPLACE INTO walking_layers (layer_id, map_id, name, description) VALUES (?, ?, ?, ?)", row)

    # 3. 搬移行政區 POI (COUNTY_ 與 TOWN_ 開頭)
    print("Extracting administrative POIs...")
    s_cursor.execute("SELECT * FROM walking_map_features WHERE feature_id LIKE 'COUNTY_%' OR feature_id LIKE 'TOWN_%'")
    features = s_cursor.fetchall()
    
    col_names = [description[0] for description in s_cursor.description]
    placeholders = ', '.join(['?'] * len(col_names))
    
    idx_id = col_names.index('feature_id')
    idx_name = col_names.index('name')
    idx_desc = col_names.index('description')
    
    count = 0
    for row in features:
        row_list = list(row)
        row_list[idx_id] = fix_mojibake(row_list[idx_id])
        row_list[idx_name] = fix_mojibake(row_list[idx_name])
        row_list[idx_desc] = fix_mojibake(row_list[idx_desc])
        
        try:
            t_cursor.execute(f"INSERT OR REPLACE INTO walking_map_features ({', '.join(col_names)}) VALUES ({placeholders})", tuple(row_list))
            count += 1
        except Exception as e:
            print(f"Error inserting feature {row_list[idx_id]}: {e}")

    print(f"Total features extracted: {count}")

    # 4. 搬移相關的 Relations
    print("Extracting relations...")
    s_cursor.execute("""
        SELECT * FROM walking_map_relations 
        WHERE map_id = 'taiwan_admin_enrichment' 
        AND (feature_id LIKE 'COUNTY_%' OR feature_id LIKE 'TOWN_%')
    """)
    relations = s_cursor.fetchall()
    if relations:
        col_rel = [description[0] for description in s_cursor.description]
        placeholders_rel = ', '.join(['?'] * len(col_rel))
        
        rel_count = 0
        idx_rel_fid = col_rel.index('feature_id')
        for r in relations:
            r_list = list(r)
            r_list[idx_rel_fid] = fix_mojibake(r_list[idx_rel_fid])
            t_cursor.execute(f"INSERT OR REPLACE INTO walking_map_relations ({', '.join(col_rel)}) VALUES ({placeholders_rel})", tuple(r_list))
            rel_count += 1
        print(f"Total relations extracted: {rel_count}")

    t_conn.commit()
    s_conn.close()
    t_conn.close()
    print("Extraction and cleanup complete.")

if __name__ == "__main__":
    extract_township_data()
