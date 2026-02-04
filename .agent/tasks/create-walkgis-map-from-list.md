---
description: 從景點清單自動建立 WalkGIS 地圖的全流程 (搜尋 -> MD -> DB -> NotebookLM -> KML)
---

# Create WalkGIS Map from List

This task automates the creation of a full WalkGIS map package from a simple list of location names.

## 1. Input Collection
- **Ask the user** for the **"Map Name"** (This will be used as the Map Title and the `tag` for features).
- **Ask the user** for the **"List of Locations"** (Names of the POIs).
- **Define IDs**:
    - Create a `map_id` based on the date and map name (e.g., `2025_map_name_english`).
    - Create `feature_id`s for each location (e.g., `20251230_location_name`).

## 2. Research & Enrichment
- **Strategy**: Search in batches of 4-5 locations to ensure high-quality results and avoid context window limits.
- For *each* batch:
    - Use `search_web` to find **GPS Coordinates** and **Descriptions** for the locations.

## 3. Map & Feature Generation (Python Script)
- Create a **single Python script** `static/walkgis_prj/scripts/create_{map_id}.py` to handle all file generation.
- **Script Responsibilities**:
    1.  **Generate Feature Markdowns**: Create `static/walkgis_prj/features/{feature_id}.md` for each location.
    2.  **Generate Map Markdown**: Create `static/walkgis_prj/maps/{map_id}.md` including:
        - Frontmatter with `map_id` and `name`.
        - A **Mermaid graph** linking the features (e.g., `graph TD`).
        - A list of links to the feature markdown files.
    3.  **Generate SQL**: Create `static/walkgis_prj/sql/create_{map_id}.sql` to register Features, Map, and Relations.
- **Path Best Practice**: In the Python script, use `os.path.dirname(os.path.abspath(__file__))` to determine the script's location, then use relative paths like `../features`, `../maps`, and `../sql`. Avoid hardcoding absolute paths.
- **Execute**: Run the Python script.

## 4. Database Registration
- Execute the generated SQL script using `sqlite3 static/walkgis_prj/walkgis.db < static/walkgis_prj/sql/create_{map_id}.sql`.

## 5. NotebookLM Context Generation
- Execute the shell script:
  ```bash
  static/walkgis_prj/scripts/gen_notebooklm_context.sh {map_id}
  ```

## 6. KML & Navigation Link Generation
- Create a Python script `static/walkgis_prj/scripts/export_{map_id}.py` tailored for this map.
    - **Reference**: Use the logic from `static/walkgis_prj/scripts/export_map_to_google.py`.
    - **Customize**: Set `MAP_ID = "{map_id}"` and `OUTPUT_KML = "../maps/{map_id}.kml"`.
- Execute the Python script.
- **Output**: Display the path of the generated KML and the Google Maps Navigation URL to the user.

## 7. Final Report
- Summarize the actions taken:
    - Number of features created.
    - Map ID created.
    - Location of the NotebookLM context file.
    - Location of the KML file.
    - The Google Maps Link.
