import os
import shutil
from datetime import datetime

def auto_backup_photos(source_dir="./photos", backup_root="./backup"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(backup_root, timestamp)
    os.makedirs(backup_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        src_file = os.path.join(source_dir, filename)
        dst_file = os.path.join(backup_dir, filename)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)

    print(f"📁 백업 완료: {backup_dir}")
    return backup_dir
