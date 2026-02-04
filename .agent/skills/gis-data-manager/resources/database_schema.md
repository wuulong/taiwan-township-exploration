# WalkGIS Database Description (walkgis.db)

此文件定義並解釋了 WalkGIS 專案的核心資料庫結構，旨在幫助 AI 與開發者準確執行 SQL 操作。

## 📊 資料表概覽 (Tables Overview)

### 1. `layers` (圖層定義)
定義地圖點位的分類體系。
- `layer_id`: PK, 自增。
- `layer_type`: 必填，主分類 (例如：`水文與親水層`, `人文史蹟`)。
- `layer_subtype`: 次分類 (例如：`壩堰`, `古蹟/建築`)。
- `qgis_qml`: 儲存 QGIS 樣式片段。
- `description`: Markdown 格式說明。
- `meta_data`: JSON 備註。
- **唯一性**: `(layer_type, layer_subtype)` 組合不可重複。

### 2. `walking_maps` (地圖專案)
定義一個獨立的地圖探索計畫。
- `map_id`: PK, 唯一識別碼 (例如: `2026xxxx_gaoping_exploration`)。
- `name`: 專案名稱。
- `description`: 專案描述。
- `cover_image`: 封面圖路徑 (`assets/images/...`)。
- `meta_data`: JSON 格式，關鍵欄位為 `routes` (存儲 Mermaid 圖表)。

### 3. `walking_map_features` (特徵點位/幾何)
存儲所有的 POI、河流線段或流域多邊形。
- `feature_id`: UNIQUE, 檔案關聯碼，對應 `features/` 下的 `.md` 檔名。
- `name`: 顯示名稱。
- `description`: 簡要描述。
- `layer_id`: FK -> `layers.layer_id`。
- `geometry_type`: `Point`, `LineString`, 或 `Polygon`。
- `geometry_wkt`: **核心欄位**，WKT 格式幾何 (格式: `POINT(LNG LAT)` 或 `LINESTRING(LNG LAT, ...)`)。
- `meta_data`: JSON，常用於存儲標籤、亮點、座標陣列。

### 4. `walking_map_relations` (地圖-特徵關聯)
定義哪些點位屬於哪個地圖，及其顯示屬性。
- `map_id`: FK -> `walking_maps.map_id`。
- `feature_id`: FK -> `walking_map_features.feature_id`。
- `display_order`: 在地圖列表中的排序 (整數)。
- `is_highlight`: 是否標註為重點 (Boolean)。
- `note`: 針對特定地圖的專屬註解。

---

## 🛠️ 常用 SQL 指令範例 (Recipes)

### 查詢地圖中的所有點位與其圖層
```sql
SELECT f.feature_id, f.name, l.layer_type, l.layer_subtype
FROM walking_map_features f
JOIN layers l ON f.layer_id = l.layer_id
JOIN walking_map_relations r ON f.feature_id = r.feature_id
WHERE r.map_id = '2026xxxx_gaoping_exploration'
ORDER BY r.display_order;
```

### 插入新 POI (需先找到對應的 layer_id)
```sql
-- 1. 查找或建立 layer
INSERT OR IGNORE INTO layers (layer_type, layer_subtype) VALUES ('水利設施', '抽水站');
-- 2. 獲取 layer_id
SELECT layer_id FROM layers WHERE layer_type = '水利設施' AND layer_subtype = '抽水站';
-- 3. 插入 feature
INSERT INTO walking_map_features (feature_id, name, layer_id, geometry_type, geometry_wkt, description, meta_data)
VALUES ('id', 'name', 123, 'Point', 'POINT(120.4 22.5)', 'desc', '{"highlights":[]}');
```

---
*Last Updated: 2026-02-04*
