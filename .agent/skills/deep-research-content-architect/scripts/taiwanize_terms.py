import os
import argparse

# 定義置換字典
replacements = {
    "數據": "資料",
    "訊息": "資訊",
    "信息": "資訊",
    "質量": "品質",
    "項目": "專案",
    "建模": "模型化",
    "範式": "典範",
    "屏幕": "螢幕",
    "軟件": "軟體",
    "接口": "介面",
    "用戶": "使用者",
    "文檔": "文件",
    "渠道": "管道",
    "鏈接": "連結",
    "組件": "元件",
    "生命周期": "生命週期",
    "佈景": "場景",
    "解碼": "解讀",
}

def replace_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Taiwanize terminology in markdown files.")
    parser.add_argument("target_dir", help="Directory to process")
    parser.add_argument("--exclude", help="Directory name to exclude", default="Research")
    
    args = parser.parse_args()
    
    for root, dirs, files in os.walk(args.target_dir):
        if args.exclude in root:
            continue
        for file in files:
            if file.endswith(".md"):
                replace_in_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
