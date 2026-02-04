---
name: deep-research-content-architect
description: 整合深度研究 (Deep Research) 與多階段寫作的核心技能。適用於需要消化大量外部資料、動態生成研究指令、並進行文化語氣校準的長篇內容產製。
---

# Deep Research Content Architect Skill

此技能封裝了「代理程式寫作 (Agentic Writing)」的最佳實踐，將創作過程拆解為結構設計、深度採掘、內容合成與文化精修四個階段。

## Capabilities

1.  **ToC Architecting**: 建立具備邏輯深度與開放式架構（如動態檔案櫃）的內容大綱。
2.  **Autonomous Research Prompting**: 辨識知識缺口，動態生成高效的「深度研究指令 (Deep Research Prompts)」以獲取外部報告。
3.  **Synthesis writing**: 將多份研究報告自動轉化為模組化的章節內容，並保持敘事一致性。
4.  **Cultural Localization (Taiwanese Soul)**: 提供術語置換與語氣修正模型，確保內容符合台灣在地語境與價值觀。

## Resources

*   **Scripts**:
    *   `scripts/taiwanize_terms.py`: 批次將大陸式/通用科技用語置換為台灣慣用語。
*   **Templates**:
    *   `templates/research_prompt_template.md`: 用於對外請求深度研究的結構化指令範本。
    *   `templates/chapter_structure.md`: 確保每一章節具備「實踐註記」、「解讀邏輯」與「擴充工具箱」的深度結構。

## Instructions

### 階段一：二階段架構規劃 (Two-Stage Structuring)
1.  **Step 1: 建立全書 TOC**：優先設計具備「核心方法論」、「導航索引」與「動態實踐紀錄」的三位一體架構，確立全書的骨幹與邏輯。
2.  **Step 2: 章節範本化 (Templates)**：為每一類型的章節（如流域導航、規劃分析）建立標準範本。這能確保多人或多個 AI 會話產出的內容品質一致。
3.  **解耦 (Decoupling)**：針對隨時間增加的內容（如實作紀錄），採用「動態檔案櫃」取代固定章節編號，使用語意化檔名。

### 階段二：二階段研究採掘 (Two-Stage Research Injection)
為了確保內容廣度與深度的平衡，必須執行兩個層次的研究：
1.  **Stage A: 跨域摘要研究 (Cross-domain Summary)**：先獲得一份包含所有主題（如 11 個流域）的橫向對比資料。這用於快速填補章節骨架，確保全書不留白。
2.  **Stage B: 深度研究注入 (Deep Research Injection)**：辨識出核心節點或讀者最關心的章節，動態生成一份針對該主題的「深度研究指令」。當獲得「厚度」更強的獨立報告後，再對原先的骨架進行「版本注入式」的覆寫。

### 階段三：內容合成與結構化佈局 (Synthesis)
1.  **精煉而非複製**：注入深度報告時，應保持導航者的語氣，僅提取地質、權力、文化等「解讀邏輯」，而非貼上整篇研究。
2.  **必備模組**：每一章節需包含：
    *   **身分證 (Basic Identity)**：核心基礎資料。
    *   **靈魂特徵 (Signature)**：該章節的獨特批判視角。
    *   **方法論實踐 (Methodology Notation)**：如何應用方法論來解讀。
    *   **擴充工具箱 (Prompt Extension)**：提供讀者可進一步追問的指令。

### 階段四：在地化與品質精修 (Localization & Refinement)
1.  **術語置換**：執行 `scripts/taiwanize_terms.py` 置換通用/大陸式科技用語。
2.  **主體性注入**：進行人工覆寫，強化「台灣人視角」、「咱的土地」等情感連結。
3.  **撇步化語氣**：將專業教條改為具備「在地導覽前輩傳承經驗」感的語氣。

## Usage/Examples

*   **請求 AI 啟動寫作流程**:
    "請使用 deep-research-content-architect 技能，為我建立一份關於『台灣都市更新』的書本架構，並針對第一章產出深度研究指令..."
