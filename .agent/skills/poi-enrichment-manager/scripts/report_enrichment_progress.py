import sqlite3
import json
import os

BASE_PATH = "/Users/wuulong/github/bmad-pa"
DB_PATH = f"{BASE_PATH}/events/notes/wuulong-notes-blog/static/walkgis_prj/walkgis.db"

def report_progress():
    if not os.path.exists(DB_PATH):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT feature_id, name, meta_data FROM walking_map_features WHERE feature_id LIKE 'COUNTY_%' OR feature_id LIKE 'TOWN_%'")
        rows = cursor.fetchall()

        stats = {
            "DEFAULT": 0,
            "AI_ENRICHED": 0,
            "DEEP_RESEARCHED": 0,
            "VERIFIED": 0,
            "UNKNOWN": 0
        }
        
        details = []

        for fid, name, meta_json in rows:
            meta = json.loads(meta_json) if meta_json else {}
            status = meta.get('enrichment_status', 'DEFAULT')
            if status in stats:
                stats[status] += 1
            else:
                stats["UNKNOWN"] += 1
            
            if status != "DEFAULT":
                details.append(f"| {fid} | {name} | {status} |")

        print("## POI Enrichment Progress Report")
        print("\n### Summary Counts")
        for k, v in stats.items():
            print(f"- {k}: {v}")
            
        if details:
            print("\n### Enriched POIs Detail")
            print("| Feature ID | Name | Status |")
            print("| --- | --- | --- |")
            print("\n".join(details))

    finally:
        conn.close()

if __name__ == "__main__":
    report_progress()
