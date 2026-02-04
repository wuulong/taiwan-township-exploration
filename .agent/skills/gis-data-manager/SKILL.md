---
name: gis-data-manager
description: 協助進行地理資訊 (GIS) 數據的處理、轉換與管理，專注於河流流域、POI 地理編碼與 WalkGIS 整合。
---

# GIS Data Manager 技能說明

此技能旨在簡化空間數據的處理流程，特別是針對台灣河流探勘與 WalkGIS 專案。

## 核心能力 (Capabilities)
1. **地理編碼 (Geocoding)**: 將 POI 名稱批量轉換為經緯度與 Place ID。
2. **KML/KMZ 處理**: 合併多條河流線段、建立層級式資料（如：主流與支流）、建立符合 Google My Maps 規範的乾淨 KML。
3. **流域範圍提取**: 從大型圖資（如 SHP）中篩選特定流域範圍並轉換格式。
4. **編碼轉型 (Encoding Fix)**: 解決台灣常見的 Big5 與 UTF-8 混合導致的圖資亂碼問題。
5. **WalkGIS 整合**: 自動生成 WalkGIS 規格的 Feature Markdown 檔案與資料庫語句。
6. **整合性敘事地圖 (ISMap)**: 生成包含 Mermaid 架構圖、深度研究 Prompt、動態視覺化指引 (Dynamic View) 與景點索引的豐富地圖文件，提升圖資的可讀性與故事性。

## 常用工具與資源
- **Google Maps API**: 用於搜尋地點與編碼。
- **Python (fiona, shapely, simplekml)**: 必須使用 **conda m2504** 環境 (`/Users/wuulong/opt/anaconda3/envs/m2504/bin/python`) 進行空間分析與轉換。
- **OGR/GDAL (ogrinfo, ogr2ogr)**: 用於快速格式轉換與編碼偵測。
- **SQL (SQLite)**: 用於 WalkGIS 特徵點存儲。
- **Templates**:
    - `templates/ISMap_template.md`: 整合性敘事地圖標準模板。
    - `templates/Feature_template.md`: WalkGIS 特徵點 (Feature) 標準模板。
- **Resources**:
    - `resources/database_schema.md`: `walkgis.db` 的完整 Schema 定義與常用 SQL 語句。

## 📏 WalkGIS Feature 標準 (Standard v1.0)
所有存儲於 `features/` 的 Markdown 檔案必須符合以下規範，以確保 AI 兼容性與資料庫同步：

### 1. Frontmatter 欄位
- `id`: (必填) 唯一識別碼，格式 `YYYYMMDD_{short_id}`。
- `name`: (必填) 景點中文名稱。
- `type`: (必填) 主分類 (如: 水利設施, 自然地景, 人文史蹟, 交通設施, 服務據點)。
- `subtype`: (選填) 次分類。
- `date`: (必填) 建立日期 (YYYY-MM-DD)。
- `coordinate`: (點位必填) `[Lat, Lng]` 陣列格式。
- `geometry_type`: (必填) `Point` 或 `LineString`。
- `geometry_wkt`: (必填) WKT 字串 (WKT 座標為 `LON LAT`)。

### 2. 內容結構要求
- **標題**: 使用 `# {景點名稱}`。
- **簡介**: 第一段必須是簡短的摘要。
- **內容區塊**: 必須包含 `## 📜 歷史背景` 與 `## ✨ 亮點特色`。
- **位置資訊**: 必須在結尾包含 `## 📍 座標與地圖連結`。

## 技術工作流 (Technical Workflow)
1. **編碼與結構檢查 (Inspection)**: 
    - 使用 `ogrinfo -so` 檢查 SHP 欄位與座標系。
    - **必做：** 測試編碼 (UTF-8, Big5, CP950)，確保中文名稱在提取後不為亂碼。
2. **資料提取與預處理 (Extraction)**: 
    - 使用 Python 腳本從原始圖資提取數據。
    - **必做：** 進行幾何合併 (Dissolve)，將碎片化的河段依中文名稱合併為單一圖徵 (ST_Union / unary_union)。
    - **必做：** 進行座標簡化 (Simplify)，確保單一圖徵節點數不過多。
