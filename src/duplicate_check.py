import os
import hashlib
import logging
from collections import defaultdict
from typing import List, Dict, Tuple
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def calculate_file_hash_fast(filepath: str, chunk_size: int = 65536) -> str:
    """
    Calculate MD5 hash of a file with optimized chunk size.
    
    Args:
        filepath: Path to the file
        chunk_size: Size of chunks to read at once (64KB default)
    
    Returns:
        MD5 hash string
    """
    try:
        hasher = hashlib.md5()
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating hash for {filepath}: {e}")
        return None

def calculate_file_hash_sample(filepath: str, sample_size: int = 8192) -> str:
    """
    Calculate hash using only first and last bytes of file (very fast).
    Less accurate but much faster for initial filtering.
    
    Args:
        filepath: Path to the file
        sample_size: Number of bytes to sample from start and end
    
    Returns:
        Hash string based on file samples
    """
    try:
        hasher = hashlib.md5()
        file_size = os.path.getsize(filepath)
        
        with open(filepath, "rb") as f:
            # Read first sample_size bytes
            start_bytes = f.read(sample_size)
            hasher.update(start_bytes)
            
            # Read last sample_size bytes
            if file_size > sample_size * 2:
                f.seek(-sample_size, 2)  # Seek from end
                end_bytes = f.read(sample_size)
                hasher.update(end_bytes)
            
            # Also include file size in hash
            hasher.update(str(file_size).encode())
            
        return hasher.hexdigest()
    except Exception as e:
        logger.error(f"Error calculating sample hash for {filepath}: {e}")
        return None

def get_file_info(filepath: str) -> Dict:
    """
    Get file information including size, modification time, etc.
    
    Args:
        filepath: Path to the file
    
    Returns:
        Dictionary with file information
    """
    try:
        stat = os.stat(filepath)
        return {
            'path': filepath,
            'size': stat.st_size,
            'mtime': stat.st_mtime,
            'name': os.path.basename(filepath)
        }
    except Exception as e:
        logger.error(f"Error getting file info for {filepath}: {e}")
        return None

def find_duplicate_photos_fast(folder_path: str, min_size: int = 1024, use_sample_hash: bool = True) -> List[List[str]]:
    """
    Find duplicate photos with optimized performance.
    
    Args:
        folder_path: Path to the folder to scan
        min_size: Minimum file size to consider (in bytes)
        use_sample_hash: If True, use faster sample-based hash first
    
    Returns:
        List of lists, where each inner list contains paths of duplicate files
    """
    if not os.path.exists(folder_path):
        logger.error(f"Folder does not exist: {folder_path}")
        return []
    
    if not os.path.isdir(folder_path):
        logger.error(f"Path is not a directory: {folder_path}")
        return []
    
    start_time = time.time()
    logger.info(f"Scanning folder: {folder_path}")
    
    # Step 1: Group files by size (very fast)
    size_groups = defaultdict(list)
    file_count = 0
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if not os.path.isfile(file_path):
            continue
            
        file_info = get_file_info(file_path)
        if file_info is None or file_info['size'] < min_size:
            continue
            
        size_groups[file_info['size']].append(file_info)
        file_count += 1
    
    logger.info(f"Found {file_count} files in {len(size_groups)} different sizes")
    
    # Step 2: Find duplicates within each size group
    duplicates = []
    potential_duplicates = 0
    
    for size, files in size_groups.items():
        if len(files) == 1:
            continue  # No duplicates possible
            
        logger.info(f"Checking {len(files)} files with size {size:,} bytes")
        potential_duplicates += len(files)
        
        if use_sample_hash:
            # Use faster sample-based hash first
            sample_hash_groups = defaultdict(list)
            
            for file_info in files:
                sample_hash = calculate_file_hash_sample(file_info['path'])
                if sample_hash:
                    sample_hash_groups[sample_hash].append(file_info['path'])
            
            # Only do full hash for files with same sample hash
            for sample_hash, file_paths in sample_hash_groups.items():
                if len(file_paths) > 1:
                    # Now do full hash comparison
                    hash_groups = defaultdict(list)
                    
                    for file_path in file_paths:
                        full_hash = calculate_file_hash_fast(file_path)
                        if full_hash:
                            hash_groups[full_hash].append(file_path)
                    
                    # Add groups with more than one file
                    for hash_value, paths in hash_groups.items():
                        if len(paths) > 1:
                            duplicates.append(paths)
                            logger.info(f"Found duplicate group with {len(paths)} files")
        else:
            # Use full hash directly
            hash_groups = defaultdict(list)
            
            for file_info in files:
                file_hash = calculate_file_hash_fast(file_info['path'])
                if file_hash:
                    hash_groups[file_hash].append(file_info['path'])
            
            # Add groups with more than one file
            for hash_value, file_paths in hash_groups.items():
                if len(file_paths) > 1:
                    duplicates.append(file_paths)
                    logger.info(f"Found duplicate group with {len(file_paths)} files")
    
    elapsed_time = time.time() - start_time
    logger.info(f"Scan completed in {elapsed_time:.2f} seconds")
    logger.info(f"Checked {potential_duplicates} files, found {len(duplicates)} duplicate groups")
    
    return duplicates

