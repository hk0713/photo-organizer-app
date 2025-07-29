def find_duplicate_photos(photo_list):
    """
    사진 리스트에서 중복된 사진을 찾는 함수 (예시 틀)
    """
    duplicates = set()
    seen = set()

    for photo in photo_list:
        if photo in seen:
            duplicates.add(photo)
        else:
            seen.add(photo)

    return list(duplicates)
