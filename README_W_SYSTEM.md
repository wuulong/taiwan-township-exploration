# 🌍 WalkGIS Data Template (地圖資料庫模板)

歡迎使用 WalkGIS Data Template！這是一個專為 [WalkGIS](https://wuulong.github.io/wuulong-notes-blog/walkgis_app/) 設計的個人地圖資料庫啟動包。

透過這個模板，您可以在幾分鐘內建立屬於自己的「去中心化地圖資料庫」，並透過 WalkGIS App 與全世界分享您的私房景點與路線。

## 🚀 快速開始 (Quick Start)

### 步驟 1: 建立您的資料庫
點擊右上角的綠色按鈕 **"Use this template"** -> **"Create a new repository"**。
這將會複製一份完整的資料庫結構到您的 GitHub 帳號下。

### 步驟 2: 開啟 GitHub Pages
進入您新建立的 Repo 頁面：
1. 點擊 **Settings** (設定) 分頁。
2. 左側選單找到 **Pages** (頁面)。
3. 在 **Build and deployment** > **Branch** 區塊，選擇 `main` 分支，然後點擊 **Save**。
4. 等待幾分鐘，當看到 "Your site is live at..." 表示資料庫已上線。

### 步驟 3: 在 WalkGIS App 中瀏覽
複製您的 GitHub Pages 網址 (例如 `https://username.github.io/my-walkgis-db/`)。
前往 [WalkGIS Web App](https://wuulong.github.io/wuulong-notes-blog/walkgis_app/)，在來源選單中選擇「自訂來源」，並貼上您的網址。

恭喜！您應該能看到範例地圖「**範例散步地圖**」已成功載入。

---

## 🤖 如何新增地圖 (使用 AI 代理人)

您不需要懂 SQL 或 Python，我們為您準備了強大的 AI 自動化任務。

**前置準備**：建議使用 [Cursor](https://cursor.sh/) 或任何支援 BMad Agent 的環境。

1.  準備一份地點清單 (例如 `my_trip.txt`)，列出您想去的景點名稱。
2.  呼叫 AI 代理人執行任務：
    ```text
    請執行 .agent/tasks/create-walkgis-map-from-list.md 任務，
    使用 my_trip.txt 作為輸入，建立一張名為 "京都拉麵之旅" 的地圖。
    ```
3.  AI 將會自動：
    *   🔍 搜尋每個地點的座標與介紹。
    *   📝 生成 `features/*.md` 檔案。
    *   💾 將資料寫入 `walkgis.db`。
    *   🗺️ 生成 `maps/*.kml` 供您匯出。

4.  完成後，將變更 **Commit & Push** 到 GitHub，您的地圖就上線了！

---

## 📂 目錄結構說明

本資料庫採用 "Database + Markdown" 的混合儲存架構：

*   **`walkgis.db`**: 核心 SQLite 資料庫。儲存地圖列表、景點座標與關聯。這是給機器讀的索引。
*   **`features/`**: 景點內容資料夾。每個景點都有一個對應的 `.md` 檔案，儲存詳細的文字介紹與圖片連結。這是給人讀的故事。
*   **`maps/`**: 地圖定義檔。包含 Mermaid 路線圖與 KML 檔案。
*   **`assets/images/`**: 存放地圖封面與相關圖片。
*   **`.agent/tasks/`**: 存放 AI 自動化任務腳本，協助您快速生成內容。
*   **`sql/`**: (進階) 資料庫架構定義檔。

## 🔗 相關資源
*   [WalkGIS App](https://walkgis-544663807110.us-west1.run.app/)
*   [WalkGIS 官方部落格](https://wuulong.github.io/wuulong-notes-blog/)

---
*Powered by WalkGIS Protocol*