3. **KML 封裝 (KML Packaging)**:
    - 針對 Google My Maps 輸出時，移除所有 `ExtendedData` 或 `SchemaData`。
    - 確保 `<name>` 是 `<Placemark>` 的第一個子標籤。
    - 加入明確的 `<Style>` (LineStyle, PolyStyle) 以避免 My Maps 渲染異常。
5. **验证與發佈**: 確保點位與軌跡在目標軟體中正確疊合。
6. **資料庫同步 (Database Sync)**:
    - **必做：** 參考 `resources/database_schema.md` 以確保 SQL 語句符合最新的 Schema（特別是 `layers` 與 `walking_map_features` 的關聯）。
    - **必做：** 產出或修正 `update_walkgis_db.py`。
    - **地圖主檔更新**：將 `cover_image` (assets/images/...) 與 `meta_data` (包含 Mermaid `routes`) 寫入 `walking_maps` 表。
    - **特徵點更新**：將新 Feature 的 WKT 與分類中繼資料更新至 `walking_map_features` 並建立 `walking_map_relations`。


## 📍 Google My Maps 匯入規範 (Crucial)
若目標是 Google My Maps，開發時必須遵守以下限制：
- **格式**：優先使用 KML (不支援直接匯入 GeoJSON)。
- **大小**：單一 KML 檔案上限 5MB。
- **複雜度**：避免單一線段包含過多節點，必須進行簡化 (Simplify)。
- **結構**：My Maps 對 KML 解析非常嚴格，不支持複雜屬性。若發生「無法剖析」或「圖示亂碼」，請使用 Python 產出僅含 `<name>` 與精簡幾何的「極簡 KML」。
- **階層**：使用 `<Folder>` 標籤來區分不同的圖層 (Layer)。

## 建議任務 (Recommended Tasks)
- `geocode_pois.md`: 批量獲取地點座標。
- `river_kml_hierarchy.md`: 生成具備層級關係的河流 KML。
- `export_walkgis_features.md`: 將 POI 轉換為 WalkGIS 檔案。
- `create_rich_story_map.md`: 建立包含架構圖與深度研究 Prompt 的整合性地圖。

## 整合性地圖 (ISMap) 標準配置
建立地圖文件（如 `2026xxxx_zengwen_exploration.md`）時，應包含以下區塊：
1. **Mermaid 架構圖**: 展示河流與水利設施的邏輯關係，並同步存儲於資料庫的 `meta_data -> routes` 欄位。
2. **封面圖 (Cover Image)**: 在 Frontmatter 設定 `cover_image`，並存放於 `assets/images/`。
3. **工程與計畫細節**: 引用官方數據、計畫標案說明。
4. **資源下載**: ATAK Data Package 與相關文件的相對路徑連結。
5. **AI 深度探索 (Deep Research) Prompt**: 預設好的 Prompt，幫助使用者挖掘該區域的文史美食。
6. **Dynamic View 策略**: 提供視覺化長文本研究報告的 Prompt 建議（包含時間軸、比較表、卡片視圖）。
7. **景點 Feature 索引**: 完整條列相關點位 Markdown 檔案，連結格式應為 `[Name](?map=MAP_ID&feature=FEATURE_ID)`。

## 🔄 內容豐富化程序 (Content Enrichment Procedure)
當從 KML 或清單建立基礎 Feature 後，AI 必須執行以下「加厚」(Thick Markdown) 流程：
1. **關鍵字搜尋**: 使用 `search_web` 搜尋 `{景點名稱} 歷史 特色 美食`。
2. **多源驗證**: 比對官方手冊 (PDF) 與網路資料，確保座標與開放時間資訊正確。
3. **結構化寫作**:
   - 提取日治時期或清領時期的歷史背景。
   - 識別獨特的建築特色、生態價值或美食亮點。
   - 若為「山海驛站」，必須包含地址與服務電話。
4. **資料庫同步**: 確保 Markdown 更新後，同步執行 SQL 更新資料庫中的 `meta_data` 與 `description` 欄位。
