def find_duplicate_chars_count(s: str) -> dict:
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    return {char: count for char, count in counts.items() if count > 1}

print(find_duplicate_chars_count("programming"))
print(find_duplicate_chars_count("mississippi"))
print(find_duplicate_chars_count("abcdefg"))
print(find_duplicate_chars_count("abacabad"))