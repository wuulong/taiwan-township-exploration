---
name: poi-enrichment-manager
description: 協助進行行政區劃（縣市、鄉鎮級）POI 的內容厚化管理，追蹤並更新其富化狀態與數據整合。
---

# POI 富化管理器 (POI Enrichment Manager)

本 Skill 專為 WalkGIS 專案設計，用於管理行政區劃 POI 的富化過程，確保內容從基本的行政資訊，逐步發展為深度的文化地誌。

## 富化狀態定義 (Enrichment Status)

每個 POI 的 `meta_data` 欄位中應包含 `enrichment_status` 鍵，定義如下：

1.  **`DEFAULT`**: 初始狀態，僅包含名稱、行政代碼。
2.  **`AI_ENRICHED`**: 已透過標準 AI 搜尋完成基本歷史、地理、美食、市場、展館資訊。
3.  **`DEEP_RESEARCHED`**: 已整合外部 Deep Research (如 Gemini Advanced) 的詳細深度研究內容。
4.  **`VERIFIED`**: 經過使用者人工修訂、審閱並確認內容準確。

## 核心工作流程

### 1. 初始建立 (Default Phase)
- 使用 `create_taiwan_hierarchy_map.py` 建立全台結構。
- 初始狀態設為 `DEFAULT`。

### 2. AI 快速厚化 (AI Search Phase)
此階段目標是將 POI 提升至 `AI_ENRICHED` 等級。
- **資訊檢索**: 使用 AI 搜尋歷史發展、地理亮點、特色產業、文藝展館、傳統市場、在地小吃。
- **標準內容結構**:
    ```markdown
    # {名稱}
    ![{ID}]({影像連結})
    
    {摘要簡介}
    
    ## Highlight 亮點
    - 亮點 1...
    
    ## 🖼️ 文藝展館 (Culture & Arts)
    - 展館 1...
    
    ## 🛒 傳統市場 (Traditional Markets)
    - 市場 1...
    
    ## 🥢 在地美食 (Local Food)
    - 美食 1...
    ```
- **執行步驟**:
    1. 使用 AI 生成各行政區內容並寫入 `features/{ID}.md`。
    2. **影像厚化**: 使用 `poi-image-manager` skill 的 `enrich_map_images.py` 獲取 Wikipedia/Wikimedia 封面圖。
    3. **幾何同步**: 執行 `sync_geometry_to_md.py` 將資料庫中的 WKT 與中心點座標寫回 Markdown。
    4. **描述更新**: 執行 `sync_md_to_db.py` 將厚化後的摘要簡介同步回資料庫的 `description` 欄位。
    5. **狀態變更**: 執行 `update_poi_status.py {ID} AI_ENRICHED`。

### 3.深度研究整合 (Deep Research Phase)
此階段旨在引入高品質的人文地誌內容，提升 POI 的文化價值。
- **指令注入**: 執行 `inject_deep_research_prompts.py`。此腳本會將針對該縣市特別設計的 Deep Research Prompt 注入 Markdown 檔案，方便使用者複製。
- **外部研究**: 使用者將指令貼至 Gemini Advanced (Deep Research 模式) 生成長篇報告。
- **數據存檔**: 將原始報告存儲於 `data/deep_research/{map_id}/` (例如：`hsinchu_city_deep_research.md`)。
- **內容精煉與回填**:
    *   **人工/AI 協力**: 閱讀原始報告，提煉各行政區的高價值洞察（如歷史演進、空間再結構、文化資產意義）。
    *   **結構化回填**: 將精煉後的內容填入對應 Markdown 的 `## 🏛️ 深度人文地誌 (Deep Gazetteer)` 章節。
    *   **清理**: 移除檔案末尾的「研究指令」預留區塊。
- **狀態變更**: 執行 `update_poi_status.py {ID} DEEP_RESEARCHED`。

### 4. 人工檢校 (Verified Phase)
- **審閱**: 由具備地方知識的專業人員進行最終修訂，確保術語與在地脈絡無誤。
- **狀態變更**: `update_poi_status.py {ID} VERIFIED`。

## 🛠️ 核心腳本工具鏈

- **初始化**:
    *   `scripts/initialize_all_taiwan_admin_pois.py`: 全台 390 個行政區 POI 批量初始化。
- **數據同步**:
    *   `scripts/sync_geometry_to_md.py`: 將 WKT 邊界與中心點同步至 Markdown。
    *   `scripts/sync_md_to_db.py`: 將 Markdown 簡介同步回資料庫 `description`。
- **深度研究流**:
    *   `scripts/inject_deep_research_prompts.py`: 自動分發研究指令至各級 POI。
    *   `scripts/apply_deep_research_results.py`: (輔助) 從報告中自動提取並更新至 Markdown。
- **管理與報告**:
    *   `scripts/update_poi_status.py`: 更新資料庫中的富化狀態標籤。
    *   `scripts/report_enrichment_progress.py`: 產出全台行政區富化完成度報表。

## 💡 最佳實踐：新竹市方法論 (Hsinchu Methodology)
1.  **批量建立**全台框架，確保 ID 與 WKT 標準化。
2.  **AI 搜尋**快速生成 390 區的亮點、美食與市場基礎資料。
3.  **影像匹配**自動獲取大尺度封面（如縣市火車站、行政區老街）。
4.  **深度研究**以「縣市」為單位下 Prompt，一次獲取母體與下轄子區的歷史地誌報告。
5.  **地誌加厚**將長篇研究產出的洞察（如九降風、城池演進、科學園區再結構）回填至 POI。
