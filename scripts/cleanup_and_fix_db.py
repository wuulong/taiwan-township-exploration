import sqlite3
import os

DB_PATH = "/Users/wuulong/github/bmad-pa/events/AIBooks/TaiwanTownshipExploration/walkgis.db"
MAP_ID = "taiwan_admin_enrichment"

def fix_mojibake(text):
    if text is None:
        return None
    try:
        # 嘗試處理 Latin-1 誤認 UTF-8 的情況
        b = text.encode('latin-1')
        decoded = b.decode('utf-8')
        if decoded != text:
            return decoded
    except:
        pass
    return text

def cleanup_db():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. 清理地圖
    print(f"Keeping only map: {MAP_ID}")
    cursor.execute("DELETE FROM walking_maps WHERE map_id != ?", (MAP_ID,))
    
    # 2. 清理圖層並確保預設圖層存在
    print("Rebuilding layers...")
    cursor.execute("DELETE FROM walking_layers WHERE map_id != ?", (MAP_ID,))
    cursor.execute("INSERT OR REPLACE INTO walking_layers (layer_id, map_id, name, description) VALUES (1, ?, '行政區劃', '台灣各縣市與鄉鎮地圖層')", (MAP_ID,))

    # 3. 清理關聯
    print("Cleaning relations...")
    cursor.execute("DELETE FROM walking_map_relations WHERE map_id != ?", (MAP_ID,))

    # 4. 修復編碼 (Mojibake Fix)
    print("Fixing character encoding for maps and features...")
    
    # 修復 Maps
    cursor.execute("SELECT map_id, name, description, meta_data FROM walking_maps")
    maps = cursor.fetchall()
    for mid, name, desc, meta in maps:
        cursor.execute("UPDATE walking_maps SET name=?, description=?, meta_data=? WHERE map_id=?", 
                       (fix_mojibake(name), fix_mojibake(desc), fix_mojibake(meta), mid))

    # 修復 Features
    cursor.execute("SELECT feature_id, name, description FROM walking_map_features")
    features = cursor.fetchall()
    for fid, name, desc in features:
        cursor.execute("UPDATE walking_map_features SET name=?, description=? WHERE feature_id=?", 
                       (fix_mojibake(name), fix_mojibake(desc), fid))

    conn.commit()
    conn.close()
    print("Database cleanup and fix complete.")

if __name__ == "__main__":
    cleanup_db()
