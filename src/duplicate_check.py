import os
import hashlib

def calculate_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def find_duplicate_photos(folder_path):
    seen_hashes = {}
    duplicates = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if not os.path.isfile(file_path):
            continue

        file_hash = calculate_file_hash(file_path)
        if file_hash in seen_hashes:
            duplicates.append(file_path)
        else:
            seen_hashes[file_hash] = file_path

    return duplicates