def find_duplicate_photos(folder_path: str, min_size: int = 1024) -> List[List[str]]:
    """
    Find duplicate photos in a folder using file hash comparison.
    This is the original function maintained for compatibility.
    
    Args:
        folder_path: Path to the folder to scan
        min_size: Minimum file size to consider (in bytes)
    
    Returns:
        List of lists, where each inner list contains paths of duplicate files
    """
    return find_duplicate_photos_fast(folder_path, min_size, use_sample_hash=True)

def find_duplicate_photos_by_size(folder_path: str, min_size: int = 1024) -> List[List[str]]:
    """
    Find potential duplicates by file size only (faster but less accurate).
    
    Args:
        folder_path: Path to the folder to scan
        min_size: Minimum file size to consider (in bytes)
    
    Returns:
        List of lists, where each inner list contains paths of files with same size
    """
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        logger.error(f"Invalid folder path: {folder_path}")
        return []
    
    size_groups = defaultdict(list)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if not os.path.isfile(file_path):
            continue
            
        file_info = get_file_info(file_path)
        if file_info and file_info['size'] >= min_size:
            size_groups[file_info['size']].append(file_path)
    
    # Return groups with more than one file
    return [file_paths for file_paths in size_groups.values() if len(file_paths) > 1]

def remove_duplicates(duplicates: List[List[str]], keep_oldest: bool = True) -> List[str]:
    """
    Remove duplicate files, keeping one copy.
    
    Args:
        duplicates: List of duplicate file groups
        keep_oldest: If True, keep the oldest file; if False, keep the newest
    
    Returns:
        List of removed file paths
    """
    removed_files = []
    
    for duplicate_group in duplicates:
        if len(duplicate_group) <= 1:
            continue
            
        # Sort by modification time
        files_with_time = []
        for file_path in duplicate_group:
            try:
                mtime = os.path.getmtime(file_path)
                files_with_time.append((file_path, mtime))
            except Exception as e:
                logger.error(f"Error getting modification time for {file_path}: {e}")
                continue
        
        if not files_with_time:
            continue
            
        # Sort by modification time
        files_with_time.sort(key=lambda x: x[1], reverse=not keep_oldest)
        
        # Keep the first file (oldest or newest based on keep_oldest)
        keep_file = files_with_time[0][0]
        
        # Remove the rest
        for file_path, _ in files_with_time[1:]:
            try:
                os.remove(file_path)
                removed_files.append(file_path)
                logger.info(f"Removed duplicate: {file_path}")
            except Exception as e:
                logger.error(f"Error removing file {file_path}: {e}")
    
    return removed_files

def print_duplicate_report(duplicates: List[List[str]], folder_path: str):
    """
    Print a detailed report of found duplicates.
    
    Args:
        duplicates: List of duplicate file groups
        folder_path: Original folder path
    """
    if not duplicates:
        print(f"\n✅ No duplicates found in {folder_path}")
        return
    
    print(f"\n🔍 Found {len(duplicates)} duplicate groups in {folder_path}")
    print("=" * 60)
    
    total_duplicates = sum(len(group) for group in duplicates)
    total_unique = len(duplicates)
    space_saved = 0
    
    for i, duplicate_group in enumerate(duplicates, 1):
        print(f"\n📁 Group {i} ({len(duplicate_group)} files):")
        
        # Calculate space that could be saved
        if len(duplicate_group) > 1:
            file_size = os.path.getsize(duplicate_group[0])
            space_saved += file_size * (len(duplicate_group) - 1)
        
        for j, file_path in enumerate(duplicate_group):
            try:
                file_size = os.path.getsize(file_path)
                mtime = os.path.getmtime(file_path)
                print(f"  {j+1}. {os.path.basename(file_path)}")
                print(f"      Path: {file_path}")
                print(f"      Size: {file_size:,} bytes")
                print(f"      Modified: {mtime}")
            except Exception as e:
                print(f"  {j+1}. {file_path} (Error: {e})")
    
    print(f"\n📊 Summary:")
    print(f"  - Total duplicate groups: {total_unique}")
    print(f"  - Total duplicate files: {total_duplicates}")
    print(f"  - Space that could be saved: {space_saved:,} bytes ({space_saved/1024/1024:.2f} MB)")

# Example usage and testing
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = "test_photos"
    
    print("Testing Duplicate Detection (Optimized)")
    print("=" * 40)
    
    # Find duplicates with timing
    start_time = time.time()
    duplicates = find_duplicate_photos_fast(folder_path, use_sample_hash=True)
    elapsed_time = time.time() - start_time
    
    # Print report
    print_duplicate_report(duplicates, folder_path)
    print(f"\n⏱️  Total execution time: {elapsed_time:.2f} seconds")
    
    # Ask user if they want to remove duplicates
    if duplicates:
        response = input("\nDo you want to remove duplicates? (y/N): ").lower()
        if response == 'y':
            removed = remove_duplicates(duplicates)
            print(f"\nRemoved {len(removed)} duplicate files.")
        else:
            print("No files were removed.")
