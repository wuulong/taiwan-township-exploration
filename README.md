# 🌍 台灣鄉鎮探索導航 (Taiwan Township Exploration)

這是一個結合了 **方法論著作**、**WalkGIS 數位地圖** 與 **AI Agent 技能** 的「三位一體」探索計畫。旨在透過「架構前行」的精神，系統化地完成全台 368 個鄉鎮行政區的地誌富化。

## 📖 核心組件 (The Trinity)

1.  **實體書 (The Book)**: 
    - 位於根目錄的 `toc.md` 與各章節 Markdown 文件。
    - 提供鄉鎮探索的樣態分類、國土規劃視角與解讀邏輯。
2.  **數位系統 (W 系統)**: 
    - **地圖**: `maps/taiwan_admin_enrichment.md` 提供全島導航入口。
    - **數據**: `walkgis.db` 與 `features/` 儲存 390 個行政單元的幾何、標籤與地誌內容。
3.  **AI 助手 (Antigravity Skills)**:
    - 位於 `.agent/skills/` 內。
    - 提供全自動化的資料厚化、影像搜尋與內容同步工具。

## 🚀 快速開始

### 探索地圖
您可以直接在 [WalkGIS App](https://walkgis-544663807110.us-west1.run.app/?map=taiwan_admin_enrichment) 中開啟本專案地圖。

### 閱讀方法論
- 從 [目錄 (Table of Contents)](toc.md) 開始。
- 閱讀 [第 1 章：範式轉移](01_ParadigmShift.md) 了解計畫初衷。

### AI 協作開發
如果您使用支援 BMad Agent 的環境（如 Cursor 或 Antigravity），您可以直接執行以下指令來維護資料庫：
- `python scripts/sync_md_to_db.py`: 將 Markdown 內容同步至資料庫。
- `python scripts/update_admin_map_navigation.py`: 更新導航地圖。

## 📂 目錄結構
- `features/`: 368 鄉鎮與 22 縣市的 POI 詳細文件。
- `maps/`: WalkGIS 地圖定義文件與導覽圖。
- `plan/`: 計畫書與編寫範本。
- `scripts/`: 維護專案所需的工具腳本。
- `.agent/`: 專屬的 AI Agent 技能配置。

---
*Powered by WalkGIS Protocol & BMad Agentic AI*
