# 台灣鄉鎮分類與標籤系統辭典 (Taxonomy Dictionary)

本文件定義了《台灣鄉鎮探索導航》與 **W 系統 (WalkGIS)** 深度對齊的分類與標籤標準。所有數據注入與書本章節編寫應遵循此架構。

---

## 1. 三層式分類架構 (The Three-Layer Architecture)

### 1.1 第一層：核心樣態 (Macro-Category)
定義鄉鎮的行政與職能重心，每個鄉鎮僅限一個主樣態。

| 分類 ID | 名稱 | 說明 |
| :--- | :--- | :--- |
| `urban_core` | 都會核心 | 縣市行政、商業與經濟重心，POI 密度最高。 |
| `tech_core` | 科技/產業核心 | 具備強大產業動能、科學園區或工業基地的區域。 |
| `satellite_sprawl` | 生活衛星 | 環繞核心區、承載大規模居住與基本消費機能的延伸區。 |
| `agri_hub` | 農業功能核心 | 傳統農產集散地，保存大量傳統市場與常民生活樣貌。 |
| `edge_town` | 邊陲轉型 | 位於行政或地理邊緣，面臨人口凋零或尋求觀光/文創轉型。 |
| `resort_hub` | 觀光/生態核心 | 以自然景觀、國家公園或特定觀光遊憩為主要動能。 |
| `indigenous_vibe` | 山海原鄉 | 具備原住民族文化脈絡與特殊行政規範之區域。 |

### 1.2 第二層：多維職能標籤 (Multi-Dimensional Tags)
描述鄉鎮的具體特徵，可疊加多個標籤。

*   **經濟維度 (`economy:*`)**：
    - `economy:high_tech`, `economy:traditional_market`, `economy:commerce`, `economy:agriculture`
*   **文史維度 (`culture:*`)**：
    - `culture:temple_cluster`, `culture:colonial_heritage`, `culture:industrial_heritage`, `culture:modern_reborn`
*   **地理維度 (`geography:*`)**：
    - `geography:basin`, `geography:coastal`, `geography:terrace`, `geography:river_delta`, `geography:mountainous`
*   **交通維度 (`transport:*`)**：
    - `transport:railway`, `transport:port`, `transport:highway_hub`

### 1.3 第三層：探索進度標籤 (Process Tags)
管理數據與實地探勘的生命週期。

*   `status:scanned`：完成基本地圖框架建立。
*   `status:ai_enriched`：完成初步 AI 厚化填充。
*   `status:deep_researched`：完成深度地誌研究與內容對接。
*   `status:field_verified`：完成實地踏勘驗證。

---

## 2. 分類判定邏輯 (Classification Logic)

1.  **優先行政地位**：若為縣市政府所在地或歷史官署核心，優先判定為 `urban_core`。
2.  **產值/機能主導**：若園區產值與從業人口為主要動能，判定為 `tech_core`。
3.  **地誌脈絡判讀**：
    *   看市場與寺廟密度（判讀 `agri_hub` 或 `culture:temple_cluster`）。
    *   看人口流動方向（判讀 `satellite_sprawl`）。
4.  **轉型特徵**：若傳統產業衰退但文創/民宿興起，判定為 `edge_town` 並加上 `culture:modern_reborn`。

---

## 3. W 系統 (walkgis.db) 實作協定

標籤應儲存於 `walking_map_features` 表的 `meta_data` 欄位中。

**標準 JSON 範例：**
```json
{
  "taxonomy": {
    "class": "tech_core",
    "tags": [
      "economy:high_tech",
      "geography:basin",
      "culture:market_reborn"
    ]
  },
  "enrichment_status": "deep_researched"
}
```

---
*版本：v1.0 (2026-02-05)*
