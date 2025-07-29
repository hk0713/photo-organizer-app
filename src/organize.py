import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from backup import auto_backup_photos
from duplicate_check import find_duplicate_photos
from photo_tagger import tag_photo

def main():
    print("📁 백업 시작...")
    backup_dir = auto_backup_photos()

    print("🔍 중복 검사 중...")
    duplicates = find_duplicate_photos(backup_dir)
    if duplicates:
        print(f"⚠️ 중복 사진 발견: {len(duplicates)}개")
        for d in duplicates:
            print("  -", d)
    else:
        print("✅ 중복 없음")

    print("🏷️ 태깅 시작...")
    for filename in os.listdir(backup_dir):
        path = os.path.join(backup_dir, filename)
        if os.path.isfile(path):
            tags = tag_photo(path)
            print(f"{filename}: {tags}")

if __name__ == "__main__":
    main()
